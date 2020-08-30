#! /bin/bash
# Build a docker image
cd ..
docker build -t pyengine/google-cloud-compute .  --no-cache
docker tag pyengine/google-cloud-compute pyengine/google-cloud-compute:1.0
docker tag pyengine/google-cloud-compute spaceone/google-cloud-compute:1.0
