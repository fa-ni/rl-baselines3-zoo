#!/bin/bash
# For Execution under Linux we need to use python3 instead of python
source ../../venv/Scripts/activate
max=100
for (( i=1; i <= max; ++i ))
do
    python main.py --round_number "$i"
    python main_py4j.py --round_number "$i"
    python main_pyjnius.py --round_number "$i"
done
