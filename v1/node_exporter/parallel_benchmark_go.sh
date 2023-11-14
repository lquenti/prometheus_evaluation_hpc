#!/bin/bash

TARGET_URL="http://localhost:9100"
DURATION=20
STEPS=(25 50 100 200 300 400 500 600 700 800 900 1000)

for CONCURRENCY in "${STEPS[@]}"
do
    echo "--------------------------------------------------------"
    echo "Running benchmark with $CONCURRENCY goroutines for $DURATION seconds"
    go-wrk -c $CONCURRENCY -d $DURATION $TARGET_URL
    sleep 2
done

