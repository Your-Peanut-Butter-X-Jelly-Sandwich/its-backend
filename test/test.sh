#!/bin/bash

set -e  # Exit immediately if a command exits with a non-zero status
trap cleanup EXIT

TEST_DIR="$( cd "$( dirname "$0" )" && pwd )"
ROOT_DIR="$(dirname "$TEST_DIR")"
DJANGO_PID=""
REDIS_PID=""
CELERY_PID=""
POSTMAN_COLLECTION="ITS-API-Test.postman_collection.json"

if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    ROOT_DIR="${ROOT_DIR///c/C:}"
    TEST_DIR="${TEST_DIR///c/C:}"
fi

cleanup() {
    # Restore original database if backed up
    if [ -f "${TEST_DIR}/temp.sqlite3" ]; then
        mv "${TEST_DIR}/temp.sqlite3" "${ROOT_DIR}/db.sqlite3"
    fi


    # Kill servers if running
    if kill -0 "$REDIS_PID" 2> /dev/null; then
        kill "$REDIS_PID"
    fi
    if kill -0 "$CELERY_PID" 2> /dev/null; then
        kill "$CELERY_PID"
    fi
    if kill -0 "$DJANGO_PID" 2> /dev/null; then
        kill "$DJANGO_PID"
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

# Run development server in background and save PID
redis-server --port 6379 &
REDIS_PID=$!
celery -A its_backend worker -l info &
CELERY_PID=$!
python "${ROOT_DIR}/manage.py" runserver &
DJANGO_PID=$!

# Wait for server startup
sleep 5

# Run postman tests
newman run "${TEST_DIR}/${POSTMAN_COLLECTION}"

# Run tests for utils.py and its_utils under submission app
python "${ROOT_DIR}/manage.py" test its_backend.apps.submissions
