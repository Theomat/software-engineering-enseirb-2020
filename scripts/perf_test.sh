#!/bin/bash

echo "Running performance tests !"

locust -f perf_test.py –H http://127.0.0.1:8000
