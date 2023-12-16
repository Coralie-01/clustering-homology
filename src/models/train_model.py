
from dotenv import find_dotenv, load_dotenv
import pandas as pd
import numpy as np
from Bio import Align
from Bio.Align import substitution_matrices
import matplotlib.pyplot as plt
import markov_clustering as mc
import click
from halo import Halo



@click.command()
def main():
    matrix = np.load('data/processed/similarity_matrix.npy')
    matrix = (matrix - np.min(matrix)) / (np.max(matrix) - np.min(matrix))

    # Apply threeshold
    matrix[matrix < 0.1] = 0

    row_sums = matrix.sum(axis=1)
    stochastic_matrix = matrix / row_sums[:, np.newaxis]

    stochastic_matrix[np.isnan(stochastic_matrix)] = 0

    np.save('data/processed/stochastic_matrix.npy', stochastic_matrix)

    for i in range(11,15):
        inflation = i/10
        result = mc.run_mcl(stochastic_matrix, inflation=inflation)
        clusters = mc.get_clusters(result)
        print(clusters)
        #Q = mc.modularity(matrix=result, clusters=clusters)
        #print("inflation:", inflation, "modularity:", Q)

        mc.draw_graph(matrix, clusters, node_size=50, with_labels=False, edge_color="silver")
        plt.savefig(f'reports/figures/mcl{inflation}.png')


if __name__ == '__main__':

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()
