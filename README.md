[![Nextflow](https://img.shields.io/badge/nextflow%20DSL2-%E2%89%A522.10.1-23aa62.svg)](https://www.nextflow.io/)
[![run with conda](http://img.shields.io/badge/run%20with-conda-3EB049?labelColor=000000&logo=anaconda)](https://docs.conda.io/en/latest/)
[![run with docker](https://img.shields.io/badge/run%20with-docker-0db7ed?labelColor=000000&logo=docker)](https://www.docker.com/)
[![run with singularity](https://img.shields.io/badge/run%20with-singularity-1d355c.svg?labelColor=000000)](https://sylabs.io/docs/)
[![Launch on Nextflow Tower](https://img.shields.io/badge/Launch%20%F0%9F%9A%80-Nextflow%20Tower-%234256e7)](https://tower.nf/launch?pipeline=https://github.com/nf/nextpyrad)

## Introduction

<!-- TODO nf-core: Write a 1-2 sentence summary of what data the pipeline is for and what it does -->

**nextPyrad** is a bioinformatics best-practice analysis pipeline designed for processing CT scans and extracting Radiomics features from medical images. Utilizing Pyradiomics, an open-source Python package, this pipeline automates the extraction of Radiomics features, making it a valuable tool for medical imaging research.

The pipeline is built using [Nextflow](https://www.nextflow.io), a workflow tool to run tasks across multiple compute infrastructures in a very portable manner. It uses Docker/Singularity containers making installation trivial and results highly reproducible. The [Nextflow DSL2](https://www.nextflow.io/docs/latest/dsl2.html) implementation of this pipeline uses one container per process which makes it much easier to maintain and update software dependencies. Where possible, these processes have been submitted to and installed from [nf-core/modules](https://github.com/nf-core/modules) in order to make them available to all nf-core pipelines, and to everyone within the Nextflow community!

## Pipeline summary

<!-- TODO nf-core: Fill in short bullet-pointed list of the default steps in the pipeline -->

* **Input:** Read folder with medical images and corresponding masks in NIfTI format.
* **Processing:** Utilize ([PyRadiomics](https://pyradiomics.readthedocs.io/en/latest/index.html)) to extract Radiomics features.
* **Output:** Merge all the individual Radiomics feature patient's file in a unified final CSV file `NSCLC_features_results.csv`

## Quick Start

1. Install [`Nextflow`](https://www.nextflow.io/docs/latest/getstarted.html#installation) (`>=22.10.1`)

2. Download the pipeline by cloning the repository

   ```bash
   git clone git@github.com:sandrocarollo/nextPyrad.git
   cd nextPyrad
   ```

3. Create and activate conda environment
   ```bash
   conda env create -f environment.yml
   conda activate nextpyrad
   ```
   
4. Run the pipeline:

   ```bash
   nextflow run main.nf 
   ```

5. Start running your own analysis!

   In order to do so you should keep your data in a certain folder structure like this one:
   ```bash
      Data
      ├── Sample_1
      │   ├── sample1_image.nrrd
      │   └── sample1_seg.nrrd
      ├── ...
      ├── Sample_N
      │   ├── sampleN_image.nrrd
      │   └── sampleN_seg.nrrd
      └── ...
   ```
   >
   >Note that the predifined pattern to access all the Images and the respective Masks is `*_{image,seg}.n*`, meaning that the image file should have "_image" and the mask "_seg" as a suffix.
   
   Use:
   ```bash
   nextflow run main.nf --input_img_mask = "./data/Test" --pattern = "*_{image,seg}.n*"
   ```
   where the flags `--input_img_mask` and `--pattern` replace the predefined values. 

## Acknowledgments

nextPyrad was originally written by Sandro Carollo.

## Citations

If you use nextPyrad for your research, please cite its use in your publications.

