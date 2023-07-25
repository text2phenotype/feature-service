import os

from text2phenotype.constants.environment import (
    Environment,
    EnvironmentVariable,
)


class FeatureServiceEnv(Environment):
    APPLICATION_NAME = Environment.APPLICATION_NAME
    APPLICATION_NAME.value = 'Feature Service'

    # UMLS/CTAKES/NLP
    FEAT_LOCAL_CTAKES = EnvironmentVariable(name='MDL_FEAT_LOCAL_CTAKES', value=False)
    UMLS_HOST = EnvironmentVariable(name='MDL_FEAT_UMLS_HOST', legacy_name='NLP_HOST', value='https://ctakes-dev-nlp-ci.mdl-dev.in/nlp/rest')
    UMLS_REQUEST_MODE = EnvironmentVariable(name='MDL_FEAT_UMLS_REQUEST_MODE',
                                            legacy_name='UMLS_REQUEST_MODE',
                                            value=False)
    NLP_CACHE = EnvironmentVariable(name='MDL_FEAT_NLP_CACHE', legacy_name='NLP_CACHE', value='.nlp_cache')
    NLP_CACHE_ENABLE = EnvironmentVariable(name='MDL_FEAT_NLP_CACHE_ENABLE',
                                           legacy_name='NLP_CACHE_ENABLE',
                                           value=False)
    NLP_USERNAME = EnvironmentVariable(name='MDL_FEAT_NLP_USERNAME', legacy_name='NLP_USERNAME')
    NLP_PASSWORD = EnvironmentVariable(name='MDL_FEAT_NLP_PASSWORD', legacy_name='NLP_PASSWORD')
    NLP_MAX_RETRIES = EnvironmentVariable(name='MDL_FEAT_ANNOTATE_ENDPOINT_RETRY ', value=3)
    NLP_HOST_MAX_TOKENS = EnvironmentVariable(name='MDL_FEAT_MAX_UMLS_TOKENS', value=10000)

    # NPI
    NPI_HOST = EnvironmentVariable(name='MDL_FEAT_NPI_HOST', legacy_name='NPI_HOST',
                                   value='https://ctakes-dev-nlp-ci.mdl-dev.in/npi/rest')

    # Feature Service
    SVC_HOST = EnvironmentVariable(name='MDL_FEAT_SVC_HOST', legacy_name='FEATURE_SERVICE_HOST', value='0.0.0.0')
    SVC_PORT = EnvironmentVariable(name='MDL_FEAT_SVC_PORT', legacy_name='FEATURE_SERVICE_PORT', value=8081)
    PRELOAD = EnvironmentVariable(name='MDL_FEAT_PRELOAD', legacy_name='PRELOAD_FEATURE_DATA', value=True)

    # APM
    APM_SERVICE_NAME = EnvironmentVariable(name='MDL_FEAT_APM_SERVICE_NAME',
                                           legacy_name='APM_SERVICE_NAME',
                                           value='Text2phenotype Feature Service')
    FEAT_MAX_THREAD_COUNT = EnvironmentVariable(name='MDL_FEAT_MAX_THREAD_COUNT', value=8)

    FDL_API_URL = EnvironmentVariable(name='MDL_FDL_API_URL', value='https://fdl-dev-nlp-ci.mdl-dev.in')

    MODELS_PATH = EnvironmentVariable(name='MDL_FEAT_MODELS_ROOT', value=os.path.dirname(__file__))
