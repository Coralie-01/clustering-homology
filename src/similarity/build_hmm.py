import os
import subprocess
import pandas as pd
from halo import Halo
from Bio import SeqIO




def generate_msa():
    fasta_dir = "data/raw/fasta_files/"
    for fasta_file in os.listdir(fasta_dir):
        seq_file = os.path.join(fasta_dir, fasta_file)
        output_msa_dir = "data/processed/msa"
        os.makedirs(output_msa_dir, exist_ok=True)
        output_msa_file = os.path.join(output_msa_dir, fasta_file)
        subprocess.run(["hhblits", "-i", seq_file, "-oa3m", output_msa_file])

def remove_empty_sequences(input_dir, output_dir):
    """Remove empty sequences from all fasta files in the input directory and save the cleaned files in the output directory."""
    for filename in os.listdir(input_dir):
        if filename.endswith(".faa"):
            input_file = os.path.join(input_dir, filename)
            output_file = os.path.join(output_dir, filename)
            with open(input_file, "r") as infile, open(output_file, "w") as outfile:
                for record in SeqIO.parse(infile, "fasta"):
                    if len(record.seq) > 0:  # Check if the sequence is not empty
                        SeqIO.write(record, outfile, "fasta")


def create_hmm_with_hhblits(fasta_dir, output_dir):
    # Create hmm directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    # file path
    file_path = os.path.join(fasta_dir, "5.faa")
    # Create the HMM
    subprocess.run(["hhblits", "-i", file_path, "-d", "/app/data/external/uniprot_sprot_vir70/uniprot_sprot_vir70", "-oa3m", "seq.a3m","-cpu", "4","-M","first"])

def pairwise_hmm_comparison(hmm_files, output_dir):
    spinner = Halo(text='Running pairwise HMM comparisons', spinner='dots').start()
    for i in range(len(hmm_files)):
        for j in range(i + 1, len(hmm_files)):
            output_file = os.path.join(output_dir, f"comparison_{i}_{j}.hhr")
            subprocess.run(["hhalign", "-i", hmm_files[i], "-j", hmm_files[j], "-o", output_file])
    spinner.succeed("Pairwise HMM comparisons completed.")

def main():
    sequences_df = pd.read_csv("data/processed/sequences.csv")
    fasta_dir = "data/raw/fasta_files/"
    database_dir = "data/external/database"
    output_dir = "data/processed/fasta"
    os.makedirs(output_dir, exist_ok=True)

    # Remove empty sequences
    remove_empty_sequences(fasta_dir, output_dir)

    fasta_dir = output_dir
    output_dir = "data/processed/hmm"
    create_hmm_with_hhblits(fasta_dir, output_dir)

    # Pairwise HMM comparison
    hmm_files = [os.path.join(output_dir, file) for file in os.listdir(output_dir)]
    

if __name__ == '__main__':
    main()
