from feature_service.feature_service_env import FeatureServiceEnv
from feature_service.workers.annotation.worker import AnnotateTaskWorker


if __name__ == '__main__':
    worker = AnnotateTaskWorker()
    FeatureServiceEnv.APPLICATION_NAME.value = f'Feature Service - {worker.NAME}'

    worker.start()
