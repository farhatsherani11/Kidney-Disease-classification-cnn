from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class DataIngestionConfig:
    root_dir: Path
    source_URL: str
    local_data_file: Path
    unzip_dir: Path

@dataclass(frozen=True)
class BaseModelConfig:
    root_dir: Path
    base_model_path: Path
    updated_base_model_path: Path
    params_Image_size: list
    params_learning_rate: float
    params_classes: int
    params_weights: str
    params_include_top: bool


@dataclass(frozen=True)
class TrainingConfig:
    root_dir: Path
    trained_model_path: Path
    updated_base_model_path: Path
    training_data: Path
    epochs: int
    batch_size: int
    params_is_augmentation: bool
    params_image_size: list

@dataclass(frozen=True)
class EvalutionConfig:
    path_of_model: Path
    train_data_path: Path
    all_parameters: dict
    mlflow_url: str
    params_image_size:list
    params_batch_size:int