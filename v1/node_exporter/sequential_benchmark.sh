#!/bin/bash

#wrk -t1 -d60s http://localhost:9100
wrk -t1 -d5s http://localhost:9100
