#!/bin/bash

for i in `cat MVSSRC.jay.datasets.txt`; do
       echo "Getting $i"
       lftp -u herc01,cul8tr -e "mirror -v --ascii $i ./$i; bye" localhost:21021
done       
