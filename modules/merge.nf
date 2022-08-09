#!/usr/bin/env nextflow

nextflow.enable.dsl=2

mode = params.publish_dir_mode

process merge{
    
    publishDir "${params.outdir}", mode: "$mode"

    input:
        path csv
    output:
        path "*.csv"

    script:
    """
    HEADER=\$(head -1 ${csv.get(0)})
    for i in ${csv}
    do
        sed -i '1d' \$i
    done
    echo \$HEADER > NSCLC_features_results.csv
    find . -maxdepth 1 -iname '*.csv' -not -name 'NSCLC_features_results.csv' -exec cat {} + >> NSCLC_features_results.csv
    """

}