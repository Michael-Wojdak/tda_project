from DTM_filtrations import *

import gudhi
import numpy as np
import matplotlib.pyplot as plt

from functions import *

# higher values of p tend to simplify the persistence diagram
# different values of m may highlight various areas of the dataset

X = extract_points(['ivy/'], 'classes')

' Usual Rips complex on X '
st_rips = gudhi.RipsComplex(points=X).create_simplex_tree(max_dimension=2) # create a Rips complex     
diagram_rips = st_rips.persistence()                                       # compute the persistence

# plot the persistence diagram
gudhi.plot_persistence_diagram(diagram_rips)                    
plt.title('Persistence diagram of the Rips complex')
plt.savefig('my_plot')

' Compute the DTM on X ' 
# compute the values of the DTM of parameter m
m = 0.1                    
DTM_values = DTM(X,X,m)             

# plot of the DTM
plt.figure()
plot=plt.scatter(X[:,0], X[:,1], c=DTM_values)
plt.colorbar(plot)
plt.axis('equal')
plt.title('Values of the DTM on X with parameter m='+str(m))
plt.savefig('output')

# m = 0.1               # parameter of the DTM
# N = np.shape(X)[0]    # number of points
# k = int(m*N)          # parameter of the DTMRipsComplex in gudhi

# dtm_rips = gudhi.dtm_rips_complex.DTMRipsComplex(points=X, k=k)  # DTM-Filtration in gudhi
# st_DTM = dtm_rips.create_simplex_tree(max_dimension=2)
# diagram_DTM = st_DTM.persistence()                               # compute the persistence diagram

# # plot the persistence diagram
# gudhi.plot_persistence_diagram(diagram_DTM)
# plt.title('Persistence diagram of the DTM-filtration with parameter p ='+str(1))
# plt.savefig('output')

' Compute a DTM-filtration '
p = 1                                    
dimension_max = 2                               # maximal dimension to expand the complex
st_DTM = DTMFiltration(X, m, p, dimension_max)  # creating a simplex tree
diagram_DTM = st_DTM.persistence()              # compute the persistence diagram

# plot the persistence diagram
gudhi.plot_persistence_diagram(diagram_DTM)
plt.title('Persistence diagram of the DTM-filtration with parameter p ='+str(p))
plt.savefig('dtm_pd')

# Seems like higher p flattens all cc bars, no interesting homology seems to emerge