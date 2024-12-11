import gudhi
import numpy as np
import matplotlib.pyplot as plt
from functions import *

''' Computes the bottleneck distance between diagrams of different datasets'''

def main(): 
    '''Computing simplicial complexes:'''
    # All classes in subfolders
    datasets = [
        extract_points(['ivy/tools'], 'classes'), #/analyser
        extract_points(['ivy/util'], 'classes'),
        extract_points(['ivy/ant'], 'classes'),
        extract_points(['ivy/core'], 'classes'),
        extract_points(['ivy/osgi'], 'classes'),
        extract_points(['ivy/plugins'], 'classes')
    ]

    # Methods split by subfolder
    # datasets = [
    #     extract_points(['ivy/Ivy'], 'methods'),
    #     extract_points(['ivy/Ivy14'], 'methods'),
    #     extract_points(['ivy/Main'], 'methods'),
    #     extract_points(['ivy/tools'], 'methods'), #/analyser
    #     extract_points(['ivy/util'], 'methods'),
    #     extract_points(['ivy/ant'], 'methods'),
    #     extract_points(['ivy/core'], 'methods'),
    #     extract_points(['ivy/osgi'], 'methods'),
    #     extract_points(['ivy/plugins'], 'methods')
    # ]

    # All classes vs. subset of methods
    # datasets = [
    #     extract_points(['ivy'], 'classes'),
    #     extract_points(['ivy/core'], 'methods')
    # ]
    

    ''' Here we calculate only the first dimensional simplicies (graph), then collapse the size and expand to
    the desired dimension in order to obtain an equivalent persistence diagram in much less time'''
    # edge length increased to 60 to ensure only 1 cc remains in all cases (otherwise botl. dist = inf)
    simplex_trees = [get_rips_tree(X, max_edge=60, sparse=None, max_dim=1) for X in datasets]

    for st in simplex_trees:
        st.collapse_edges()
        st.expansion(3)

    ''' Plot and save persistence diagrams:'''
    fig = plt.figure(figsize=(25,5))
    for i, st in enumerate(simplex_trees):
        ax = fig.add_subplot(1, len(simplex_trees), i+1)
        barcode = st.persistence(homology_coeff_field=2)
        gudhi.plot_persistence_diagram(barcode, axes = ax)
        plt.title('Title')

    plt.savefig('my_plot.png')

    ''' Compute persistence values for Betti 0 and Betti 1'''
    for st in simplex_trees:
        st.compute_persistence()

    persistence_list0 = [st.persistence_intervals_in_dimension(0) for st in simplex_trees]
    persistence_list1 = [st.persistence_intervals_in_dimension(1) for st in simplex_trees]

    ''' Creating matrix of bottleneck distances'''
    l = len(simplex_trees)
    B0 = np.zeros((l, l))
    B1 = np.zeros((l, l))

    for i in range(l):
        for j in range(i):
            B0[i,j] = gudhi.bottleneck_distance(persistence_list0[i], persistence_list0[j])
            B1[i,j] = gudhi.bottleneck_distance(persistence_list1[i], persistence_list1[j])

    B0 = B0 + B0.transpose()
    B1 = B1 + B1.transpose()

    print(B0)
    print(B1)



if __name__ == "__main__":
    main()
