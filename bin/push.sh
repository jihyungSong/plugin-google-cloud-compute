#!/usr/bin/env bash
# How to upload
./build.sh
docker push pyengine/gcp-compute:1.0
docker push spaceone/gcp-compute:1.0
