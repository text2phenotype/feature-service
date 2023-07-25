import asyncio
import connexion
import uuid

from feature_service.jobs.feature_service_job import FeatureServiceJob
from feature_service.jobs.job_metadata import JobMetadata

from text2phenotype.apiclients.feature_service import FeatureRequest
from text2phenotype.common.log import operations_logger
from text2phenotype.constants.environment import Environment
from text2phenotype.services.queue.drivers.rmq_updated import RMQBasicPublisher


def __get_request(feature_request: FeatureRequest = None):
    if connexion.request.is_json:
        req = FeatureRequest.from_dict(connexion.request.get_json())
    else:
        req = FeatureRequest.from_dict(feature_request)

    if 'job_id' not in req.metadata:
        req.metadata['job_id'] = req.tid if req.tid else str(uuid.uuid1())

    return req


def annotate_label(feature_request: FeatureRequest = None):
    req = __get_request(feature_request)

    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        operations_logger.info("CREATING LOOP")
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    future_val = asyncio.ensure_future(annotate_label_helper(req.metadata))
    loop.run_until_complete(future_val)

    return req.metadata['job_id']


async def annotate_label_helper(metadata):
    FeatureServiceJob(**metadata)


def annotate_label_task(feature_request: FeatureRequest = None):
    req = __get_request(feature_request)

    operations_logger.info(f'Request with tid {req.metadata["job_id"]} received')
    queue_client = RMQBasicPublisher(queue_name=Environment.LABEL_TASKS_QUEUE.value,
                                     client_tag='annotate_label_task controller')
    queue_client.publish_message(req.metadata)

    return req.metadata['job_id']
