# tda_project

Start with the tda env

Activate the conda base environment (on the bg's I used `source /opt/anaconda/bin/activate`)

Then activate the tda environment with `conda activate tda` (If this is the first time create it with `conda env create -f tda.yml`)

You may need to `pip install matplotlib` and `pip install gudhi` once inside the tda env.
some gudhi modules like dtm also requires scipy `pip install scipy` (not used currently)
DTM_filtrations.py requires `pip install scikit-learn`

generate_code_embeddings.py can be used to create the embedding data. That data should already be present on bg13 in `/scratch/mwojdak/data/`.

`functions.py` contains utility functions used in the other files

Other scripts like `persistent_homology.py` and `bottleneck_distance.py` are designed to be modified/run individually.



1. persistent homology used to show persistence diagrams and betti curves. Compared against uniform and normal distributions
data seems to have a wider range of spacings with components merging at early, mid, and late thickening values (other distributions looked highly separated by comparison).

2. bottleneck distance compares different persistence diagrams, so far haven't been able to detect any strong differences
between any levels or sets of embedings

3. dtm filtrations should help reduce noise, seems to reduce to nothing interesting (single c.c. no other features).

TODO

4. more advanced selection of which embedings to consider?