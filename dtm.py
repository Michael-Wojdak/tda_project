from DTM_filtrations import *

import gudhi
import matplotlib.pyplot as plt

from functions import *

'''
Uses the DTM filtration to compute persistent homology. The DTM should reduce the impact of outliers.
Requires the sklearn package (run `pip install scikit-learn` if it is not present)

Different values of m may highlight various areas of the dataset.
Higher values of p tend to simplify the persistence diagram.

Seems like higher values of p flatten all cc bars, no interesting homology seems to emerge.
'''

def main():
    X = extract_points(['ivy/'], 'classes')

    ' Usual Rips complex on X '
    st_rips = gudhi.RipsComplex(points=X).create_simplex_tree(max_dimension=2) # create a Rips complex     
    diagram_rips = st_rips.persistence()                                       # compute the persistence

    # plot the persistence diagram
    gudhi.plot_persistence_diagram(diagram_rips)                    
    plt.title('Persistence diagram of the Rips complex')
    plt.savefig('persistence_diagram')

    ' Compute the DTM on X ' 
    # compute the values of the DTM of parameter m
    m = 0.1                    
    DTM_values = DTM(X,X,m)             

    # plot of the DTM on X
    # arranges points along first two axes, maybe a different visualization could be more helpful?
    plt.figure()
    plot=plt.scatter(X[:,0], X[:,1], c=DTM_values)
    plt.colorbar(plot)
    plt.axis('equal')
    plt.title('Values of the DTM on X with parameter m='+str(m))
    plt.savefig('data_plot')

    ' Compute a DTM-filtration '
    p = 1                                    
    dimension_max = 2                               # maximal dimension to expand the complex
    st_DTM = DTMFiltration(X, m, p, dimension_max)  # creating a simplex tree
    diagram_DTM = st_DTM.persistence()              # compute the persistence diagram

    # plot the persistence diagram
    gudhi.plot_persistence_diagram(diagram_DTM)
    plt.title('Persistence diagram of the DTM-filtration with parameter p ='+str(p))
    plt.savefig('dtm_pd')


if __name__ == "__main__":
    main()