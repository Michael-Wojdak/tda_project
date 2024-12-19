import gudhi
import numpy as np
import matplotlib.pyplot as plt
from functions import *

'''
Code for testing the performance of rips complexes:

The first section (sparse) tests the effects of the sparse parameter on performance and persistent homology.
The second section (variations) tests an alternative way of computing the persistent homology that is much faster
'''

def sparse(): 
    '''
    Compares computing rips complexes with diffirent values of sparse in terms of run time and persistence diagrams.
    High values of sparse give significant speed ups, but can drastically alter persistant homology and are somewhat random.

    sparse=None:
    Rips complex is of dimension 3 - 2000592274 simplices - 579 vertices.
    get_rips_tree took  64.2231 seconds
    
    sparse=1:
    Rips complex is of dimension 3 - 1376876777 simplices - 579 vertices.
    get_rips_tree took  42.5172 seconds
    
    sparse=2:
    Rips complex is of dimension 3 - 3457 simplices - 579 vertices.
    get_rips_tree took  0.3579 seconds)
    '''

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



def variations(): 
    '''
    An alternative way of computing the rips complex is much faster and gives equivalent persistent homology.
    By only computing the simplex tree up to the first dimension, collapsing the resulting graph, then expanding up
    to the desired dimension, a much smaller complex can be analyzed.

    On a point cloud of about 600 points:

    sparse=None:
    Rips complex is of dimension  3  -  2000592274  simplices -  579  vertices.
    usual_rips took  66.6048 seconds

    sparse=1:
    Rips complex is of dimension  3  -  1358488310  simplices -  579  vertices.
    usual_rips took  45.6246 seconds

    sparse=2:
    Rips complex is of dimension  3  -  5054  simplices -  579  vertices.
    usual_rips took  4.3841 seconds

    alternative method:
    Rips complex is of dimension  3  -  47927  simplices -  579  vertices.
    fast_rips took  0.6582 seconds
    '''

    def usual_rips(X, s=None):
        '''Usual construction of a rips complex'''
        rips = gudhi.RipsComplex(points=X, max_edge_length=50, sparse=s)
        st = rips.create_simplex_tree(max_dimension=3)

        print('Rips complex is of dimension ', st.dimension(), ' - ', st.num_simplices(), ' simplices - ', st.num_vertices(), ' vertices.')

        return st

    def fast_rips(X):
        '''Computing only one dimensional simplicies then expanding to achieve equivalent persistent homology'''
        rips = gudhi.RipsComplex(points=X, max_edge_length=50, sparse=None)
        st = rips.create_simplex_tree(max_dimension=1)
        st.collapse_edges()
        st.expansion(3)

        print('Rips complex is of dimension ', st.dimension(), ' - ', st.num_simplices(), ' simplices - ', st.num_vertices(), ' vertices.')

        return st

    #X = extract_points(['ivy/Ivy', 'ivy/Ivy14', 'ivy/Main'], 'classes')
    #X = extract_points(['ivy/ant'], 'classes')
    #X = extract_points(['ivy/Ivy'], 'methods')
    X = extract_points(['ivy'], 'classes')
    #X = extract_points(['ivy/Ivy'], 'tokens')

    # Alternate method for computing the persistent homology of the rips complex is much faster 
    time_function(usual_rips, X, None)
    time_function(usual_rips, X, 1)
    time_function(usual_rips, X, 2)
    time_function(fast_rips, X)

if __name__ == "__main__":
    sparse()
    #variations()
