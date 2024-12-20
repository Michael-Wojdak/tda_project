# tda_project

### Setup:

Code in this repo is designed to be run using the tda environment.

If the tda environment has not been created yet create it with `conda env create -f tda.yml`.

To activate the tda environment first activate the conda base environment (on the bg's I used `source /opt/anaconda/bin/activate`).
Then activate the tda environment with `conda activate tda`.

You may need to run `pip install matplotlib` and `pip install gudhi` once inside the tda env.

DTM_filtrations.py also requires `pip install scikit-learn` and `pip install scipy`.

`generate_code_embeddings.py` can be used to create the embedding data from the files listed in `download_urls.json`. That data is saved to `/scratch/mwojdak/data/` and should already be present on the bg13 machine.

### Scripts:

`DTM_filtrations.py`, `unixcoder.py`, and `functions.py` are utility scripts that are used by other files

Other scripts are designed to be modified/run individually and explore different aspects of the project:

`rips_complexes.py` analyzes the performance of calculating persitent homology using rips complexes.

`alpha_complexes.py` analyzes the performance of calculating persistent homology using alpha complexes.

`persistent_homology.py` generates Betti curves, persistence barcodes, and persistence diagrams.

`bottleneck_dist.py` compares persistence diagrams of multiple datasets and computes bottleneck distances between them.

`dtm.py` uses a DTM filtration to compute persistent homology of data.

Some notworthy figures are included in the figures directory.