#!/bin/bash
cd "$(dirname "$0")"
#sh run.sh 2>&1 | tee "log/$(date +%Y-%m-%d_%H-%M).txt"
sh run.sh
