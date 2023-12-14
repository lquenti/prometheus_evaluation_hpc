#!/bin/bash

TARGET_URL="http://localhost:9100"
DURATION=60
CONNECTIONS=(1 10 25 50 100 150 200 300 400 500)
THREADS=(1 2 4 8 16)

for C in "${CONNECTIONS[@]}"
do
  for T in "${THREADS[@]}"
  do
    if [ $C -ge $T ]
    then
      echo "--------------------------------------------------------"
      echo "Running benchmark with $T threads and $C connections for ${DURATION}s"
      wrk -t${T} -c${C} -d${DURATION}s $TARGET_URL
      sleep 2
    fi
  done
done

