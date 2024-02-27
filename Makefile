all: run_all

run_all:
	snakemake -c all -s ./Snakefile -d . --max-jobs-per-second 29 -- all

download_tmy_all:
	snakemake -c all -s ./Snakefile -d . --max-jobs-per-second 29 -- download_tmy_all

compute_indicators:
	snakemake -c all -s ./Snakefile -d . -- compute_indicators

plot:
    jupyter nbconvert --to notebook --execute --allow-errors notebooks/graficas.ipynb

create_conda_envs:
	conda env create -n zonificacion-climatica-cte -f envs/environment.yml

clean_snakemake_metadata:
	rm -rf .snakemake/metadata/*
	rm -rf .snakemake/log/*

clean_snakemake_conda_envs:
	rm -rf .snakemake/conda/*
