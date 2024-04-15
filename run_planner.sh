#!/bin/bash

# Define the base directory
BASEDIR="/config/workspace/Plannif_auto"

# Set PYTHONPATH to include the directory of the script
export PYTHONPATH="$BASEDIR:$PYTHONPATH"

# Path to the domain file
domain_file="$BASEDIR/Group6/Taquin/taquin_domain.pddl"

# Directory containing the problem files
problems_folder="$BASEDIR/Group6/Taquin/problem"

# Output file to store all results
output_file="$BASEDIR/all_results.txt"

# Remove the output file if it exists to avoid appending to old results
if [ -f "$output_file" ]; then
    rm "$output_file"
fi

# Create an array of problem files and sort them
mapfile -t problem_files < <(find "$problems_folder" -name "*.pddl" -print | sort)

# Display the order of problem files
echo "The following problem files will be processed in this order:"
printf "%s\n" "${problem_files[@]}"

# Loop through each sorted problem file
for problem_file in "${problem_files[@]}"; do
    echo "Processing problem: $problem_file" >> "$output_file"
    # Execute the planner with the domain file and the current problem file
    python3 "$BASEDIR/pddl_parser/planner.py" "$domain_file" "$problem_file" >> "$output_file"
    echo "----------------------------------------" >> "$output_file"
done

echo "All problems have been processed. Results are stored in $output_file."
