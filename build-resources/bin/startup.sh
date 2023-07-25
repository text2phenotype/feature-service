#!/usr/bin/env bash

set -e
set -o pipefail

# Source the bash.utils
source "${APP_BASE_DIR}/bin/bash.utils"

log.info "> Starting 'startup.sh' ($(date))"

export PATH="${APP_BASE_DIR}/.local/bin:$PATH"

# Port Nginx will listen on
export NGINX_LISTEN_PORT="${NGINX_LISTEN_PORT:-8080}"

# Downcase the these variables for consistent usage
APP_SERVICE=$( tr '[:upper:]' '[:lower:]' <<<"${APP_SERVICE}" )

### Python Sanity Check
log.info "> Using Python..."
which python
python --version

log.info "> Using PIP:"
which pip

log.info "> Using PIP version:"
pip --version
### Python Sanity Check

log.info "> Starting ${APP_NAME} as service ${APP_SERVICE}..."

case "${APP_SERVICE}" in
  worker-annotate)
    # Startup delay hack for annotation and ctakes
    STARTUP_DELAY=${STARTUP_DELAY:-150}
    log.info "> Startup delay of $STARTUP_DELAY seconds"
    sleep $STARTUP_DELAY
    time python "${APP_BASE_DIR}/feature_service/workers/annotation/start_worker.py"
  ;;

  worker-vectorize)
    time python "${APP_BASE_DIR}/feature_service/workers/vectorization/start_worker.py"
  ;;

  worker-annotate-label)
    time python "${APP_BASE_DIR}/feature_service/workers/annotate_label/start_worker.py"
  ;;

  feature-service-api)
    export GUNICORN_SOCKET_PATH="unix:${APP_BASE_DIR}/feature_service.sock"
    export GUNICORN_WORKER_CLASS="${GUNICORN_WORKER_CLASS:-gthread}"
    # Default threads to 1 or it forces gthreads as the worker class
    export GUNICORN_WORKER_THREADS="${GUNICORN_WORKER_THREADS:-100}"
    export GUNICORN_WORKER_TIMEOUT="${GUNICORN_WORKER_TIMEOUT:-300}"
    export GUNICORN_WORKERS="${GUNICORN_WORKERS:-1}"

    declare nginx_default_conf="/etc/nginx/sites-enabled/default"

    log.info "> Installing nginx proxy config..."
    log.info "GUNICORN_SOCKET_PATH: ${GUNICORN_SOCKET_PATH}"

    j2 "${APP_BASE_DIR}/build-resources/config/nginx-proxy.conf.j2" > "${nginx_default_conf}"
    log.info "> nginx configuration complete."

    log.info "> Starting nginx..."
    /usr/sbin/nginx
    log.info "> Launching guincorn workers..."
    log.info "Worker Class  : ${GUNICORN_WORKER_CLASS}"
    log.info "Worker Timeout: ${GUNICORN_WORKER_TIMEOUT}"
    log.info "Worker Number : ${GUNICORN_WORKERS}"
    if [[ "$GUNICORN_WORKER_CLASS" == "gthread" ]]; then
      log.info "Worker Threads : ${GUNICORN_WORKER_THREADS}"
    fi
    time gunicorn \
      --timeout ${GUNICORN_WORKER_TIMEOUT} \
      --workers ${GUNICORN_WORKERS} \
      --worker-class ${GUNICORN_WORKER_CLASS} \
      --threads ${GUNICORN_WORKER_THREADS} \
      --bind ${GUNICORN_SOCKET_PATH} feature_service.__main__:app

  ;;

  *)
    log.error "> The service name '${APP_SERVICE}' was not recognized. Not starting a service!"
  ;;

esac

log.warn "> ${APP_NAME} as service ${APP_SERVICE} stopped!"

log.info "> Finished 'startup.sh' ($(date))"
