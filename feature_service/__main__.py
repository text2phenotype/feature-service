import connexion

from text2phenotype.apm.flask import configure_apm
from text2phenotype.common.cli_utils import CommonCLIArguments
from text2phenotype.common.log import operations_logger
from text2phenotype.open_api import encoder

from feature_service.feature_service_env import FeatureServiceEnv
from feature_service.feature_set.feature_cache import FeatureCache


operations_logger.info('Starting service...')
app = connexion.App(__name__, specification_dir='./')
configure_apm(app.app, FeatureServiceEnv.APM_SERVICE_NAME.value)

operations_logger.debug(f'app.app.config = {app.app.config}')

app.app.json_encoder = encoder.JSONEncoder
app.add_api('open_api_spec.yml', arguments={'title': 'Text2phenotype Feature Service'})
for handler in operations_logger.logger.handlers:
    app.app.logger.addHandler(handler)

FeatureCache(FeatureServiceEnv.PRELOAD.value)

if __name__ == '__main__':
    debug = CommonCLIArguments().debug
    app.run(host=FeatureServiceEnv.SVC_HOST.value,
            port=FeatureServiceEnv.SVC_PORT.value,
            debug=debug)
