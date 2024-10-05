#!/bin/bash
# post stats to PVOutput.org every 5 minutes

# 5m interval
delay=300

let s=$(date +%s)
# PVOutput rounds to the nearest 5m, so begin with a delay to sync to 5m
let next=$((s + delay - s%delay))

while true; do
    let delta=$next-$(date +%s)
    echo "sleeping $delta seconds"
    sleep $delta
    date -Iseconds
    let next+=$delay
done
