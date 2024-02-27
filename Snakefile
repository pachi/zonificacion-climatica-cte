import pandas as pd
from snakemake.utils import min_version

min_version("7.0")


rule all:
    input:
        "data/output/Results.csv",
        "data/output/plots/zci-diff-hist.png",
        "data/output/plots/zcv-diff-hist.png",
        "data/output/plots/zc-tmy.png",


rule plot:
    input:
        "data/output/Results.csv",
    output:
        "data/output/plots/zci-diff-hist.png",
        "data/output/plots/zcv-diff-hist.png",
        "data/output/plots/zc-tmy.png",
    conda:
        "envs/environment.yml"
    notebook:
        "notebooks/graficas.ipynb"


checkpoint select_input:
    input:
        "data/ign/MUNICIPIOS.csv",
    output:
        "data/output/Municipios.csv",
    conda:
        "envs/environment.yml"
    script:
        "src/select_input.py"


def get_tmy_link(wildcards):
    """Llamadas a la API de PVGIS para obtener datos climáticos en formato TMY.
    Documentación de la API en:
    https://joint-research-centre.ec.europa.eu/pvgis-photovoltaic-geographical-information-system/getting-started-pvgis/api-non-interactive-service_en

    Está limitado a 30 req/s, de modo que hay que llamar a snakemake con la opcion --max-jobs-per-second 29
    """
    URL = "https://re.jrc.ec.europa.eu/api/v5_2/tmy?lat={lat}&lon={lon}&outputformat=csv&startyear=2005&endyear=2020"
    with open(checkpoints.select_input.get(**wildcards).output[0]) as f:
        df = pd.read_csv(f)
        res = df.query(f'ARCHIVO_TMY=="{wildcards.loc_id}"')
        q = res.to_dict("records")[0]
        return URL.format(lat=q["LATITUD_ETRS89"], lon=q["LONGITUD_ETRS89"])


def get_all_tmy_files(wildcards):
    """Calcula archivos GNL para todos los municipios de BFA"""
    with open(checkpoints.select_input.get(**wildcards).output[0]) as f:
        df = pd.read_csv(f, dtype={"ARCHIVO_TMY": str})
        tmy_files = expand("data/output/tmy/{loc_id}", loc_id=df.ARCHIVO_TMY)
        return tmy_files


rule download_tmy_loc:
    input:
        ancient("data/output/Municipios.csv"),
    params:
        link=get_tmy_link,
        script=Path(workflow.basedir) / "src/download_file.py",
    output:
        "data/output/tmy/{loc_id}",
    conda:
        "envs/environment.yml"
    message:
        "Descarga de archivo TMY de localidad de PV-GIS"
    shell:
        "python3 {params.script} --link {params.link:q} --output_file {output:q}"


rule download_tmy_all:
    input:
        tmy_files=ancient(get_all_tmy_files),
    output:
        touch("data/output/tmy/downloads.done"),
    message:
        "Descarga de conjunto de archivos con datos TMY de PV-GIS"


rule compute_indicators:
    input:
        "data/output/Municipios.csv",
        "data/output/downloads.done",
    output:
        "data/output/Results.csv",
    conda:
        "envs/environment.yml"
    script:
        "src/compute_indicators.py"
