import json
from pathlib import Path
import gudhi
import numpy as np
import matplotlib.pyplot as plt

def GetBettiCurvesFromPointCloud(X, J, dim=3):
    I = 2*J
    tmax = max(I)
    rips = gudhi.RipsComplex(points=X, max_edge_length = tmax, sparse = 2)
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

def extract_points(level:str):
    
    base_path = Path('/scratch/mwojdak/data/').joinpath(level)

    all_files = list(base_path.glob('**/*.json'))

    # Maybe append the directory the file was in 
    # Currently the file the object was from is not saved in the data
    X = []
    for file in all_files:
        with file.open() as f:
            data = json.load(f)
            X.append(data[0][0]) # idk but embeddings are in a nested list

    print(X[0])
    X = np.asarray(X)
    # Each embedding has >700 dimensions. about 500 embeddings for classes
    print(X.shape)
    # values ~ -10 < x < 5, most are close to 0 #always 1 very negative outlier
    print(min(X[100]))

    I = 50 * np.linspace(0,1,100)
    Betti_curves = GetBettiCurvesFromPointCloud(X, I, dim = 3)

    fig = plt.figure(figsize=(15,5))
    ax1 = fig.add_subplot(1,3,1); ax2 = fig.add_subplot(1,3,2); ax3 = fig.add_subplot(1,3,3)
    ax1.step(I, Betti_curves[0])
    #ax1.ylim(0, max(Betti_curves[0])+1)
    #ax1.title('0-Betti curve')
    
    

    #plt.figure()
    ax2.step(I, Betti_curves[1])
    #ax2.ylim(0, max(Betti_curves[1])+1)
    #ax2.title('1-Betti curve')
    #plt.savefig('Betti-1')

    #plt.figure()
    ax3.step(I, Betti_curves[2])
    #ax3.ylim(0, max(Betti_curves[2])+1)
    #ax3.title('2-Betti curve')
    #plt.savefig('Betti-2')
    plt.savefig('Betti-Curves')

    # Compring against random distributions
    # np.random.seed(1)
    # X = np.array(np.random.uniform(high=2., low=-2., size=(500,700)), dtype=np.float32)
    #X = np.array(np.random.normal(loc=0, scale=2, size=(500,700)), dtype=np.float32)
    # print(min(X[0]))

    # ploting individual dimensions looks very similar to normal distribution however normal distribution
    # points seem to be farther apart as no cc's die until 30
    # always seem to have one outlier negative point

    # TODO plot first 2 dimensions of X
    #color = np.linspace(0,1,X.shape[0]) #, c=color
    fig = plt.figure()
    ax1 = fig.add_subplot(3,3,1); ax2 = fig.add_subplot(3,3,2)
    ax3 = fig.add_subplot(3,3,3); ax4 = fig.add_subplot(3,3,4)
    ax5 = fig.add_subplot(3,3,5); ax6 = fig.add_subplot(3,3,6)
    ax7 = fig.add_subplot(3,3,7); ax8 = fig.add_subplot(3,3,8)
    ax9 = fig.add_subplot(3,3,9)
    ax1.scatter(X[:,0], X[:,1])
    ax2.scatter(X[:,0], X[:,2])
    ax3.scatter(X[:,0], X[:,3])
    ax4.scatter(X[:,0], X[:,4])
    ax5.scatter(X[:,1], X[:,2])
    ax6.scatter(X[:,1], X[:,3])
    ax7.scatter(X[:,1], X[:,4])
    ax8.scatter(X[:,2], X[:,3])
    ax9.scatter(X[:20,20], X[:20,40])
    plt.savefig('data_plot.png')


    # Sparse=2 gives very fast run times but each run has a noticably different persistence
    # Otherwise can't get past edge length of 20
    rips_complex = gudhi.RipsComplex(points=X/2, max_edge_length=50.0, sparse=2)
    st = rips_complex.create_simplex_tree(max_dimension=5)

    # TODO try to get this to work
    # Seems like alpha complexes are too slow for high dimensional data
    #alpha_complex = gudhi.AlphaComplex(points=X/2, precision='fast')
    #st = alpha_complex.create_simplex_tree(max_dimension=2)

    # result_str = 'Rips complex is of dimension ' + repr(st.dimension()) + ' - ' + \
    # repr(st.num_simplices()) + ' simplices - ' + \
    # repr(st.num_vertices()) + ' vertices.'
    # print(result_str)
    # fmt = '%s -> %.2f'
    # for filtered_value in st.get_filtration():
    #     print(fmt % tuple(filtered_value))

    barcode = st.persistence(homology_coeff_field = 2)

    fig = plt.figure(figsize=(15,5))
    ax1 = fig.add_subplot(1,2,1); ax2 = fig.add_subplot(1,2,2)

    gudhi.plot_persistence_barcode(barcode, axes = ax1)
    gudhi.plot_persistence_diagram(barcode, axes = ax2)

    plt.savefig('my_plot.png')


if __name__ == "__main__":
    extract_points("classes")
