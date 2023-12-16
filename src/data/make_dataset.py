# -*- coding: utf-8 -*-
import click
import logging
from pathlib import Path
from dotenv import find_dotenv, load_dotenv
import pandas as pd

from asymmetree.treeevolve import species_tree_n_age
from asymmetree.genome import GenomeSimulator
from asymmetree.seqevolve import SubstModel, IndelModel, HetModel
from Bio import AlignIO
import os
import csv
import re


def load_data():
    """
    Simulate evolution and put the result in data/raw
    """
    # simulate the common species tree
    S = species_tree_n_age(10, 1.0, model='yule')

    # specify models for sequence evolution
    subst_model = SubstModel('a', 'JTT')
    indel_model = IndelModel(0.01, 0.01, length_distr=('zipf', 1.821))
    het_model = HetModel(2.0)

    # initialy GenomeSimulator instance
    gs = GenomeSimulator(S, outdir='data/raw/')

    # simulate 50 gene trees along the species tree S (and write them to file)
    gs.simulate_gene_trees(50, dupl_rate=1.0, loss_rate=0.4,
                        base_rate=('gamma', 0.7, 0.7),
                        prohibit_extinction='per_species')

    # simulate sequences along the gene trees
    gs.simulate_sequences(subst_model,
                        indel_model=indel_model,
                        het_model=het_model,
                        length_distr=('constant', 500))


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
        

def clean_directory(input_dir, output_dir):
    """
    Removes the i in all PHYLIP files in the input directory and save the cleaned files in the output directory.
    """
    # Ensure output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for filename in os.listdir(input_dir):
        if filename.endswith(".phylip"):
            input_file = os.path.join(input_dir, filename)
            output_file = os.path.join(output_dir, filename)
            clean_phylip_file(input_file, output_file)
            print(f"Processed {filename}")


def process_phylip_file(filepath):
    """Process a single PHYLIP file and return sequence IDs and cleaned sequences."""
    print("Process",filepath)
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
    
    data = pd.read_csv(output_file)
    data.dropna(inplace=True)
    data.to_csv(output_file, index=False)


def phylip_to_fasta(input_path, output_path):
    """Convert a single all phylip files from a directory into fasta files """
    for file in os.listdir(input_path):
        if file.endswith(".phylip"):
            input_file = os.path.join(input_path, file)
            output_file = os.path.join(output_path, file.replace(".phylip", ".fasta"))
            AlignIO.convert(input_file, "phylip-relaxed", output_file, "fasta")
    


@click.command()
@click.argument('input_filepath', type=click.Path(exists=True))
@click.argument('output_filepath', type=click.Path())
def main(input_filepath, output_filepath):
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    logger = logging.getLogger(__name__)
    logger.info('making final data set from raw data')

    # Create data from AsymmeTree evolution
    load_data()

    # Specify the directory containing the original PHYLIP files and where the new ones should be saved 
    input_directory = 'data/raw/alignments'
    output_directory = 'data/interim/alignments-v2'

    # Clean the PHYLIP files
    clean_directory(input_directory, output_directory)


    # Process the files to remove gaps and save as CSV
    input_directory_path = 'data/interim/alignments-v2'
    output_csv_path = 'data/processed/sequences.csv'

    phylip_dir_to_csv(input_directory_path, output_csv_path)



if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()
