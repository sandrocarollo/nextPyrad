#!/usr/bin/env nextflow

nextflow.enable.dsl=2

mode = params.publish_dir_mode

process pyTask{
    //Packages dependencies
    //conda 'conda-forge::python=3.7 anaconda::future auto::logging anaconda::pandas simpleitk::simpleitk anaconda::yaml conda-forge::argparse radiomics:pyradiomics'

    publishDir "${params.outdir}/${sample_id}", mode: "$mode"

    input:
        tuple val(sample_id), file(in_img)

    output:
        path "${sample_id}.csv", emit: rad_csv

    script:
    """
    pyradpanda.py --inputimage ${in_img[1]} --inputmask ${in_img[0]} --outputfilename ${sample_id}.csv
    """
}