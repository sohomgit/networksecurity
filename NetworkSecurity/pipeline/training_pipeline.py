import os
import sys

from NetworkSecurity.exceptions.exceptions import NetworkSecurityException
from NetworkSecurity.logging.logger import logging

from NetworkSecurity.components.data_ingestion import  DataIngestion
from NetworkSecurity.components.data_transformation import DataTransformation
from NetworkSecurity.components.data_validation import DataValidation
from NetworkSecurity.components.model_trainer import ModelTrainer

from NetworkSecurity.constants.training_pipeline import TRAINING_BUCKET_NAME
from NetworkSecurity.cloud.s3_syncer import S3Sync

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
        self.s3_sync = S3Sync()
    
    def start_data_ingestion(self):
        try:
            self.data_ingestion_config = DataIngestionConfig(training_pipeline_config=self.training_pl_config)
            logging.info("Initiate the data ingestion")
            data_ingestion=DataIngestion(self.data_ingestion_config)
            dataingestionartifact=data_ingestion.initiate_data_ingestion()
            logging.info("Data Initiation Completed")
            logging.info(f"dataingestionartifact is{dataingestionartifact}")
            return dataingestionartifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def start_data_validation(self,dataingestionartifact:DataIngestionArtifact):
        try:
            data_validation_config=DataValidationConfig(self.training_pl_config)
            data_validation=DataValidation(dataingestionartifact,data_validation_config)
            logging.info("Initiate the data Validation")
            data_validation_artifact=data_validation.initiate_data_validation()
            logging.info("data Validation Completed")
            logging.info(f"data_validation_artifact is{data_validation_artifact}")
            return data_validation_artifact

        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def start_data_transformation(self,data_validation_artifact:DataValidationArtifact):
        try:
            data_transformation_config=DataTransformationConfig(self.training_pl_config)
            logging.info("data Transformation started")
            data_transformation=DataTransformation(data_validation_artifact,data_transformation_config)
            data_transformation_artifact=data_transformation.initiate_data_transformation()
            logging.info("data Transformation completed")
            logging.info(f"data_transformation_artifact is{data_transformation_artifact}")
            return data_transformation_artifact

        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def start_model_training(self,data_transformation_artifact:DataTransformationArtifact):
        try:
            logging.info("Model Training stared")
            model_trainer_config=ModelTrainerConfig(self.training_pl_config)
            model_trainer=ModelTrainer(model_trainer_config=model_trainer_config,data_transformation_artifact=data_transformation_artifact)
            model_trainer_artifact=model_trainer.initiate_model_trainer()
            logging.info("Model Training artifact created")
            logging.info(f"model_trainer_artifact is {model_trainer_artifact}")
            return model_trainer_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
   
    
    def sync_artifact_dir_to_s3(self):
        try:
            aws_bucket_url = f"s3://{TRAINING_BUCKET_NAME}/artifact/{self.training_pl_config.timestamp}"
            self.s3_sync.sync_folder_to_s3(folder= self.training_pl_config.artifact_dir,aws_bucket_url= aws_bucket_url)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def sync_saved_model_dir_to_s3(self):
        try:
            aws_bucket_url = f"s3://{TRAINING_BUCKET_NAME}/artifact/{self.training_pl_config.timestamp}"
            self.s3_sync.sync_folder_to_s3(folder= self.training_pl_config.model_dir,aws_bucket_url= aws_bucket_url)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def run_pipeline(self):
        dataingestionartifact = self.start_data_ingestion()
        data_validation_artifact = self.start_data_validation(dataingestionartifact)
        data_transformation_artifact = self.start_data_transformation(data_validation_artifact)
        model_trainer_artifact = self.start_model_training(data_transformation_artifact)
        self.sync_artifact_dir_to_s3()
        self.sync_saved_model_dir_to_s3()
        return model_trainer_artifact

