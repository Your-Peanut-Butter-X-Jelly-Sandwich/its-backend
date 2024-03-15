#!/bin/bash

set -e  # Exit immediately if a command exits with a non-zero status
trap cleanup EXIT

TEST_DIR="$( cd "$( dirname "$0" )" && pwd )"
ROOT_DIR="$(dirname "$TEST_DIR")"
SERVER_PID=""

POSTMAN_COLLECTION="ITS-API-Test.postman_collection.json"

cleanup() {
    # Restore original database if backed up
    if [ -f "${TEST_DIR}/temp.sqlite3" ]; then
        mv "${TEST_DIR}/temp.sqlite3" "${ROOT_DIR}/db.sqlite3"
    fi

    # Kill server if running
    if [ -n "$SERVER_PID" ]; then
        kill "$SERVER_PID"
    fi
}

# Backup original database if exists
if [ -f "${ROOT_DIR}/db.sqlite3" ]; then
    mv "${ROOT_DIR}/db.sqlite3" "${TEST_DIR}/temp.sqlite3"
fi

# Make and apply migrations
python "${ROOT_DIR}/manage.py" makemigrations
python "${ROOT_DIR}/manage.py" migrate

# Populate database with test data
sqlite3 "${ROOT_DIR}/db.sqlite3" ".read ${TEST_DIR}/populate_db.sql"

# Run development server in background and save PID
python "${ROOT_DIR}/manage.py" runserver &
SERVER_PID=$!

# Wait for server startup
sleep 5

# Run postman tests
newman run "${TEST_DIR}/${POSTMAN_COLLECTION}"
