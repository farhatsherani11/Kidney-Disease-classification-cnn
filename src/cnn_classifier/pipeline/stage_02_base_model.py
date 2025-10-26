from cnn_classifier.config.configuration import ConfigurationManager
from cnn_classifier.components.base_model import PrepareBaseModel
from cnn_classifier import logger

STAGE_NAME = "Base Model Preparation Stage"

class BaseModelTrainingPipeline:
    def __init__(self):
        pass
    def main(self):
        config= ConfigurationManager()
        base_model_config = config.get_base_model_config()
        base_model = PrepareBaseModel(config=base_model_config)
        base_model.get_base_model()
        base_model.update_base_model()

if __name__ == "__main__":
    try:
        logger.info(f">>>>> stage {STAGE_NAME} started <<<<<")
        obj = BaseModelTrainingPipeline()
        obj.main()
        logger.info(f">>>>> stage {STAGE_NAME} completed <<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e