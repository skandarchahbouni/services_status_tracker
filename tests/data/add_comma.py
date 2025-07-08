input_file = "history.ndjson"
output_file = "history_with_commas.ndjson"

# Open the input file and the output file
with open(input_file, "r") as infile, open(output_file, "w") as outfile:
    for line in infile:
        # Add a comma at the end of each line and write to the output file
        outfile.write(line.strip() + ",\n")

print(f"File with commas added has been saved to {output_file}")