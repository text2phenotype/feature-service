#!/bin/bash

set -e
set -o pipefail

echo "> Starting 'collect-fs-resources.sh' ($(date))"

cd $WORKSPACE/biomed
echo "> Working directory: $(pwd)"

### Python Sanity Check
echo "> Using Python3..."
which python3

echo "> These Python versions should match!"
python3 --version
python --version

echo "> Upgrading virtualenv PIP..."
python3 -m pip install -U pip

echo "> Using PIP:"
which pip

echo "> These PIP versions should match!"
pip --version
pip3 --version
### Python Sanity Check

echo "> Installing DVC"
pip install dvc[s3]

echo "> DVC Pull"
time python3 -m dvc pull -j9 -v

# Build Docker Image with FS resources
cd ${WORKSPACE}/feature-service
echo "> Working directory: $(pwd)"

DOCKERFILE_NAME="Dockerfile.collect-fs-resources"
DOCKER_IMAGE_TARGET="docker.text2phenotype.com/fs-resources:dev_latest"

# Create Dockerfile
cat > "${DOCKERFILE_NAME}" <<EOF
FROM alpine:latest

RUN apk add rsync

COPY ./resources /app/shared-content/feature-service/resources
EOF

time docker build . \
    -f "${DOCKERFILE_NAME}" \
    -t "${DOCKER_IMAGE_TARGET}"

time docker push "${DOCKER_IMAGE_TARGET}"

echo "> Finished 'collect-fs-resources.sh' ($(date))"
