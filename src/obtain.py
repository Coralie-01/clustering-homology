from asymmetree.treeevolve import species_tree_n_age
from asymmetree.genome import GenomeSimulator
from asymmetree.seqevolve import SubstModel, IndelModel



def run():
    """Run the simulation."""
    # simulate the common species tree
    S = species_tree_n_age(10, 1.0, model='yule')

    # specify models for sequence evolution
    subst_model = SubstModel('a', 'JTT')
    indel_model = IndelModel(0.01, 0.01, length_distr=('zipf', 1.821))

    # initialy GenomeSimulator instance
    gs = GenomeSimulator(S, outdir='data/raw')

    # simulate 50 gene trees along the species tree S (and write them to file)
    gs.simulate_gene_trees(50, dupl_rate=1.0, loss_rate=0.5,
                        base_rate=('gamma', 1.0, 1.0),
                        prohibit_extinction='per_species')

    # simulate sequences along the gene trees
    gs.simulate_sequences(subst_model,
                        indel_model=indel_model,
                        het_model=None,
                        length_distr=('constant', 200))

