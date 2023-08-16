#!/bin/bash

python3 -u ../generic/foam_to_numpy.py \
 -case flatplate -foam_parent_dir ${ML_FOAM_DATASET}/komegasst/\
 -data_save_dir ${ML_NUMPY_DATASET}/komegasst/ \
 -case_type komegasst \
 -write_fields_application writeFields_RANS > ${PIPELINE_LOGS}/log.fp_foam_to_numpy

