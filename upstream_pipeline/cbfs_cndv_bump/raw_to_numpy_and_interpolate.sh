for case in convdiv12600 convdiv20580 cbfs13700 h20 h26 h31 h38 h42 
do
    echo $case
    python3 -u raw_to_numpy_single.py -case $case -REF_data_dir ${ML_REF_TXT_DATA} -REF_numpy_dir ${ML_NUMPY_DATASET}/REF > ${PIPELINE_LOGS}/log.raw_to_numpy_${case}
    python3 -u interpolate_REF_RANS_single.py --case $case --fine_field_dir ${ML_NUMPY_DATASET}/REF --coarse_field_dir ${ML_NUMPY_DATASET}/komegasst --output_dir ${ML_NUMPY_DATASET}/REF > ${PIPELINE_LOGS}/log.${case}_interpolate_REF_to_RANS
done
