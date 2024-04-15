#!/bin/bash

TEST_DIR="$( cd "$( dirname "$0" )" && pwd )"
ROOT_DIR="$(dirname "$TEST_DIR")"

# 1. Remove previous coverage files if they exist
if [[ -f ${ROOT_DIR}/.coverage ]]; then
    rm ${ROOT_DIR}/.coverage
    echo "Remove coverage data"
fi
if [[ -d ${ROOT_DIR}/htmlcov ]]; then
    rm -rf ${ROOT_DIR}/htmlcov
    echo "Remove coverage HTML report"
fi
if [[ -f ${ROOT_DIR}/coverage.json ]]; then
    rm ${ROOT_DIR}/coverage.json
    echo "Remove coverage JSON report"
fi
coverage erase  # just in case

# 2. Kill Django server if still running
# Get PID listening on port 8000
SERVER_PID=$(lsof -n -i :8000 | grep LISTEN | awk '{print $2}')
if [[ -n $SERVER_PID ]]; then
    kill -SIGINT $SERVER_PID
    SERVER_PID=""
    echo "Killed Django server"
fi
