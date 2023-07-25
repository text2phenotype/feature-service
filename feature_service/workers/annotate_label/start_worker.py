from feature_service.feature_service_env import FeatureServiceEnv
from feature_service.workers.annotate_label.worker import AnnotateLabelTaskWorker


if __name__ == '__main__':
    worker = AnnotateLabelTaskWorker()
    FeatureServiceEnv.APPLICATION_NAME.value = f'Feature Service - {worker.NAME}'

    worker.start()
