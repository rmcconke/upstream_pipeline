#!/bin/bash

echo Writing duct Pinelli raw data to text files.
for Re in 1100 1150 1250 1300 1350 1400 1500 1600 1800 2000 2205 2400 2600 2900 3200 3500
do
    echo $Re
    python3 -u duct_raw_to_fields.py -raw_filename ${ML_DUCT_DATA}/pinelli_rawdata/statistics_0${Re}_repo.bin -Re $Re -DNS_data_dir ${ML_DUCT_DATA}/squareDuct_fields/ &
    pid=$!
    sleep 0.25
done

# Write duct raw data to foam for gradient computations


echo Writing duct raw data to foam.
for Re in 1100 1150 1250 1300 1350 1400 1500 1600 1800 2000 2205 2400 2600 2900 3200 3500
do
    echo $Re
    python3 -u write_duct_DNS_to_foam.py -Re $Re -DNS_data_dir ${ML_DUCT_DATA}/squareDuct_fields/ -DNS_foam_dir ${ML_FOAM_DATASET}/DNS/squareDuct > ${PIPELINE_LOGS}/log.duct_dns_to_foam_${Re} &
    pid=$!
    sleep 0.25

done

wait $pid
echo Finished writing duct raw data to foam.
# Extract computed foam fields from RANS and DNS
echo Reading numpy fields from foam cases.
echo DNS:
for case in squareDuct_Re_1100 squareDuct_Re_1150 squareDuct_Re_1250 squareDuct_Re_1300 squareDuct_Re_1350 squareDuct_Re_1400 squareDuct_Re_1500 squareDuct_Re_1600 squareDuct_Re_1800 squareDuct_Re_2000 squareDuct_Re_2205 squareDuct_Re_2400 squareDuct_Re_2600 squareDuct_Re_2900 squareDuct_Re_3200 squareDuct_Re_3500
do
    echo $case
    ./duct_DNS_single.sh $case &
    pid1=$!
    sleep 0.25
done

echo RANS:
for case in squareDuct_Re_1100 squareDuct_Re_1150 squareDuct_Re_1250 squareDuct_Re_1300 squareDuct_Re_1350 squareDuct_Re_1400 squareDuct_Re_1500 squareDuct_Re_1600 squareDuct_Re_1800 squareDuct_Re_2000 squareDuct_Re_2205 squareDuct_Re_2400 squareDuct_Re_2600 squareDuct_Re_2900 squareDuct_Re_3200 squareDuct_Re_3500
do
    echo $case
    ./duct_RANS_single.sh $case &
    pid2=$!
    sleep 0.25
done
wait $pid1 $pid2
echo Finished reading numpy fields from foam cases.

echo Averaging RANS duct fields along x-direction.

# Average duct RANS fields along x (flow) direction to get a yz plane
for Re in 1100 1150 1250 1300 1350 1400 1500 1600 1800 2000 2205 2400 2600 2900 3200 3500
do
    echo $Re
    python3 -u average_duct_RANS.py -Re $Re -case_type komegasst -RANS_numpy_dir ${ML_NUMPY_DATASET}/komegasst/ > ${PIPELINE_LOGS}/log.duct_average_RANS_x_${Re}_komegasst &
    pid=$!
done
wait $pid

# Average duct RANS fields along x (flow) direction to get a yz plane
for Re in 1100 1150 1250 1300 1350 1400 1500 1600 1800 2000 2205 2400 2600 2900 3200 3500
do
    echo $Re
    python3 -u average_duct_RANS.py -Re $Re -case_type komega -RANS_numpy_dir ${ML_NUMPY_DATASET}/komega/ > ${PIPELINE_LOGS}/log.duct_average_RANS_x_${Re}_komega &
    pid=$!
done

wait $pid
# Average duct RANS fields along x (flow) direction to get a yz plane
for Re in 1100 1150 1250 1300 1350 1400 1500 1600 1800 2000 2205 2400 2600 2900 3200 3500
do
    echo $Re
    python3 -u average_duct_RANS.py -Re $Re -case_type kepsilonphitf -RANS_numpy_dir ${ML_NUMPY_DATASET}/kepsilonphitf/ > ${PIPELINE_LOGS}/log.duct_average_RANS_x_${Re}_kepsilonphitf &
    pid=$!
done

wait $pid
echo Finished averaging RANS duct fields along x-direction.

echo Interpolating DNS yz plane fields to RANS yz plane fields.
# Interpolate DNS yz plane fields to RANS yz plane fields
for Re in 1100 1150 1250 1300 1350 1400 1500 1600 1800 2000 2205 2400 2600 2900 3200 3500
do
    echo $Re
    for field in tau divtau gradU S R U a b k
    do
        python3 -u interpolate_DNS_RANS.py --case $Re --field $field --fine_field_dir ${ML_NUMPY_DATASET}/REF --coarse_field_dir ${ML_NUMPY_DATASET}/komegasst --output_dir ${ML_NUMPY_DATASET}/REF > ${PIPELINE_LOGS}/log.duct_interpolate_DNS_to_RANS_${Re}_${field} &
        pid=$!
    done
done

wait $pid
echo Finished interpolating DNS yz plane fields to RANS yz plane fields.






