import sys, os
sys.path.append(os.path.join(os.getcwd(), "src"))

 
from cnn_classifier import logger
from cnn_classifier.pipeline.stage_01_data_ingestion import DataIngestionTrainingPipeline
from cnn_classifier.pipeline.stage_02_base_model import BaseModelTrainingPipeline
from cnn_classifier.pipeline.stage_03_model_train import ModelTrainPipeline
from cnn_classifier.pipeline.stage_04_model_evalution import EvalutionPipeline

STAGE_NAME = "Data Ingestion Stage"

try:
        logger.info(f">>>>> stage {STAGE_NAME} started <<<<<")
        obj = DataIngestionTrainingPipeline()
        obj.main()
        logger.info(f">>>>> stage {STAGE_NAME} completed <<<<<\n\nx==========x")
except Exception as e:
        logger.exception(e)
        raise e


STAGE_NAME = "Base Model Preparation Stage"
try:
        logger.info(f">>>>> stage {STAGE_NAME} started <<<<<")
        obj = BaseModelTrainingPipeline()
        obj.main()
        logger.info(f">>>>> stage {STAGE_NAME} completed <<<<<\n\nx==========x")
except Exception as e:
        logger.exception(e)
        raise e



STAGE_NAME = "Model Training Stage"
try:
        logger.info(f">>>>> stage {STAGE_NAME} started <<<<<")
        obj = ModelTrainPipeline()
        obj.main()
        logger.info(f">>>>> stage {STAGE_NAME} completed <<<<<\n\nx==========x")
except Exception as e:
        logger.exception(e)
        raise e



STAGE_NAME = "Evalution Stage"
try:
        logger.info(f">>>>> stage {STAGE_NAME} started <<<<<")
        obj = EvalutionPipeline()
        obj.main()
        logger.info(f">>>>> stage {STAGE_NAME} completed <<<<<\n\nx==========x")
except Exception as e:
        logger.exception(e)
        raise e