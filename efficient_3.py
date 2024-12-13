import numpy as np
import sys
from resource import * 
import time 
import psutil

def generate_sequence(base_s:str, operations):
    current_s = base_s
    for position in operations:
        current_s = (current_s[:position + 1] +
                        current_s +
                        current_s[position + 1:])
    return current_s

def dp_sol(x:str, y:str):
    # length of sequence
    len_1 = len(x)
    len_2 = len(y)

    # Initialize table: value of the opt solution
    # Create table
    opt = np.zeros([len_1+1,len_2+1], dtype=int)
    for i in range(len_1 + 1):
        opt[i][0] = i * 30
    for j in range(len_2 + 1):
        opt[0][j] = j * 30
    # fill
    # calculating the minimum penalty
    for i in range(1, len_1 + 1): 
        for j in range(1, len_2 + 1):
            # For sequence x & y, the index begins from 0
            opt[i][j] = min(opt[i - 1][j - 1] + alpha.get((x[i-1], y[j-1])),
                            opt[i - 1][j] + 30,
                            opt[i][j - 1] + 30)
    # print(dp)
    # Top_down pass (Reconstruction)
    i = len_1
    j = len_2
    x_ans = ""
    y_ans = ""

    while i != 0 and j != 0:
        if opt[i][j] == opt[i - 1][j - 1] + alpha.get((x[i-1], y[j-1])):
            x_ans = x[i - 1] + x_ans
            y_ans = y[j - 1] + y_ans
            i -= 1
            j -= 1
        elif opt[i][j] == opt[i - 1][j] + 30:
            x_ans = x[i - 1] + x_ans
            y_ans = '_' + y_ans
            i -= 1
        elif opt[i][j] == opt[i][j-1] + 30:
            x_ans = '_' + x_ans
            y_ans = y[j - 1] + y_ans
            j -= 1
    
    while i:
        x_ans = x[i - 1] + x_ans
        y_ans = '_' + y_ans
        i -= 1

    while j:
        x_ans = '_' + x_ans
        y_ans = y[j - 1] + y_ans
        j -= 1
 
    return opt[len_1][len_2], x_ans, y_ans

def findFinalColXl(xl, y):
    m, n = len(xl), len(y)
    # left column of window
    col_l = [int(i*30) for i in range(n+1)]
    # right column of window
    col_r = [int(0) for j in range(n+1)]

    for i in range(1,m+1): # move horizontally
        col_r[0] = 30 * i
        for j in range(1,n+1): # move up the col
            col_r[j] = min(col_l[j-1]+alpha.get((xl[i-1], y[j-1])), 
                           30 + col_r[j-1], 
                           30 + col_l[j])

        # slide window one over
        for j in range(n + 1):
            col_l[j] = col_r[j]
    return col_r

def findFinalColXr(xr, y):
    rev_xr = xr[::-1]
    rev_y = y[::-1]
    return findFinalColXl(rev_xr,rev_y)[::-1]


def findOptY(xl, xr, y):
    xl_cut = findFinalColXl(xl, y)
    xr_cut = findFinalColXr(xr, y)

    min_cost = xl_cut[0] + xr_cut[0]
    pos = 0
    for i in range(1,len(y)+1):
        if xl_cut[i]+xr_cut[i] < min_cost:
            min_cost = xl_cut[i]+xr_cut[i]
            pos = i

    return pos

def divide_conquer_sol(x:str, y:str):
    # x to xl & xr
    x_mid = int(len(x) / 2)
    if(len(x) % 2 ==1):
        x_mid = x_mid + 1

    xl = x[0:x_mid]
    xr = x[x_mid:len(x)]

    y_bestcut = findOptY(xl, xr, y)
    yl = y[:y_bestcut]
    yr = y[y_bestcut:]

    x_ans_l = ""
    x_ans_r = ""
    y_ans_l = ""
    y_ans_r = ""
    opt_score_l = 0
    opt_score_r = 0

    if len(xl) < 2 or len(yl) < 2:
        opt_score_l, x_ans_l, y_ans_l = dp_sol(xl,yl)
    else:
        opt_score_l, x_ans_l, y_ans_l = divide_conquer_sol(xl,yl)

    if len(xr) < 2 or len(yr) < 2:
        opt_score_r, x_ans_r, y_ans_r = dp_sol(xr,yr)
    else:
        opt_score_r, x_ans_r, y_ans_r = divide_conquer_sol(xr,yr)

    return opt_score_l+opt_score_r, x_ans_l+x_ans_r, y_ans_l+y_ans_r

def process_memory():
    process = psutil.Process()
    memory_info = process.memory_info()
    memory_consumed = int(memory_info.rss/1024) 
    return memory_consumed


if __name__ == '__main__':
    # Initialize
    sequence_1 = "" 
    sequence_2 = "" 
    operations_1 = []
    operations_2 = []

    # Open the file and read lines
    with open(sys.argv[-2], 'r') as file:
        change = 0
        for line in file:
            n = line.strip()
            if n.isalpha() and change == 0:
                sequence_1 = n
                change = 1
            elif n.isdigit() and change == 1:
                operations_1.append(int(n))
            elif n.isalpha() and change == 1:
                sequence_2 = n
                change = 2
            elif n.isdigit() and change == 2:
                operations_2.append(int(n))

    sequence_1 = generate_sequence(sequence_1, operations_1)
    sequence_2 = generate_sequence(sequence_2, operations_2)

    # print(sequence_1)
    # print(sequence_2)

    # dictionary for alpha penalty
    alpha = {('A', 'A'): 0, ('A', 'C'): 110, ('A', 'G'): 48, ('A', 'T'): 94,
            ('C', 'A'): 110, ('C', 'C'): 0, ('C', 'G'): 118, ('C', 'T'): 48,
            ('G', 'A'): 48, ('G', 'C'): 118, ('G', 'G'): 0, ('G', 'T'): 110,
            ('T', 'A'): 94, ('T', 'C'): 48, ('T', 'G'): 110, ('T', 'T'): 0}

    start_time = time.time() 
    results = divide_conquer_sol(sequence_1, sequence_2)
    memory_used = process_memory()
    end_time = time.time()
    time_taken = (end_time - start_time)*1000
    """
    print("Alignment Score:", results[0])
    print(results[1])
    print(results[2])
    print(time_taken)
    print(memory_used)
    """

    with open(sys.argv[-1], 'w') as file:
        file.write(str(results[0]) + "\n")
        file.write(str(results[1]) + "\n")
        file.write(str(results[2]) + "\n")
        file.write(str(time_taken) + "\n")
        file.write(str(memory_used))