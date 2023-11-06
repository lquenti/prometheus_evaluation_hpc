#!/bin/bash

mkdir -p ./tmp/prom
singularity run --bind ./tmp/prom:/tsdb/prometheus-2.45.1.linux-amd64/data/ singularity_*
