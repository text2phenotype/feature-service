 # feature-service
API for biomed model data

Quick Start
---
Envvironment Variables:
```
FEATURE_SERVICE_HOST="0.0.0.0"
FEATURE_SERVICE_PORT=8081
DATA_ROOT={project root}
PRELOAD_FEATURE_DATA=TRUE
DEBUG=FALSE
NLP_HOST:{ctakes url}
```

```
pip install text2phenotype-py
pip install feature-service
cd feature-service
python nltk-download.py
python feature_service
```
  NLP Pipelines
 ---------------------------
https://github.com/text2phenotype/ctakes

 * **default_clinical**: extract coded concepts from text using standard vocabs (SNOMED, RXNORM, etc)
 * **lab_value**: Lab value names, values, and units (LOINC/SNOMED)
 * **drug_ner**: Drug Named Entity Recognition with dosage and frequency (RXNORM)
 * **smoking_status**: Smoking status detection (SNOMED-CT)
 * **temporal_module**: temporal relations, match dates/times with clinical concepts
 * **pos_tagger**: Part Of Speech Tagging (NLTK)
 * **hepc_clinical**: **default_clinical** pipeline using HEPC dictionary
 * **hepc_drug_ner**: **drug_ner** pipeline using HEPC dictionary
 * **hepc_lab_value**: **lab_value** pipeline using HEPC dictionary