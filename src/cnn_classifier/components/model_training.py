import os
import urllib.request as request
from zipfile import ZipFile
import tensorflow as tf
import time
from cnn_classifier.entity.config_entity import TrainingConfig
from pathlib import Path

class Training:
    def __init__(self, config: TrainingConfig):
        self.config = config
    
    def get_base_model(self):
        # Load model without optimizer state
        self.model = tf.keras.models.load_model(
            self.config.updated_base_model_path,
            compile=False
        )
        
        # Create a fresh optimizer
        optimizer = tf.keras.optimizers.Adam(learning_rate=0.001)
        
        # Recompile the model
        self.model.compile(
            optimizer=optimizer,
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        print("Model loaded and compiled successfully")
    
    def train_valid_generator(self):
        datagenerator_kwargs = dict(
            rescale=1./255,
            validation_split=0.20
        )

        dataflow_kwargs = dict(
            target_size=self.config.params_image_size[:-1],
            batch_size=self.config.batch_size,
            interpolation="bilinear",
            class_mode="categorical"
        )

        valid_datagenerator = tf.keras.preprocessing.image.ImageDataGenerator(
            **datagenerator_kwargs
        )

        self.valid_generator = valid_datagenerator.flow_from_directory(
            directory=self.config.training_data,
            subset="validation",
            shuffle=False,
            **dataflow_kwargs
        )

        if self.config.params_is_augmentation:
            train_datagenerator = tf.keras.preprocessing.image.ImageDataGenerator(
                rotation_range=40,
                horizontal_flip=True,
                width_shift_range=0.2,
                height_shift_range=0.2,
                shear_range=0.2,
                zoom_range=0.2,
                **datagenerator_kwargs
            )
        else:
            train_datagenerator = valid_datagenerator

        self.train_generator = train_datagenerator.flow_from_directory(
            directory=self.config.training_data,
            subset="training",
            shuffle=True,
            **dataflow_kwargs
        )
    
    @staticmethod
    def save_model(path: Path, model: tf.keras.Model):
        model.save(path)
    
    def train(self):
        # OPTIMIZED FOR CPU - DRAMATICALLY REDUCE STEPS
        self.steps_per_epoch = 80    # Instead of 622!
        self.validation_steps = 20   # Instead of 77!
        
        print(" OPTIMIZED CPU TRAINING STARTED")
        print(f"Steps per epoch: {self.steps_per_epoch} (was 622)")
        print(f"Validation steps: {self.validation_steps} (was 77)")
        print(f"Expected time per epoch: ~20-30 minutes")
        print(f"Total expected time: 5-7 hours for {self.config.epochs} epochs")
        
        # Add early stopping to potentially stop even earlier
        callbacks = [
            tf.keras.callbacks.EarlyStopping(
                monitor='val_accuracy',
                patience=3,
                restore_best_weights=True,
                verbose=1
            ),
            tf.keras.callbacks.ModelCheckpoint(
                filepath=str(self.config.trained_model_path).replace('.keras', '_best.keras'),
                save_best_only=True,
                monitor='val_accuracy',
                mode='max',
                verbose=1
            )
        ]

        # Train the model with optimized steps
        history = self.model.fit(
            self.train_generator,
            epochs=self.config.epochs,
            steps_per_epoch=self.steps_per_epoch,
            validation_steps=self.validation_steps,
            validation_data=self.valid_generator,
            callbacks=callbacks,
            verbose=1
        )

        # Save the final model
        self.save_model(
            path=self.config.trained_model_path,
            model=self.model
        )
        
        return history