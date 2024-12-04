# tda_project

Start with the tda env

Activate the conda base environment (on the bg's I used `source /opt/anaconda/bin/activate`)

Then activate the tda environment with `conda activate tda` (If this is the first time create it with `conda env create -f tda.yml`)

You may need to `pip install matplotlib` and `pip install gudhi` once inside the tda env.

generate_code_embeddings.py can be used to create the embedding data. That data should already be present on bg13 in `/scratch/mwojdak/data/`.
