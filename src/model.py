import numpy as np
import pandas as pd
from Bio.Blast import NCBIWWW
from Bio.Blast import NCBIXML
from Bio import Align
from Bio.Align import substitution_matrices
import markov_clustering as mcl
import matplotlib.pyplot as plt

class SequenceData:
    def __init__(self, file_path):
        self.file_path = file_path
        self.sequences = self.load_sequences()

    def load_sequences(self):
        data = pd.read_csv(self.file_path)
        data = data.dropna()
        sequences = data['Sequence'].values
        return sequences

class SequenceAlignment:
    def __init__(self, sequences):
        self.sequences = sequences
        self.alignment_matrix = None

    def align_sequences(self):
        n = len(self.sequences)
        score_matrix = np.zeros((n, n))
        for i in range(n):
            for j in range(i,n):
                if i == j :
                    score_matrix [i,i] = 0
                else:
                    score_matrix[i, j] = score_matrix[j, i] = self.align_pairwise(self.sequences[i], self.sequences[j])
        self.alignment_matrix = score_matrix
        similarity_df = pd.DataFrame(score_matrix)
        similarity_df.to_csv('similarity_matrix.csv', index=False)

    def align_pairwise(self, seq1, seq2):
        # Align two sequences with gap opening penalty of 2 and gap extension penalty of 0.5
        aligner = Align.PairwiseAligner()
        aligner.substitution_matrix = substitution_matrices.load("BLOSUM62")

        score = aligner.score(seq1, seq2)
        return score

class MarkovClustering:
    def __init__(self, similarity_matrix):
        threeshold = np.mean(similarity_matrix) 
        threeshold_matrix = np.where(similarity_matrix < threeshold, similarity_matrix, 0)
        pd.DataFrame(threeshold_matrix).to_csv('threeshold_matrix.csv',index=False)
        rows = threeshold_matrix[threeshold_matrix.sum(axis=1) != 0]
        proba_matrix = rows / rows.sum(axis=1) 
        pd.DataFrame(proba_matrix).to_csv('proba_matrix.csv', index=False)
        self.matrix = proba_matrix
        self.clusters = None

    def run_mcl(self, inflation):
        # Apply MCL algorithm
        results = mcl.run_mcl(self.matrix, inflation=inflation)
        self.clusters = mcl.get_clusters(results)


def plot_histogramme(m):
    similarity_scores = m.flatten()

    # Create a histogram of the similarity scores
    plt.hist(similarity_scores, bins=30, color='blue')

    # Add a title and labels
    plt.title('Histogram of Similarity Scores')
    plt.xlabel('Similarity Score')
    plt.ylabel('Frequency')
    

    # Show a vertical line for mean and mean+std_dev
    mean_score = np.mean(similarity_scores)
    std_dev = np.std(similarity_scores)

    plt.axvline(mean_score, color='red', linestyle='dashed', linewidth=1)
    plt.axvline(mean_score + std_dev, color='green', linestyle='dashed', linewidth=1)

    # Show the plot
    plt.show()


def run():
    print("Modeling")
    seq_data = SequenceData("data/processed/sequences.csv")
    aligner = SequenceAlignment(seq_data.sequences)
    aligner.align_sequences()
    matrix = aligner.alignment_matrix
    print(matrix)
    #matrix = pd.read_csv('similarity_matrix.csv').values

    plot_histogramme(matrix)
    mc = MarkovClustering(matrix)
    mc.run_mcl(inflation=1.5)  # Inflation parameter 

    # Post-processing and analysis of clusters
    # Display clusters
    mcl.draw_graph(mc.matrix, mc.clusters, node_size=30, with_labels=False, edge_color="silver")
    plt.show()
    # Number of clusters 
    n_cluster = len(mc.clusters)
    print("Number of clusters: ", n_cluster)
    # Size of each cluster
    cluster_size = [len(cluster) for cluster in mc.clusters]
    print("Size of each cluster: ", cluster_size)
    # Average size of clusters
    avg_cluster_size = np.mean(cluster_size)
    print("Average size of clusters: ", avg_cluster_size)
    # Largest cluster
    largest_cluster = max(cluster_size)
    print("Largest cluster: ", largest_cluster)
    # Smallest cluster
    smallest_cluster = min(cluster_size)
    print("Smallest cluster: ", smallest_cluster)
    # Number of singletons
    n_singleton = cluster_size.count(1)
    print("Number of singletons: ", n_singleton)


