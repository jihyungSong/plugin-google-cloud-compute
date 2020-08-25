#! /bin/bash
# Build a docker image
cd ..
docker build -t pyengine/googlecloud-compute .
docker tag pyengine/googlecloud-compute pyengine/googlecloud-compute:1.0
docker tag pyengine/googlecloud-compute spaceone/googlecloud-compute:1.0
