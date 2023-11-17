from Bio import AlignIO
import os

def clean_phylip_file(input_file, output_file):
    """
    Clean the PHYLIP file by removing the 'i' at the end of the first line.
    """
    with open(input_file, 'r') as infile:
        lines = infile.readlines()
    
    # Remove 'i' from the first line
    lines[0] = lines[0].rstrip('i\n') + '\n'
    
    with open(output_file, 'w') as outfile:
        outfile.writelines(lines)

def process_directory(input_dir, output_dir):
    """
    Process all PHYLIP files in the input directory and save the cleaned files in the output directory.
    """
    # Ensure output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for filename in os.listdir(input_dir):
        if filename.endswith(".phylip"):
            input_file = os.path.join(input_dir, filename)
            output_file = os.path.join(output_dir, filename)
            clean_phylip_file(input_file, output_file)
            #print(f"Processed {filename}")



def run():

    # Specify the directory containing the original PHYLIP files
    input_directory = 'data/raw/alignments'
    output_directory = 'data/interim/alignments-v2'

    process_directory(input_directory, output_directory)
