#!/bin/bash
#export PYTHONPATH=${PWD}
source ../dataenv/bin/activate
. env_setup.sh
echo fp pipeline
(cd upstream_pipeline/fp/ ; sh fp_pipeline.sh)
#echo cbfs_cndv_bump pipeline
#(cd upstream_pipeline/cbfs_cndv_bump/ ; sh cbfs_cndv_bump_pipeline.sh)
#echo phll pipeline
#(cd upstream_pipeline/phll/ ; sh phll_pipeline.sh)
#echo duct pipeline
#(cd upstream_pipeline/duct/ ; sh duct_pipeline.sh)

