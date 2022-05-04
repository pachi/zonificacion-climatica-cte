conda: "environment.yaml"

rule all:
    input: "data/output/plots/histo.png"

rule plot:
    input: "data/output/Results.csv"
    output: "data/output/plots/histo.png"
    script: "src/plot_results.py"

rule select_input:
    input: "data/ign/MUNICIPIOS.csv"
    output: "data/output/Municipios.csv"
    script: "src/select_input.py"

rule download_data:
    input: "data/output/Municipios.csv"
    output: "data/output/downloads_done.txt"
    shell: "python3 src/download_TMY.py && touch data/output/downloads_done.txt"

rule compute_indicators:
    input: "data/output/Municipios.csv", "data/output/downloads_done.txt"
    output: "data/output/Results.csv"
    script: "src/compute_indicators.py"
