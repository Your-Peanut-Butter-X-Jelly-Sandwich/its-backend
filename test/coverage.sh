#!/bin/bash

trap cleanup EXIT

TEST_DIR="$( cd "$( dirname "$0" )" && pwd )"
ROOT_DIR="$(dirname "$TEST_DIR")"
POSTMAN_COLLECTION="ITS-API-Test.postman_collection.json"
SERVER_PID=""
NEWMAN_PID=""

if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    ROOT_DIR="${ROOT_DIR///c/C:}"
    TEST_DIR="${TEST_DIR///c/C:}"
fi

cleanup() {
    # Restore original database if backed up
    if [[ -f ${TEST_DIR}/temp.sqlite3 ]]; then
        mv "${TEST_DIR}/temp.sqlite3" "${ROOT_DIR}/db.sqlite3"
    fi

    # Kill server if running
    if [[ -n $SERVER_PID ]]; then
        kill $SERVER_PID
    fi

    # Kill newman test if running
    if [[ -n $NEWMAN_PID ]]; then
        kill $NEWMAN_PID
    fi
}

# cd into ROOT_DIR to run coverage.py in ROOT_DIR
cd ${ROOT_DIR}

# Remove previous coverage files if they exist
if [[ -d ${ROOT_DIR}/htmlcov ]]; then
    rm -rf ${ROOT_DIR}/htmlcov
fi
if [[ -f ${ROOT_DIR}/coverage.json ]]; then
    rm ${ROOT_DIR}/coverage.json
fi
if [[ -f ${ROOT_DIR}/.coverage ]]; then
    rm ${ROOT_DIR}/.coverage
fi
coverage erase  # just in case

# Backup original database if exists
if [[ -f ${ROOT_DIR}/db.sqlite3 ]]; then
    mv "${ROOT_DIR}/db.sqlite3" "${TEST_DIR}/temp.sqlite3"
fi

# Make and apply migrations
python "${ROOT_DIR}/manage.py" makemigrations
python "${ROOT_DIR}/manage.py" migrate

if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    python "${ROOT_DIR}/manage.py" makemigrations submissions
    python "${ROOT_DIR}/manage.py" migrate submissions

    python "${ROOT_DIR}/manage.py" makemigrations questions
    python "${ROOT_DIR}/manage.py" migrate questions

    python "${ROOT_DIR}/manage.py" makemigrations accounts
    python "${ROOT_DIR}/manage.py" migrate accounts
fi

# Populate database with test data
sqlite3 "${ROOT_DIR}/db.sqlite3" ".read ${TEST_DIR}/populate_db.sql"

newman_test() {
    # Wait for server startup
    sleep 5

    # Run postman tests
    newman run "${TEST_DIR}/${POSTMAN_COLLECTION}"

    # Get PID listening on port 8000
    SERVER_PID=$(lsof -n -i :8000 | grep LISTEN | awk '{print $2}')

    # Kill server if still running
    if [[ -n $SERVER_PID ]]; then
        kill -SIGINT $SERVER_PID
        SERVER_PID=""
    fi

    # Wait for server to end
    sleep 1
}
newman_test &
NEWMAN_PID=$!

# Run development server in background with coverage.py
coverage run --branch ${ROOT_DIR}/manage.py runserver --noreload

# Generate report only for models.py and views.py
coverage html --include="${ROOT_DIR}/its_backend/apps/**/models.py","${ROOT_DIR}/its_backend/apps/**/views.py"
coverage json --include="${ROOT_DIR}/its_backend/apps/**/models.py","${ROOT_DIR}/its_backend/apps/**/views.py"
coverage report --include="${ROOT_DIR}/its_backend/apps/**/models.py","${ROOT_DIR}/its_backend/apps/**/views.py"
