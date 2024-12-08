import gudhi
import numpy as np
import matplotlib.pyplot as plt
from functions import *

''' Computes the bottleneck distance between diagrams of different datasets'''

def main(): 
    '''Computing simplicial complexes:'''
    datasets = [
        extract_points(['ivy/Ivy'], 'methods'),
        extract_points(['ivy/Ivy14'], 'methods'),
        extract_points(['ivy/Main'], 'methods'),
        extract_points(['ivy/tools/analyser'], 'methods')
    ]
    
    simplex_trees = []
    for X in datasets:
        simplex_trees.append(get_rips_tree(X, max_edge=50, sparse=0, max_dim=3))

    ''' Plot and save persistence diagrams:'''
    fig = plt.figure(figsize=(20,5))
    for i, st in enumerate(simplex_trees):
        ax = fig.add_subplot(1, len(simplex_trees), i+1)
        barcode = st.persistence(homology_coeff_field=2)
        gudhi.plot_persistence_diagram(barcode, axes = ax)

    plt.savefig('my_plot.png')


if __name__ == "__main__":
    main()
