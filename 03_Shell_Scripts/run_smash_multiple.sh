#!/bin/bash

# Define number of total runs
TOTAL_RUNS=2

for i in {1..$(TOTAL_RUNS)}
    do
        run_smash_basic.sh -i
    done
