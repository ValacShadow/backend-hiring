#!/bin/bash

set -e

# Default exponential backoff values
MAX_RETRIES=5
RETRY_DELAY=5

echo "Starting Celery worker with exponential backoff for retries..."

# Start Celery worker
for ((i=1; i<=MAX_RETRIES; i++)); do
    celery -A vanderval worker -Q worker_1,worker_2,worker_3 --loglevel=info && break
    echo "Celery failed to start. Retry $i/$MAX_RETRIES in $RETRY_DELAY seconds..."
    sleep $((RETRY_DELAY * i))
done

if [ $i -gt $MAX_RETRIES ]; then
    echo "Failed to start Celery worker after $MAX_RETRIES attempts."
    exit 1
fi
