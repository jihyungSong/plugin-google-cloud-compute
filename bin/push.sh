#!/usr/bin/env bash
# How to upload
./build.sh
docker push pyengine/googlecloud-compute:1.0
docker push spaceone/googlecloud-compute:1.0
