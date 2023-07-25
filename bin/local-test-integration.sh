#!/bin/bash

set -e
set -o pipefail

echo "> Starting 'local-test-integration.sh' ($(date))"

if [[ -n $SKIP_TESTS || -n $SKIP_INT_TESTS ]]; then
  echo "> Not running integration tests..."
  exit 0
fi

# ENV
export BIOMED_PRELOAD=False
export MDL_BIOM_DATA_ROOT="$CI_PROJECT_DIR"
export MDL_BIOM_PRELOAD=False
export MDL_COMN_BIOMED_API_BASE=http://0.0.0.0:8080
export MDL_COMN_DATA_ROOT="$CI_PROJECT_DIR"
export MDL_COMN_STORAGE_CONTAINER_NAME=biomed-data
export MDL_COMN_USE_STORAGE_SVC=True
export MDL_FEAT_API_BASE=http://0.0.0.0:8081
export MDL_FEAT_UMLS_REQUEST_MODE=false

echo ">> Downloading EMR test records via S3..."
# aws s3 sync --no-progress --only-show-errors s3://biomed-data/emr "$CI_PROJECT_DIR/emr"
# aws s3 sync --no-progress --only-show-errors s3://biomed-data/himss "$CI_PROJECT_DIR/himss"
aws s3 sync s3://${MDL_COMN_STORAGE_CONTAINER_NAME}/emr "$CI_PROJECT_DIR/emr"
aws s3 sync s3://${MDL_COMN_STORAGE_CONTAINER_NAME}/himss "$CI_PROJECT_DIR/himss"

echo "> Moving into '${CI_PROJECT_DIR}'"
cd "$CI_PROJECT_DIR"
echo "> Working directory: $(pwd)"

### Python Sanity Check
echo "> Using Python3..."
which python3
python3 --version

echo "> Creating Python3 virtualenv with that version"
python3 -m virtualenv venv
source venv/bin/activate

echo "> Upgrading virtualenv PIP..."
venv/bin/python -m pip install -U pip

echo "> Using virtualenv Python:"
which python

echo "> These Python versions should match!"
python --version
venv/bin/python --version

echo "> Using virtualenv PIP:"
which pip

echo "> These PIP versions should match!"
pip --version
venv/bin/pip --version
### Python Sanity Check

echo "> Installing DVC"
pip install dvc[s3]

echo "> Pulling DVC data"
time dvc pull -f -j 9 -v

echo "> Installing text2phenotype-py"
pip install ../text2phenotype-py
pip install .

echo "> Starting integration tests"
python nltk_download.py
python -m pytest feature_service/tests/integration/ --junitxml="${INTEGRATION_TESTS_REPORT_FILE:-junit-report-integration.xml}"

echo "> Finshed 'local-test-integration.sh' ($(date))"
