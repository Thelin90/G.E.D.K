#!/usr/bin/env bash
pip install --trusted-host pypi.python.org -r scripts/requirements.txt
spark-submit src/etl.py