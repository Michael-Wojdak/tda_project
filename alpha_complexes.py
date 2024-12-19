import gudhi
import matplotlib.pyplot as plt
from functions import *

'''
Code for testing the performance of alpha complexes:

generates an alpha complex for the given data and plots the persistence diagram.

Due to the high dimensonality of embedding vectors, alpha complexes take a long time to run
3 points ~ 60 sec
4 points ~ 90 sec
6 points ~ 150 sec

Asymptotic complexity may be better than rips complexes, but does not seem to be practical in this case
'''

def main(): 
    '''Computing simplicial complexes:'''
    X = extract_points(['ivy/Ivy', 'ivy/Ivy14', 'ivy/Main'], 'classes')
    #X = extract_points(['ivy/tools'], 'classes')
    #X = extract_points(['ivy/util/filter'], 'classes')

    # Seems like alpha complexes are too slow for high dimensional data (only 3 points takes 1 min)
    # Interestingly distances seem different when using alpha complexes (values almost 10x what rips gives)
    # precision seems to have little impact at least under these circumstances
    alpha_complex = time_function(gudhi.AlphaComplex, points=X) #, precision='fast')
    st = alpha_complex.create_simplex_tree()
    print('Alpha complex is of dimension ', st.dimension(), ' - ', st.num_simplices(), ' simplices - ', st.num_vertices(), ' vertices.')

    ''' Plot and save barcode and persistence diagram:'''
    barcode = st.persistence(homology_coeff_field = 2)
    fig = plt.figure(figsize=(15,5))
    ax1 = fig.add_subplot(1,2,1); ax2 = fig.add_subplot(1,2,2)
    gudhi.plot_persistence_barcode(barcode, axes = ax1)
    gudhi.plot_persistence_diagram(barcode, axes = ax2)

    plt.savefig('persistence_diagram.png')


if __name__ == "__main__":
    main()
