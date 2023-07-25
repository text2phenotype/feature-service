import requests

from text2phenotype.common.version_info import get_version_info
from text2phenotype.common.status import StatusReport, Component, Status

from feature_service.feature_service_env import FeatureServiceEnv


def live():
    pass


def ready():
    status_report = StatusReport()
    features_status = Status.healthy
    features_reason = None

    if FeatureServiceEnv.FDL_ENABLED.value:
        # TODO: need full impl here
        pass
    else:
        ctakes_host_name = FeatureServiceEnv.UMLS_HOST.value
        if ctakes_host_name.endswith('rest'):
            ctakes_host_name = ctakes_host_name[:-4]
        ctakes_response = requests.get(f'{ctakes_host_name}/health/ready')
        if ctakes_response.ok:
            status_report.add_status(Component.ctakes, (Status.healthy, None))
        else:
            status_report.add_status(Component.ctakes, (Status.dead, ctakes_response.reason))
            features_status = Status.conditional
            features_reason = 'CTAKES status'

    status_report.add_status(Component.features, (features_status, features_reason))

    return status_report.as_json(), features_status.value


def version():
    git_path = FeatureServiceEnv.root_dir
    return get_version_info(git_path).to_dict()
