for i in {1..15}
do
    input_file="in${i}.txt"
    output_file="output${i}.txt"

    python3 efficient_3.py "$input_file" "$output_file"
done