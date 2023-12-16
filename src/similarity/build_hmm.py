import os
import subprocess
import pandas as pd
from halo import Halo


def download_uniprot_db(database_dir, database_url):
    # Create database directory if it doesn't exist
    os.makedirs(database_dir, exist_ok=True)
    # Change to the database directory
    os.chdir(database_dir)
    # Download the UniProt database
    subprocess.run(["wget", database_url])
    # Extract the downloaded database
    tar_file = database_url.split('/')[-1]
    subprocess.run(["tar", "-xzvf", tar_file])
    # Clean up the tar file
    os.remove(tar_file)

def make_muscle_alignment(sequences, output_dir):
    for i,seq in enumerate(sequences):
        output_file = os.path.join(output_dir, f"seq{i}.fasta")
        with open(output_file, 'w') as f:
            f.write(f">seq{i}\n")
            f.write(f"{seq}\n")

def generate_msa():
    fasta_dir = "data/raw/fasta_files/"
    for fasta_file in os.listdir(fasta_dir):
        seq_file = os.path.join(fasta_dir, fasta_file)
        output_msa_dir = "data/processed/msa"
        os.makedirs(output_msa_dir, exist_ok=True)
        output_msa_file = os.path.join(output_msa_dir, fasta_file)
        subprocess.run(["hhblits", "-i", seq_file, "-oa3m", output_msa_file])


def create_db_from_fasta(fasta_dir, output_dir):
    fasta_file = os.path.join(fasta_dir, "1.faa")
    subprocess.run(["hhmake", "-i", fasta_file, "-o", "data/external/db/db.hmm"])

def create_hmm_with_hhblits(fasta_dir, output_dir):
    # Create hmm directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    # file path
    file_path = os.path.join(fasta_dir, "2.faa")
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
    output_dir = "data/processed/hmm"
    os.makedirs(output_dir, exist_ok=True)

    #make_fasta_from_sequences(sequences_df, fasta_dir)
    create_hmm_with_hhblits(fasta_dir, output_dir)

    # # Create HMMs for each sequence
    # hmm_files = []
    # for index, row in sequences_df.iterrows():
    #     seq_id = f"seq{index}"
    #     hmm_file = create_hmm_with_hhblits(row['Sequence'], seq_id, output_dir)
    #     hmm_files.append(hmm_file)

    # # Perform pairwise HMM comparisons
    # pairwise_hmm_comparison(hmm_files, output_dir)

if __name__ == '__main__':
    main()
