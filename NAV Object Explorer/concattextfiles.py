import os

def concatenate_txt_files(folder_path, output_file):
    # List all txt files in the folder
    txt_files = [f for f in os.listdir(folder_path) if f.endswith('.txt')]

    # Concatenate the contents of each file
    concatenated_content = ""
    for file in txt_files:
        with open(os.path.join(folder_path, file), 'r',encoding='iso-8859-1') as f:
            concatenated_content += f.read() + "\n"

    # Write the concatenated content to the output file
    with open(output_file, 'w',encoding='iso-8859-1') as f:
        f.write(concatenated_content)

# Specify the folder path and output file
folder_path = "path"  # Replace with your folder path
output_file = "path"

concatenate_txt_files(folder_path, output_file)
