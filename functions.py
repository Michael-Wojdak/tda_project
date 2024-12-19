import json
from pathlib import Path
import gudhi
import numpy as np
import matplotlib.pyplot as plt

import time

'''Contains functions used for extracting data and performing topological calculations'''

def extract_points(paths = ['ivy/'], level = 'classes'):
    '''
    Grabs all json files from the specified directories and extracts embedding data in the form of a point cloud

    Input:
        paths: a list of paths within the data directories from which to extract embeddings
        level: the desired level of granularity of the embeddings ('classes', 'methods', 'tokens')
    '''
    base_path = Path('/scratch/mwojdak/data/').joinpath(level)

    X = []

    for path in paths:
        p = base_path.joinpath(path)
        files = list(p.glob('**/*.json'))

        for file in files:
                with file.open() as f:
                    data = json.load(f)
                    X.append(data[0][0]) # not sure why but embeddings are in a nested list
    
    X = np.asarray(X)
    print('Extracted point cloud contains %d points' % X.shape[0])

    return X


def get_rips_tree(X, max_edge, sparse, max_dim, print_filtration=False):
    '''
    Takes a point cloud and returns a simplex tree generated using the rips complex

    Input:
        X: a point cloud
        max_edge: the maximum length of edges allowed in the rips complex
        sparse: how much to simplify the point cloud (can be None)
        max_dim: max dimension including in the calculation of the rips complex
        print_filtration: if true prints all simplicies and their filtration values

    Returns:
        st: a simplex tree
    '''
    rips = gudhi.RipsComplex(points=X, max_edge_length = max_edge, sparse = sparse)
    st = rips.create_simplex_tree(max_dimension=max_dim)

    result_str = 'Rips complex is of dimension ' + repr(st.dimension()) + ' - ' + \
    repr(st.num_simplices()) + ' simplices - ' + \
    repr(st.num_vertices()) + ' vertices.'
    print(result_str)
    fmt = '%s -> %.2f'
    
    if print_filtration:
        for filtered_value in st.get_filtration():
            print(fmt % tuple(filtered_value))
    
    return st

# Function copied from EMAp tutorial 2 (https://github.com/raphaeltinarrage/EMAp/blob/main/Tutorial2-Correction.ipynb)
def GetBettiCurvesFromPointCloud(X, J, dim=3):
    '''
    Computes the Betti curves of the Rips complex on the point cloud X, 
    on the interval J, up to dimension dim.

    Input:
        X (np.array): size Nx2, the point cloud.
        J (np.array): interval. Shape 1xM. 
        dim (int, optional): maximal dimension to compute the Betti curves. 
    
    Output:
        BettiCurves (np.array): the Betti curves. Shape (dim+1)xM. The ith 
                                Betti curve is given by BettiCurve[i,:].  
                                
    Example:
        X = np.asarray([[0,1],[1,0],[-1,1]])
        J = np.linspace(0,1,100)
        GetBettiCurvesFromPointCloud(X, J, dim = 2)
    '''
    I = 2*J
    tmax = max(I)
    rips = gudhi.RipsComplex(points=X, max_edge_length = tmax)
    st = rips.create_simplex_tree(max_dimension=dim)
    st.persistence(persistence_dim_max=True, homology_coeff_field = 2)
    Diagrams = [st.persistence_intervals_in_dimension(i) for i in range(dim+1)]
    BettiCurves = []
    step_x = I[1]-I[0]
    for diagram in Diagrams:
        bc =  np.zeros(len(I))
        if diagram.size != 0:
            diagram_int = np.clip(np.ceil((diagram[:,:2] - I[0]) / step_x), 0, len(I)).astype(int)
            for interval in diagram_int:
                bc[interval[0]:interval[1]] += 1
        BettiCurves.append(np.reshape(bc,[1,-1]))
    return np.reshape(BettiCurves, (dim+1, len(I)))


def betti_curves_from_simplex_tree(st, I, dim=3):
    '''
    Computes the Betti curves of the given simplex tree

    Input:
        st: a simplex tree
        I: interval over which to calculate the Betti curves
        dim: maximal dimension to compute the Betti curves.

    Returns:
        BettiCurves: array representing the Betti curves
    '''
    st.persistence(persistence_dim_max=True, homology_coeff_field = 2)
    Diagrams = [st.persistence_intervals_in_dimension(i) for i in range(dim+1)]
    BettiCurves = []
    step_x = I[1]-I[0]
    for diagram in Diagrams:
        bc =  np.zeros(len(I))
        if diagram.size != 0:
            diagram_int = np.clip(np.ceil((diagram[:,:2] - I[0]) / step_x), 0, len(I)).astype(int)
            for interval in diagram_int:
                bc[interval[0]:interval[1]] += 1
        BettiCurves.append(np.reshape(bc,[1,-1]))
    return np.reshape(BettiCurves, (dim+1, len(I)))


def time_function(func, *args, **kwargs):
    '''
    Prints the time it took to excecute a function while returning the output

    Input:
        func: the function to be timed
        *args and **kwargs: the arguments as they would be input into func
    
    Returns:
        result: the return of func
    '''
    start_time = time.perf_counter()
    result = func(*args, **kwargs)
    end_time = time.perf_counter()
    print(f'{func.__name__:s} took {end_time - start_time : 0.4f} seconds')
    return result
