#!/bin/bash

wrk -t1 -d60s http://localhost:9100
