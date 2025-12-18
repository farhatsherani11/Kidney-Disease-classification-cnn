from src.cnn_classifier.constants import *
import os
from src.cnn_classifier.utils.common import read_yaml, create_directories,save_json
from src.cnn_classifier.entity.config_entity import (DataIngestionConfig,
                                                    BaseModelConfig,
                                                    TrainingConfig,EvalutionConfig)


class ConfigurationManager:
    def __init__(self, config_filepath=CONFIG_FILE_PATH, params_filepath=PARAMS_FILE_PATH):
        self.config = read_yaml(config_filepath)
        self.params = read_yaml(params_filepath)
        create_directories([self.config.artifacts_root])
    
    def get_data_ingestion_config(self) -> DataIngestionConfig:
        config = self.config.data_ingestion
        create_directories([config.root_dir])
        data_ingestion_config = DataIngestionConfig(
            root_dir=Path(config.root_dir),
            source_URL=config.source_URL,
            local_data_file=Path(config.local_data_file),
            unzip_dir=Path(config.unzip_dir)
        )
        return data_ingestion_config
    
    def get_base_model_config(self) -> BaseModelConfig:
        config = self.config.prepare_base_model
        create_directories([config.root_dir])
        base_model_config = BaseModelConfig (
            root_dir=Path(config.root_dir),
            base_model_path=Path(config.base_model_path),
            updated_base_model_path=Path(config.updated_base_model_path),
            params_Image_size=self.params.IMAGE_SIZE,
            params_learning_rate=self.params.LEARNING_RATE,
            params_classes=self.params.CLASSES,
            params_weights=self.params.WEIGHTS,
            params_include_top=self.params.INCLUDE_TOP,
        )
        return base_model_config
    

    def get_training_config(self) -> TrainingConfig:
        training=self.config.training
        prepare_base_model=self.config.prepare_base_model
        params=self.params
        training_data=os.path.join(self.config.data_ingestion.unzip_dir, "kidney_dataset")
        create_directories([Path(training.root_dir)])

        training_config = TrainingConfig(
            root_dir=Path(training.root_dir),
            trained_model_path=Path(training.trained_model_path),
            updated_base_model_path=Path(prepare_base_model.updated_base_model_path),
            training_data=Path(training_data),
            epochs=params.EPOCHS,
            batch_size=params.BATCH_SIZE,
            params_is_augmentation=params.AUGMENTATION,
            params_image_size=params.IMAGE_SIZE,
        )
        return training_config
    

    def get_evaluation_config(self) -> EvalutionConfig:
         eval_config = EvalutionConfig(
            path_of_model="artifacts/training/trained_model.h5",
            train_data_path="artifacts/data_ingestion/kidney_dataset",
            mlflow_url="https://dagshub.com/farhatsherani08/Kidney-Disease-classification-cnn.mlflow",
            all_parameters=self.params,
            params_image_size=self.params.IMAGE_SIZE,
            params_batch_size=self.params.BATCH_SIZE
        )
         return  eval_config