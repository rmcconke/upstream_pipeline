#!/bin/bash
#export PYTHONPATH=${PWD}
source ../dataenv/bin/activate
. env_setup.sh
#echo phll pipeline
#(cd upstream_pipeline/phll/ ; sh phll_pipeline.sh)
#echo fp pipeline
#(cd upstream_pipeline/fp/ ; sh fp_pipeline.sh)
echo duct pipeline
(cd upstream_pipeline/duct/ ; sh duct_pipeline.sh)

