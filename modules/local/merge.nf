process MERGE{
    tag "$csv"
    label 'process_merge'

    publishDir "${params.outdir}", mode: "${params.publish_dir_mode}"

    input:
        path csv

    output:
        path "*.csv",   emit: csv

    when:
    task.ext.when == null || task.ext.when
    
    script:
    """
    HEADER=\$(head -1 ${csv.get(0)})
    for i in ${csv}
    do
        sed -i '1d' \$i
    done
    echo \$HEADER > Radiomics_features_results.csv
    find . -maxdepth 1 -iname '*.csv' -not -name 'Radiomics_features_results.csv' -exec cat {} + >> Radiomics_features_results.csv
    """

}