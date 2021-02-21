#!/bin/bash

echo "Enter host name:"
read HOST_NAME
echo "Enter number of processors:"
read NUM_PROCS
echo "Enter executable:"
read EXE

echo "Submitting $EXE to run on $NUM_PROCS processors on $HOST_NAME"
