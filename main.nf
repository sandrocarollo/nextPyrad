#!/usr/bin/env nextflow

nextflow.enable.dsl = 2

include { pyTask } from "./modules/pyTask"
include { merge } from "./modules/merge"

workflow {
    
    //Validate input parameters
    assert params.input_img_mask != null : "Please specify a correct path for the input img data"
    assert params.pattern != null : "Please specify a valid pattern to subdivide scan from segmentation"
    input_img_mask = file(params.input_img_mask, checkIfExists: true)
    pattern = params.pattern
    outdir = file(params.outdir, checkIfExists: true)
    read_img = Channel.fromFilePairs("${input_img_mask}/**/${pattern}", type: 'file').ifEmpty { exit 1, "Cannot find any input data matching"}

    //start workflow
    pyTask( read_img )
    merge( pyTask.out.rad_csv.collect() )

}