#!/bin/bash

set -e
set -o pipefail

echo "> Starting 'local-test-unit.sh' ($(date))"

if [[ -n $SKIP_TESTS || -n $SKIP_UNIT_TESTS ]]; then
  echo "> Not running unit tests..."
  exit 0
fi

echo "> Working directory: $(pwd)"

### Python Sanity Check
echo "> Using Python3..."
which python3
python3 --version

echo "> Creating Python3 virtualenv with that version"
python3 -m virtualenv venv
source venv/bin/activate

echo "> Using virtualenv Python:"
which python

echo "> These Python versions should match!"
python --version
venv/bin/python --version

echo "> Upgrading virtualenv PIP..."
python -m pip install -U pip

echo "> Using virtualenv PIP:"
which pip

echo "> These PIP versions should match!"
pip --version
venv/bin/pip --version
### Python Sanity Check

echo "> Installing DVC"
pip install dvc[s3]

echo "> DVC Pull"
time dvc pull -f -j 9 -v

echo "> Installing text2phenotype-py"
pip install -e ../text2phenotype-py
pip install .

echo "> Starting Feature Service unit tests..."
python nltk_download.py
python -m pytest feature_service/tests/unit/ --junitxml="${UNIT_TESTS_REPORT_FILE:-junit-report.xml}"

echo "> Finished 'local-test-unit.sh' ($(date))"
