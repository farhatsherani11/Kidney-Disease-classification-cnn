from cnn_classifier.config.configuration import ConfigurationManager
from cnn_classifier.components.model_training import Training
from cnn_classifier import logger
import tensorflow as tf
import os
import time



STAGE_NAME = "Model Training Stage"

class ModelTrainPipeline:
    def __init__(self):
        pass
        
    def main(self):
            # Configure environment for CPU
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
        tf.get_logger().setLevel('ERROR')

        # Clear session
        tf.keras.backend.clear_session()

        start_time = time.time()

        try:
            config = ConfigurationManager()
            training_config = config.get_training_config()
            
        
            
            print(f" OPTIMIZED TRAINING CONFIGURATION:")
            print(f"Epochs: {training_config.epochs}")
            print(f"Batch Size: {training_config.batch_size}")
            
            training = Training(config=training_config)
            training.get_base_model()
            training.train_valid_generator()
            
            # Start optimized training
            training.train()
            
            total_time = time.time() - start_time
            hours = total_time // 3600
            minutes = (total_time % 3600) // 60
            
            print(f"Training completed in {int(hours)}h {int(minutes)}m")
            
        except Exception as e:
            print(f" Training failed: {e}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    try:
        logger.info(f">>>>> stage {STAGE_NAME} started <<<<<")
        obj = ModelTrainPipeline()
        obj.main()
        logger.info(f">>>>> stage {STAGE_NAME} completed <<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e


