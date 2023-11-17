import os
from Bio import AlignIO
import csv
import re 

def process_phylip_file(filepath):
    """Process a single PHYLIP file and return sequence IDs and cleaned sequences."""
    alignment = AlignIO.read(filepath, "phylip-relaxed")
    data = []
    for record in alignment:
        # Extract the family, gene, and species IDs from the sequence ID
        sequence_id = record.id
        pattern = r'fam(\d+)gene(\d+)spec(\d+)'
        match = re.match(pattern, sequence_id)
        fam_id, gene_id, spec_id = match.groups()
        # Extract the alignment sequence and remove the gaps
        sequence = str(record.seq).replace('-', '') 
        data.append([fam_id,gene_id,spec_id, sequence])
    return data

def phylip_dir_to_csv(input_directory, output_file):
    """Convert all PHYLIP files in the directory to a single CSV format using AlignIO."""
    csv_data = []
    
    for filename in os.listdir(input_directory):
        if filename.endswith(".phylip"):
            filepath = os.path.join(input_directory, filename)
            csv_data.extend(process_phylip_file(filepath))

    # Write data to CSV
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Family","Gene","Species", "Sequence"])  # header
        writer.writerows(csv_data)


def run():
    print("Making dataset")
    input_directory_path = 'data/interim/alignments-v2'
    output_csv_path = 'data/processed/sequences.csv'

    phylip_dir_to_csv(input_directory_path, output_csv_path)
