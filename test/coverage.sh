#!/bin/bash

trap cleanup EXIT

TEST_DIR="$( cd "$( dirname "$0" )" && pwd )"
ROOT_DIR="$(dirname "$TEST_DIR")"
POSTMAN_COLLECTION="ITS-API-Test.postman_collection.json"
DJANGO_PID=""
NEWMAN_PID=""
REDIS_PID=""
CELERY_PID=""

if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    ROOT_DIR="${ROOT_DIR///c/C:}"
    TEST_DIR="${TEST_DIR///c/C:}"
fi

cleanup() {
    # Restore original database if backed up
    if [[ -f ${TEST_DIR}/temp.sqlite3 ]]; then
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

    # Kill newman test if running
    if kill -0 "$NEWMAN_PID" 2> /dev/null; then
        kill "$NEWMAN_PID"
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
python manage.py loaddata "${TEST_DIR}/test_data.json"

newman_test() {
    # Wait for server startup
    sleep 10

    # Run postman tests
    newman run "${TEST_DIR}/${POSTMAN_COLLECTION}"

    # Get PID listening on port 8000
    DJANGO_PID=$(lsof -n -i :8000 | grep LISTEN | awk '{print $2}')

    # Kill server if still running
    if [[ -n $DJANGO_PID ]]; then
        kill -INT $DJANGO_PID
        DJANGO_PID=""
    fi

    # Wait for server to end
    sleep 1
}
newman_test &
NEWMAN_PID=$!

# Run development server in background with coverage.py
redis-server --port 6379 &
REDIS_PID=$!
celery -A its_backend worker -l info &
CELERY_PID=$!
coverage run --branch ${ROOT_DIR}/manage.py runserver --noreload

# Generate report only for models.py and views.py
FILES="${ROOT_DIR}/its_backend/apps/**/models.py","${ROOT_DIR}/its_backend/apps/**/views.py","${ROOT_DIR}/its_backend/apps/submissions/its_utils.py","${ROOT_DIR}/its_backend/apps/submissions/utils.py"
coverage html --include=$FILES
coverage json --include=$FILES
coverage report --include=$FILES
