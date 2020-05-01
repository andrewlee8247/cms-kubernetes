#!/usr/bin/env bash

# Activate service account and set environment variables
gcloud auth activate-service-account --key-file=healthcare-predictions-85c2b5783a5e.json
gcloud config set project healthcare-predictions
gcloud config set compute/zone us-central1-b
export GOOGLE_APPLICATION_CREDENTIALS=healthcare-predictions-85c2b5783a5e.json

# Run api
python api.py