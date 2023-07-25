import functools

from text2phenotype.common.log import operations_logger
from text2phenotype.common.speech import chunk_text

from feature_service.feature_service_env import FeatureServiceEnv
from feature_service.features.feature import Feature


class chunk_annotations:
    def __call__(self, func):

        @functools.wraps(func)
        def decorated(self: Feature, *args, **kwargs):
            text = kwargs.get('text', args[0])
            chunks = chunk_text(text, FeatureServiceEnv.NLP_HOST_MAX_TOKENS.value)
            operations_logger.debug(f'{len(chunks)} chunks found for annotation for feature "{self.feature_type.name}"')

            combined_annotations = []

            for i, chunk in enumerate(chunks, start=1):
                chunk_range = chunk[0]
                chunk_str = chunk[1]

                operations_logger.debug(f'Chunk #{i} / {len(chunks)} with size: {len(chunk_str)} processing')

                # Call "annotate()" function for chunk
                try:
                    chunk_annotations = list(func(self, text=chunk_str, **kwargs))
                except Exception:
                    operations_logger.exception(
                        f'An exception occurred during annotation for feature "{self.feature_type.name}". '
                        f'Chunk #{i} / {len(chunks)}, chunk range: {chunk_range}, chunk size: {len(chunk_str)}')
                    raise

                # Update ranges, combine annotations
                for ann_range, ann in chunk_annotations:
                    ann_range = (ann_range[0] + chunk_range[0], ann_range[1] + chunk_range[0])
                    combined_annotations.append((ann_range, ann))

            return combined_annotations

        return decorated
