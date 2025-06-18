#!/bin/bash
# Start the Python API using gunicorn, binding to the PORT environment variable provided by Deta
gunicorn app:app --bind 0.0.0.0:$PORT