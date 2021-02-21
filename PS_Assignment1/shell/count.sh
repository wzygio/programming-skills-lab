#!/bin/bash 
COUNT=1
while [  $COUNT -lt 1000000000 ]; do
    sleep 1
    echo $COUNT
    let COUNT=COUNT+1 
done
