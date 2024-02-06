#!/bin/bash

wrk -t1 -d60s http://localhost:24343/metrics
