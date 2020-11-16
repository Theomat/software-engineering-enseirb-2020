#!/bin/bash

echo "Running performance tests !"

~/go/bin/bombardier -c 100 -r 2000 -d 30s -l http://127.0.0.1:8000/api/intent?sentence=trouve%20des%20toilette
