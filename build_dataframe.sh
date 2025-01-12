#!/bin/bash
#export PYTHONPATH=${PWD}
source ../dataenv/bin/activate
. env_setup.sh
echo building dataframe
python3 -u build_dataframe.py

