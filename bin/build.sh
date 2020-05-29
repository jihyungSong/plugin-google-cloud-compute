#! /bin/bash
# Build a docker image
cd ..
docker build -t pyengine/gcp-compute .
docker tag pyengine/gcp-compute pyengine/gcp-compute:1.0
docker tag pyengine/gcp-compute spaceone/gcp-compute:1.0
