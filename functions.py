import json
from pathlib import Path
import gudhi
import numpy as np
import matplotlib.pyplot as plt

''' Contains functions used for extracting data and performing topological calculations'''

# Grabs all json files from each path in paths and returns a point cloud of their embedding
def extract_points(paths = ['ivy/'], level = 'classes'):
    base_path = Path('/scratch/mwojdak/data/').joinpath(level)

    X = []
    #Y=[] # corresponding data that can distinguish points based on origin etc.
    # name of folder one level up (file it was contained in), directory the file was in

    for path in paths:
        p = base_path.joinpath(path)
        files = list(p.glob('**/*.json'))

        for file in files:
                with file.open() as f:
                    data = json.load(f)
                    X.append(data[0][0]) # idk but embeddings are in a nested list
    
    X = np.asarray(X)
    # Each embedding has >700 dimensions. about 500 embeddings for classes
    print('Extracted point cloud contains %d points' % X.shape[0])

    return X

def get_rips_tree(X, max_edge, sparse, max_dim, print_filtration=False):
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

# From TDA tutorials
def GetBettiCurvesFromPointCloud(X, J, dim=3):
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