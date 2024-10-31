import os
import sys

from NetworkSecurity.exceptions.exceptions import NetworkSecurityException
from NetworkSecurity.logging.logger import logging

from NetworkSecurity.components.data_ingestion import  DataIngestion
from NetworkSecurity.components.data_transformation import DataTransformation
from NetworkSecurity.components.data_validation import DataValidation
from NetworkSecurity.components.model_trainer import ModelTrainer

from NetworkSecurity.entity.config_entity import(
    TrainingPipelineConfig,
    DataIngestionConfig,
    DataTransformationConfig,
    DataValidationConfig,
    ModelTrainerConfig
)

from NetworkSecurity.entity.artifact_entity import(
    DataIngestionArtifact,
    DataTransformationArtifact,
    DataValidationArtifact,
    ModelTrainerArtifact
)

class TrainingPipeline:
    def __init__(self):
        self.training_pl_config = TrainingPipelineConfig()
    
    def start_data_ingestion(self):
        try:
            self.data_ingestion_config = DataIngestionConfig(training_pipeline_config=self.training_pl_config)
            logging.info("Data Ingestion Started")
            

        except Exception as e:
            raise NetworkSecurityException(e,sys)