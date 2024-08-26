#!/bin/bash

# Directory containing the Markdown files
input_dir="../autosearch_projects/polymer_representation/polymer_representation/0.3/output/markdown"
output_dir="../ragtest/input"

# Create the output directory if it doesn't exist
mkdir -p "$output_dir"

# Loop through all Markdown files in the input directory
for md_file in "$input_dir"/*.md; do
  # Get the base name of the file (without the directory and extension)
  # print the nemar of the file
  echo "$md_file"
  base_name=$(basename "$md_file" .md)
  
  # Convert the Markdown file to a text file
  pandoc "$md_file" -t plain -o "$output_dir/$base_name.txt"
done

echo "Conversion complete."