import gudhi
import numpy as np
import matplotlib.pyplot as plt
from functions import *

def main(): 
    #X = extract_points(['ivy/Ivy', 'ivy/Ivy14', 'ivy/Main'], 'classes')
    #X = extract_points(['ivy/ant'], 'classes')
    X = extract_points(['ivy/Ivy'], 'methods')

    np.random.seed(0)
    # both uniform and normal are much more spread out than actual data
    #X = np.array(np.random.uniform(high=2., low=-2., size=(70,768)), dtype=np.float32)
    #X = np.array(np.random.normal(loc=0, scale=1.0, size=(70,768)), dtype=np.float32)

    plt.scatter(X[:,0], X[:,1])
    plt.savefig('data_plot.png')

    # Large datasets (>100 points) may need to increase sparse variable to 1 or 2 to be computable in a reasonable amount of time
    # Using sparse introduces a random element as the points used to reduce are selected randomly
    st = get_rips_tree(X, max_edge=50, sparse=0, max_dim=3)
    persistent_homology(st)
    
# ## Getting Betti curves
# def Betti_curves(simplex_tree)
#     I = 50 * np.linspace(0,1,100)
#     Betti_curves = betti_curves_from_simplex_tree(simplex_tree, I)

#     # Save betti curves to an image
#     fig = plt.figure(figsize=(15,5))
#     ax1 = fig.add_subplot(1,3,1); ax2 = fig.add_subplot(1,3,2); ax3 = fig.add_subplot(1,3,3)
#     ax1.step(I, Betti_curves[0])
#     ax2.step(I, Betti_curves[1])
#     ax3.step(I, Betti_curves[2])
#     plt.savefig('Betti-Curves')


    # ploting individual dimensions looks very similar to normal distribution however normal distribution
    # points seem to be farther apart as no cc's die until 30
    # always seem to have one outlier negative point

def plot_individual_axes():
    #color = np.linspace(0,1,X.shape[0]) #, c=color
    # fig = plt.figure()
    # ax1 = fig.add_subplot(3,3,1); ax2 = fig.add_subplot(3,3,2)
    # ax3 = fig.add_subplot(3,3,3); ax4 = fig.add_subplot(3,3,4)
    # ax5 = fig.add_subplot(3,3,5); ax6 = fig.add_subplot(3,3,6)
    # ax7 = fig.add_subplot(3,3,7); ax8 = fig.add_subplot(3,3,8)
    # ax9 = fig.add_subplot(3,3,9)
    # ax1.scatter(X[:,0], X[:,1])
    # ax2.scatter(X[:,0], X[:,2])
    # ax3.scatter(X[:,0], X[:,3])
    # ax4.scatter(X[:,0], X[:,4])
    # ax5.scatter(X[:,1], X[:,2])
    # ax6.scatter(X[:,1], X[:,3])
    # ax7.scatter(X[:,1], X[:,4])
    # ax8.scatter(X[:,2], X[:,3])
    # ax9.scatter(X[:20,20], X[:20,40])
    # plt.savefig('data_plot.png')
    pass


    
# Plot and save barcode and persistence diagram
def persistent_homology(simplex_tree):
    barcode = simplex_tree.persistence(homology_coeff_field = 2)
    fig = plt.figure(figsize=(15,5))
    ax1 = fig.add_subplot(1,2,1); ax2 = fig.add_subplot(1,2,2)
    gudhi.plot_persistence_barcode(barcode, axes = ax1)
    gudhi.plot_persistence_diagram(barcode, axes = ax2)

    plt.savefig('my_plot.png')


if __name__ == "__main__":
    main()
