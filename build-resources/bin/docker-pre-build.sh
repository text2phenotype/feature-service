#!/usr/bin/env bash

set -e
set -o pipefail

# Source the bash.utils
source "${APP_BASE_DIR}/bin/bash.utils"

log.info "> Starting 'docker-pre-build.sh' ($(date))"

log.info "> Starting ${APP_NAME} build..."

### Python Sanity Check
log.info "> Using Python..."
which python
python --version

log.info "> Upgrading PIP..."
python -m pip install -U pip

log.info "> Using PIP:"
which pip

log.info "> Using PIP version..."
pip --version
### Python Sanity Check

log.info "> Installing ${APP_NAME} dependencies..."

apt-get update -y

apt-get install -y \
  nginx \
  gfortran \
  libatlas-base-dev

log.info "> ${APP_NAME} dependency installation complete."

### Cleanup
log.info "> Cleaning up ${APP_NAME} build..."

log.info "> apt-get autoremove"
apt-get autoremove -y

log.info "> apt-get clean"
apt-get clean -y

log.info "> Removing uncleaned apt files in '/var/lib/apt/lists/'"
rm -rf /var/lib/apt/lists/*

log.info "> Remove build files from '${APP_BASE_DIR}/build'"
rm -rf "${APP_BASE_DIR}/build/"

log.info "> ${APP_NAME} build cleanup complete."

log.info "> Finished 'docker-pre-build.sh' ($(date))"
