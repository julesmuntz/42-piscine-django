#!/bin/bash

if [[ $1 =~ ^(https?:\/\/)?(www\.)?bit\.ly ]]; then
    curl -s $1 | grep -o 'href="[^"]*"' | cut -d'"' -f2
else
    echo "The input is not a bit.ly URL."
fi
