#!/bin/bash

python3 merge_flat_plate_data.py -case_type komegasst > ${PIPELINE_LOGS}/log.fp_merge_data_komegasst
python3 merge_flat_plate_data.py -case_type komega > ${PIPELINE_LOGS}/log.fp_merge_data_komega
python3 merge_flat_plate_data.py -case_type kepsilonphitf > ${PIPELINE_LOGS}/log.fp_merge_data_kepsilonphitf

