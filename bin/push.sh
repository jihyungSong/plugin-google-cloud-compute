#!/usr/bin/env bash
# How to upload
./build.sh
docker push pyengine/google-cloud-compute:1.0
docker push spaceone/google-cloud-compute:1.0
