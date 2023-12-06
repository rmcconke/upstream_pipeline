#!/bin/bash

python3 -u ../generic/foam_to_numpy.py \
 -case flatplate -foam_parent_dir ${ML_FOAM_DATASET}/komegasst/fp\
 -data_save_dir ${ML_NUMPY_DATASET}/komegasst/ \
 -case_type komegasst \
 -write_fields_application writeFields_RANS_omega_lean > ${PIPELINE_LOGS}/log.fp_foam_to_numpy_komegasst \
 -dataset_prefix komegasst

python3 -u ../generic/foam_to_numpy.py \
 -case flatplate -foam_parent_dir ${ML_FOAM_DATASET}/komega/fp\
 -data_save_dir ${ML_NUMPY_DATASET}/komega/ \
 -case_type komega \
 -write_fields_application writeFields_RANS_omega_lean > ${PIPELINE_LOGS}/log.fp_foam_to_numpy_komega

python3 -u ../generic/foam_to_numpy.py \
 -case flatplate -foam_parent_dir ${ML_FOAM_DATASET}/kepsilonphitf/fp\
 -data_save_dir ${ML_NUMPY_DATASET}/kepsilonphitf/ \
 -case_type kepsilonphitf \
 -write_fields_application writeFields_RANS_kepsilonphitf_lean > ${PIPELINE_LOGS}/log.fp_foam_to_numpy_kepsilonphitf \
 -dataset_prefix kepsilonphitf

