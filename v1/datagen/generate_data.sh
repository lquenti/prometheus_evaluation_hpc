#!/bin/bash

# Depends on tsbs_generate_data 
# https://github.com/timescale/tsbs

PATH_TO_TSBS_GEN="$HOME/pkgs/tsbs/bin/tsbs_generate_data"

# For documentation, see
# https://github.com/timescale/tsbs#data-generation
$PATH_TO_TSBS_GEN --use-case="iot" --seed=123 --scale=10\
    --timestamp-start="2016-01-01T00:00:00Z" \
    --timestamp-end="2016-01-01T00:01:00Z" \
    --log-interval="10s" --format="influx" > influxql_data.iql
