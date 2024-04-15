#!/bin/bash

: '
Starts a Django server for testing
This script will
    1. Start a fresh database and backup original
    2. Populate database with test data
    3. Run Django server
    4. Rollback to original DB after server is stopped
'

trap cleanup EXIT

ROOT_DIR="$( cd "$( dirname "$0" )" && pwd )"
TEST_DIR="${ROOT_DIR}/test"

if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    ROOT_DIR="${ROOT_DIR///c/C:}"
    TEST_DIR="${TEST_DIR///c/C:}"
fi

cleanup() {
    # Restore original database if backed up
    if [ -f "${TEST_DIR}/temp.sqlite3" ]; then
        mv "${TEST_DIR}/temp.sqlite3" "${ROOT_DIR}/db.sqlite3"
    fi
}

# Backup original database if exists
if [ -f "${ROOT_DIR}/db.sqlite3" ]; then
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
python "${ROOT_DIR}/manage.py" loaddata "${TEST_DIR}/test_data.json"

# Run test server
redis-server --port 6379 &
celery -A its_backend worker -l info &
python "${ROOT_DIR}/manage.py" runserver
