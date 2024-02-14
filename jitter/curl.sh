#!/bin/bash

# in seconds
INTERVAL=3

while true; do
    START=$(date +%s)
    curl "172.19.205.29:24343/metrics"
    END=$(date +%s)

    DURATION=$(( END - START ))
    SLEEPTIME=$(( INTERVAL - DURATION ))
    if [ $SLEEPTIME -gt 0 ]; then
        sleep $SLEEPTIME
    fi
done

