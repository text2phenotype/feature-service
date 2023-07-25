#!/usr/bin/env bash

set -e
set -o pipefail

# Source the bash.utils
source "${APP_BASE_DIR}/bin/bash.utils"

log.info "> Starting 'docker-test-unit.sh' ($(date))"

### Python Sanity Check
log.info "> Using Python..."
which python
python --version

log.info "> Upgrading PIP..."
python -m pip install -U pip

log.info "> Using PIP:"
which pip

log.info "> Using PIP version:"
pip --version
### Python Sanity Check

log.info "> Starting unit tests..."
python setup.py test -a feature_service/tests/unit/
exit_code=$?

log.info "> Unit tests complete. Exited ('${exit_code}')"
log.info "> Finished 'docker-test-unit.sh' ($(date))"

exit ${exit_code}
