import gudhi
import numpy as np
import matplotlib.pyplot as plt
from functions import *

'''
Compares computing rips complexes with diffirent values of sparse in terms of run time and persistence diagrams
'''

def main(): 
    X = extract_points(['ivy/core', 'ivy/ant'], 'classes')

    '''Compute and time creating the rips complex using different values of sparse'''
    st_none = time_function(get_rips_tree, X, max_edge=50, sparse=None, max_dim=3)
    st_1 = time_function(get_rips_tree, X, max_edge=50, sparse=1, max_dim=3)
    st_2 = time_function(get_rips_tree, X, max_edge=50, sparse=2, max_dim=3)

    ''' Plot and save barcode and persistence diagram:'''
    barcode_none = st_none.persistence(homology_coeff_field = 2)
    barcode_1 = st_1.persistence(homology_coeff_field = 2)
    barcode_2 = st_2.persistence(homology_coeff_field = 2)

    fig = plt.figure(figsize=(15,5))
    ax1 = fig.add_subplot(1,3,1); ax2 = fig.add_subplot(1,3,2); ax3 = fig.add_subplot(1,3,3)
    
    gudhi.plot_persistence_diagram(barcode_none, axes = ax1)
    ax1.set_title("sparse=None")
    gudhi.plot_persistence_diagram(barcode_1, axes = ax2)
    ax2.set_title("sparse=1")
    gudhi.plot_persistence_diagram(barcode_2, axes = ax3)
    ax3.set_title("sparse=2")

    plt.savefig('sparse_pd.png')


if __name__ == "__main__":
    main()
