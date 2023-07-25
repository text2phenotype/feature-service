from feature_service.feature_service_env import FeatureServiceEnv
from feature_service.workers.vectorization.worker import VectorizeTaskWorker


if __name__ == '__main__':
    worker = VectorizeTaskWorker()
    FeatureServiceEnv.APPLICATION_NAME.value = f'Feature Service - {worker.NAME}'

    worker.start()
