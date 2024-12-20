import gudhi
import numpy as np
import matplotlib.pyplot as plt
from functions import *

'''
Computes the persistent homology of the specified data and generates Betti curves,
barcodes, and persistence diagrams
'''

def main(): 
    '''Extracting data:'''
    #X = extract_points(['ivy/Ivy', 'ivy/Ivy14', 'ivy/Main'], 'classes')
    X = extract_points(['ivy'], 'classes')
    #X = extract_points(['ivy/Ivy'], 'methods')
    #X = extract_points(['ivy/Ivy'], 'tokens')

    # Random distributions for comparison:
    np.random.seed(0)
    #X = np.array(np.random.uniform(high=2., low=-2., size=(70,768)), dtype=np.float32)
    X = np.array(np.random.normal(loc=0, scale=1.0, size=(70,768)), dtype=np.float32)

    '''Computing simplicial complexes:'''
    # Large datasets (>100 points) may need to increase sparse variable to 1 or 2 to be computable in a reasonable amount of time
    # Using sparse introduces a random element as the points used to reduce are selected randomly
    st = get_rips_tree(X, max_edge=50, sparse=None, max_dim=1)
    # Alternatively use max_dim=1 and expand to required dimension using the code below
    st.collapse_edges(); st.expansion(3)

    ''' Getting Betti curves:'''
    I = 50 * np.linspace(0,1,100)
    Betti_curves = betti_curves_from_simplex_tree(st, I)

    # Save betti curves to an image
    fig = plt.figure(figsize=(15,5))
    ax1 = fig.add_subplot(1,3,1); ax2 = fig.add_subplot(1,3,2); ax3 = fig.add_subplot(1,3,3)
    ax1.step(I, Betti_curves[0])
    ax2.step(I, Betti_curves[1])
    ax3.step(I, Betti_curves[2])
    plt.savefig('Betti-Curves')

    '''Plot and save barcode and persistence diagram:'''
    barcode = st.persistence(homology_coeff_field = 2)

    # Plot both barcode and persistence diagram
    # fig = plt.figure(figsize=(15,5))
    # ax1 = fig.add_subplot(1,2,1); ax2 = fig.add_subplot(1,2,2)
    # gudhi.plot_persistence_barcode(barcode, axes = ax1)
    # gudhi.plot_persistence_diagram(barcode, axes = ax2)

    # Plot only persistence diagram
    gudhi.plot_persistence_diagram(barcode)

    plt.savefig('persistence_diagram.png')


if __name__ == "__main__":
    main()
