import tensorflow as tf
from pathlib import Path
import mlflow
import mlflow.keras
from urllib.parse import urlparse
from src.cnn_classifier.entity.config_entity import EvalutionConfig
from src.cnn_classifier.utils.common import save_json

class Evalution:
    def __init__(self, config: EvalutionConfig):
        self.config = config
    
    def _valid_generator(self):
        datagenerator_kwargs = dict(
            rescale=1./255,
            validation_split=0.30
        )
       
        dataflow_kwargs = dict(
            target_size=self.config.params_image_size,
            batch_size=self.config.params_batch_size,
            interpolation="bilinear"
        )
       
        valid_datagenerator = tf.keras.preprocessing.image.ImageDataGenerator(
            **datagenerator_kwargs
        )
       
        self.valid_generator = valid_datagenerator.flow_from_directory(
            directory=self.config.train_data_path,
            subset="validation",
            shuffle=False,
            **dataflow_kwargs
        )

    @staticmethod
    def _load_model(path: Path) -> tf.keras.Model:
        return tf.keras.models.load_model(path)

    def evaluate_model(self):
        self.model = self._load_model(self.config.path_of_model)
        self._valid_generator()
        self.score = self.model.evaluate(self.valid_generator)
        self.save_score()

    def save_score(self):
        score = {
            "loss": self.score[0],
            "accuracy": self.score[1]
        }
        save_json(path=Path("scores.json"), data=score)

    def log_into_mlflow(self):
        with mlflow.start_run():
            mlflow.log_params(self.config.all_parameters)
            mlflow.log_metrics({
                "loss": self.score[0],
                "accuracy": self.score[1]
            })

            
            mlflow.keras.log_model(
                self.model,
                artifact_path="model"
            )
