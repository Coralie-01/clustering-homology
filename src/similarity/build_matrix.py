
import logging
from dotenv import find_dotenv, load_dotenv
import pandas as pd
import numpy as np
from Bio import Align
from Bio.Align import substitution_matrices
import matplotlib.pyplot as plt

from halo import Halo

def score(seq1,seq2):
    aligner = Align.PairwiseAligner()
    aligner.substitution_matrix = substitution_matrices.load("BLOSUM62")
    score = aligner.score(seq1,seq2)
    return score

def build_matrix(sequences):
    n = len(sequences)
    matrix = np.zeros((n,n))
    for i in range(n):
        for j in range(n):
            if i == j:
                matrix[i,j] = 0
            elif i > j:
                matrix[i,j] = matrix[j,i]
            else:
                matrix[i,j] = score(sequences[i],sequences[j])
    return matrix

def main():
    df_seq = pd.read_csv('data/processed/sequences.csv')['Sequence']
    spinner = Halo(text='Building similarity matrix', spinner='dots').start()
    similarity_matrix = build_matrix(df_seq)
    #similarity_matrix = np.load('data/processed/similarity_matrix.npy')
    spinner.succeed('Similarity matrix built')
    spinner = Halo(text='Saving similarity matrix', spinner='dots').start()
    np.save('data/processed/similarity_matrix.npy',similarity_matrix)
    spinner.succeed('Similarity matrix saved')


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()
