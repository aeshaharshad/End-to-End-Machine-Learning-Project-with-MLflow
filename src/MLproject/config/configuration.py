import importlib
import MLproject.constants
importlib.reload(MLproject.constants)
from MLproject.constants import *
from MLproject.utils.common import read_yaml, create_directories
from MLproject.entity.config_entity import (DataIngestionConfig,DataValidationConfig,DataTransformationConfig, ModelTrainerConfig)
class ConfigurationManager:
    def __init__(
        self,
        config_filepath = None,
        params_filepath = None,
        schema_filepath = None):
        
        # Get repo root from current working directory (go up one level from research)
        repo_root = Path.cwd().parent if Path.cwd().name == 'research' else Path.cwd()
        
        if config_filepath is None:
            from MLproject.constants import CONFIG_FILE_PATH
            config_filepath = CONFIG_FILE_PATH
        if params_filepath is None:
            from MLproject.constants import PARAMS_FILE_PATH
            params_filepath = PARAMS_FILE_PATH
        if schema_filepath is None:
            from MLproject.constants import SCHEMA_FILE_PATH
            schema_filepath = SCHEMA_FILE_PATH

        # Convert relative paths to absolute paths relative to repo root
        if not Path(config_filepath).is_absolute():
            config_filepath = repo_root / config_filepath
        if not Path(params_filepath).is_absolute():
            params_filepath = repo_root / params_filepath
        if not Path(schema_filepath).is_absolute():
            schema_filepath = repo_root / schema_filepath

        self.config = read_yaml(config_filepath)
        self.params = read_yaml(params_filepath)
        self.schema = read_yaml(schema_filepath)

        # Convert config paths to absolute paths
        artifacts_root = self.config.artifacts_root
        if not Path(artifacts_root).is_absolute():
            artifacts_root = repo_root / artifacts_root
        create_directories([artifacts_root])


    
    def get_data_ingestion_config(self) -> DataIngestionConfig:
        repo_root = Path.cwd().parent if Path.cwd().name == 'research' else Path.cwd()
        config = self.config.data_ingestion
        
        # Convert paths to absolute relative to repo root
        root_dir = config.root_dir
        if not Path(root_dir).is_absolute():
            root_dir = repo_root / root_dir
        
        local_data_file = config.local_data_file
        if not Path(local_data_file).is_absolute():
            local_data_file = repo_root / local_data_file
        
        unzip_dir = config.unzip_dir
        if not Path(unzip_dir).is_absolute():
            unzip_dir = repo_root / unzip_dir

        create_directories([root_dir])

        data_ingestion_config = DataIngestionConfig(
            root_dir=root_dir,
            source_URL=config.source_URL,
            local_data_file=local_data_file,
            unzip_dir=unzip_dir
        )

        return data_ingestion_config
    
    def get_data_validation_config(self) -> DataValidationConfig:
        config = self.config.data_validation
        schema = self.schema.COLUMNS

        create_directories([config.root_dir])

        data_validation_config = DataValidationConfig(
            root_dir=config.root_dir,
            STATUS_FILE=config.STATUS_FILE,
            unzip_data_dir = config.unzip_data_dir,
            all_schema=schema,
        )

        return data_validation_config
    
    def get_data_transformation_config(self) -> DataTransformationConfig:
        repo_root = Path.cwd()
        config = self.config.data_transformation

        root_dir = config.root_dir
        if not Path(root_dir).is_absolute():
            root_dir = repo_root / root_dir
        
        data_path = config.data_path
        if not Path(data_path).is_absolute():
            data_path = repo_root / data_path

        create_directories([root_dir])

        data_transformation_config = DataTransformationConfig(
            root_dir=root_dir,
            data_path=data_path,
        )

        return data_transformation_config
    def get_model_trainer_config(self) -> ModelTrainerConfig:
        repo_root = Path.cwd()
        config = self.config.model_trainer
        params = self.params.ElasticNet
        schema = self.schema.TARGET_COLUMN

        root_dir = config.root_dir
        if not Path(root_dir).is_absolute():
            root_dir = repo_root / root_dir
        
        train_data_path = config.train_data_path
        if not Path(train_data_path).is_absolute():
            train_data_path = repo_root / train_data_path
        
        test_data_path = config.test_data_path
        if not Path(test_data_path).is_absolute():
            test_data_path = repo_root / test_data_path

        create_directories([root_dir])

        model_trainer_config = ModelTrainerConfig(
            root_dir=root_dir,
            train_data_path=train_data_path,
            test_data_path=test_data_path,
            model_name=config.model_name,
            alpha=params.alpha,
            l1_ratio=params.l1_ratio,
            target_column=schema.name
        )

        return model_trainer_config