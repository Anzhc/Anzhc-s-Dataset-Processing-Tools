import os

def remove_tags(file1_path, file2_path, output_path):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file1_path = os.path.join(script_dir, file1_path)
    file2_path = os.path.join(script_dir, file2_path)
    output_path = os.path.join(script_dir, output_path)

    with open(file1_path, 'r') as file1, open(file2_path, 'r') as file2, open(output_path, 'w') as output_file:
        tags = set(file2.read().splitlines())

        for line in file1:
            if line.strip() not in tags:
                output_file.write(line)

    print(f"Tags removed successfully. Output file saved at {output_path}")


# Usage example:
file1_path = 'wanted_tags.txt'  # Path to the first file
file2_path = 'unwanted_tags.txt'  # Path to the second file containing the tags
output_path = 'output.txt'  # Path to save the output file

remove_tags(file1_path, file2_path, output_path)