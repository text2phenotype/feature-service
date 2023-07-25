from collections import defaultdict
import concurrent
import math
import time
from concurrent.futures import (
    as_completed,
    ThreadPoolExecutor,
)
from typing import (
    List,
    Optional,
    Set,
)
import requests

from feature_service.nlp.autocode import _expand_ctakes_response, ensure_compatible_response
from feature_service.feature_service_env import FeatureServiceEnv
from feature_service.feature_set.factory import FEATURE_MAP, get_annotation_features
from text2phenotype.apiclients.fdl_client import FDLClient
from text2phenotype.apm.metrics import text2phenotype_capture_text_info
from text2phenotype.common import speech
from text2phenotype.common.featureset_annotations import MachineAnnotation
from text2phenotype.common.log import operations_logger
from text2phenotype.concurrency import (
    AbstractWorker,
    SimpleQueue,
)

from text2phenotype.constants.features import FeatureType
from ..features.feature import Feature

class AnnWorker(AbstractWorker):
    def __init__(self,
                 queue: SimpleQueue,
                 tid: str,
                 text: str,
                 annotations: MachineAnnotation):

        super().__init__(queue, tid)
        self.tid = tid
        self.text = text
        self.annotations = annotations
        self.token_ranges = annotations.range_to_token_idx_list

    def run(self):
        while True:
            msg = self.queue.get()

            if self.is_close_message(msg):
                break

            try:
                feature: Feature = FEATURE_MAP[msg]()

                operations_logger.debug(f'Beginning annotation for feature: {feature.feature_type}', tid=self.tid)
                individual_feature_annotations = feature.annotate(self.text, tid=self.tid)
                operations_logger.debug(f'Annotations for feature type: {feature.feature_type} '
                                        f'completed, beginning aggregation',
                                        tid=self.tid)
                aggregated_annotations = feature.aggregate(
                    individual_feature_annotations,
                    len(self.annotations),
                    self.token_ranges,
                )
                self.annotations.add_item(feature.feature_type, aggregated_annotations)

            except Exception as err:
                operations_logger.exception(f'An exception occured during annotation '
                                            f'for feature "{feature.feature_type.name}"')
                self.errors.append(err)



def run_thread_list(thread_list, tid: str = None):
    with ThreadPoolExecutor(FeatureServiceEnv.FEAT_MAX_THREAD_COUNT.value) as executor:
        futures = []
        for thread in thread_list:
            futures.append(executor.submit(thread.run))
        for future in as_completed(futures):
            future.result()


def delete_annotations(tokens: List[dict], feature_types: Set[FeatureType]):
    for i in range(len(tokens)):
        for feature in feature_types:
            tokens[i].pop(feature.name, None)


def check_ctakes():
    if FeatureServiceEnv.FEAT_LOCAL_CTAKES.value:
        ctakes_host_name = FeatureServiceEnv.UMLS_HOST.value
        if ctakes_host_name.endswith('rest'):
            ctakes_host_name = ctakes_host_name[:-4]

        attempt = 1
        max_attempts = 10
        while True:
            try:
                ctakes_response = requests.get(f'{ctakes_host_name}/health/ready')
                ctakes_response.raise_for_status()
            except requests.exceptions.RequestException as err:
                operations_logger.debug(f'Request exception: {err}')
            else:
                operations_logger.info('CTAKES service is ready')
                break

            if attempt >= max_attempts:
                operations_logger.error('Exceeded the maximum number of CTAKES checks attempts. Worker STOPPED')
                raise SystemExit('CTAKES service is not ready. Worker STOPPED')

            sleep_time = attempt ** 2
            operations_logger.error(f'CAKES service is not ready. '
                                    f'Next check after {sleep_time} seconds delay')
            time.sleep(sleep_time)
            attempt += 1
    return


def build_worker_pool(queue: SimpleQueue,
                      tid: str,
                      text: str,
                      annotations: MachineAnnotation,
                      size: Optional[int] = None) -> List[AbstractWorker]:
    if size is None:
        size = int(FeatureServiceEnv.FEAT_MAX_THREAD_COUNT.value)
    workers = []
    for _ in range(size):
        worker = AnnWorker(queue, tid, text, annotations)
        worker.start()
        workers.append(worker)
    return workers



def annotate_text(text: str,
                  feature_types: Set[FeatureType] = None,
                  tid: str = None,
                  max_token_size: int = math.inf,
                  fdl_data: Optional[dict] = None) -> MachineAnnotation:
    """
    annotate plain text with various annotation pipelines
    :return: a list of annotated token dictionaries
    """
    # SPEECH
    operations_logger.debug('Beginning Annotation Task', tid=tid)
    tokens = speech.tokenize(text, tid=tid)  # now a list of token dictionary
    if not tokens:
        return MachineAnnotation()

    text2phenotype_capture_text_info(text_length=len(text), token_count=len(tokens), tid=tid)

    machine_annotation = MachineAnnotation(tokenization_output=tokens, text_len=len(text))
    operations_logger.info(f'Tokenization Complete for annotation Task, Number of tokens = {len(tokens)}, '
                           f'Beginning Feature Annotations', tid=tid)

    return add_annotations(text,
                           machine_annotation,
                           feature_types,
                           tid=tid,
                           max_token_size=max_token_size,
                           fdl_data=fdl_data)


def add_annotations(text: str,
                    machine_annotation: MachineAnnotation,
                    feature_types: Set[FeatureType] = None,
                    tid: str = None,
                    max_token_size: int = math.inf,
                    fdl_data: Optional[dict] = None) -> MachineAnnotation:

    if len(machine_annotation) > max_token_size:
        operations_logger.error(f"Number of file tokens {len(machine_annotation)} > max_token count {max_token_size}")
        raise ValueError(f"Number of file tokens {len(machine_annotation)} > max_token count {max_token_size}")

    features: List = [FEATURE_MAP[feature.feature_type]() for feature in get_annotation_features(feature_types) if
                      feature.requires_annotation]

    if FeatureServiceEnv.FDL_ENABLED.value:
        # In the pipeline FDL stuff must be performed independently in the FDL Worker,
        # and Annotate worker should pass "fdl_data" downloaded from the S3 storage.
        if fdl_data is None:
            operations_logger.warning("'fdl_data' was not passed, "
                                      "calling process_data() via FDL API instead")
            fdl_data = FDLClient(FeatureServiceEnv.FDL_API_URL.value).process_data(text)

        grouped_features = defaultdict(list)
        for fa in features:
            grouped_features[fa.config_name].append(fa)

        for config_name, config_features in grouped_features.items():
            if config_name:
                data = fdl_data.get(config_name.value)
                if data:
                    data = ensure_compatible_response(data)
                    data = _expand_ctakes_response(data)
            else:
                data = None

            for fa in config_features:
                individual_feature_annotations = fa.annotate(text, fdl_data=data, tid=tid)
                aggregated_annotations = fa.aggregate(
                    individual_feature_annotations,
                    len(machine_annotation),
                    machine_annotation.range_to_token_idx_list,
                )
                machine_annotation.add_item(fa.feature_type, aggregated_annotations)

            # done processing data, so clear it from memory
            if config_name and config_name.value in fdl_data:
                del fdl_data[config_name.value]
    else:
        operations_logger.warning(
            f'FDL service is not enabled in this environment, '
            f'{FeatureServiceEnv.FDL_ENABLED.name} = {FeatureServiceEnv.FDL_ENABLED.value},  '
            f'the text will be processed via CTAKES.')

        # cTakes version
        check_ctakes()
        with ThreadPoolExecutor(FeatureServiceEnv.FEAT_MAX_THREAD_COUNT.value) as executor:
            future_to_feature = {executor.submit(fa.annotate, text, tid=tid): fa for fa in features}
            for future in concurrent.futures.as_completed(future_to_feature):
                feature = future_to_feature[future]
                try:
                    individual_feature_annotations = future.result()
                except Exception as exc:
                    operations_logger.exception(f'Failed annotation for the feature {feature.__class__.__name__}, {exc}')
                    continue

                aggregated_annotations = feature.aggregate(
                    individual_feature_annotations,
                    len(machine_annotation),
                    machine_annotation.range_to_token_idx_list,
                )
                machine_annotation.add_item(feature.feature_type, aggregated_annotations)

    operations_logger.debug(f'Annotations Completed Successfully', tid=tid)

    return machine_annotation
