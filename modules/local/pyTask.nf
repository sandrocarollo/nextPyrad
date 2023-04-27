process PYTASK{
    tag "$sample_id"
    label 'process_pyradiomics'

    //Packages dependencies
    //conda 'conda-forge::python=3.7 anaconda::future auto::logging anaconda::pandas simpleitk::simpleitk anaconda::yaml conda-forge::argparse radiomics:pyradiomics'

    publishDir "${params.outdir}/${sample_id}", mode: "${params.publish_dir_mode}"

    input:
        tuple val(sample_id), file(in_img)

    output:
        path "${sample_id}.csv", emit: rad_csv

    when:
        task.ext.when == null || task.ext.when

    script:
    """
    pyradpanda.py \\
        --inputimage ${in_img[0]} \\
        --inputmask ${in_img[1]} \\
        --outputfilename ${sample_id}.csv
    """
}
