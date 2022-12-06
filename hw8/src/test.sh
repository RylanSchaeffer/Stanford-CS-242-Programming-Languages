#!/bin/bash

for i in {01..11}; do
    ii=$(printf "%02d" $i)
    echo "lean prob${ii}.lean --trust=0"
    lean prob${ii}.lean --trust=0
done
