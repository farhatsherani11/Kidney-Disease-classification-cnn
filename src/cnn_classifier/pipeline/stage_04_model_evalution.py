from cnn_classifier.config.configuration import ConfigurationManager
from cnn_classifier.components.model_evalution_mlflow import Evalution
from cnn_classifier import logger

STAGE_NAME = "Evalution Stage"

class EvalutionPipeline:
    def __init__(self):
        pass
    def main(self):
        config = ConfigurationManager()
        eval_config = config.get_evaluation_config()
        evalution = Evalution(eval_config)
        evalution.evaluate_model()
        # evalution.log_into_mlflow()  just for decide parameters use mlflow

if __name__ == "__main__":
    try:
        logger.info(f"***************************")
        logger.info(f">>>>> stage {STAGE_NAME} started <<<<<")
        obj = EvalutionPipeline()
        obj.main()
        logger.info(f">>>>> stage {STAGE_NAME} completed <<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e