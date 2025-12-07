import os
import urllib.request as request
import zipfile
import gdown
from src.cnn_classifier import logger
from src.cnn_classifier.utils.common import get_size
from src.cnn_classifier.entity.config_entity import DataIngestionConfig

class  DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config
         
    def download_file(self):
      
      try:
       dataset_url=self.config.source_URL
       zip_download_dir=self.config.local_data_file
       os.makedirs("artifacts/data_ingestion",exist_ok=True)
       logger.info(f"Downloading file from :{dataset_url} into file :{zip_download_dir}")

       file_id = dataset_url.split('/')[-2]
       prefix='https://drive.google.com/uc?/export=download&id='
       gdown.download(prefix+file_id, str(zip_download_dir))

       logger.info(f"Downloaded data from: {dataset_url} into file :{zip_download_dir} of size :{get_size(zip_download_dir)}")

      except Exception as e:
         raise e
    
    def extract_zip_file(self):
       
       unzip_path=self.config.unzip_dir
       os.makedirs(unzip_path,exist_ok=True)
       with zipfile.ZipFile(self.config.local_data_file,mode="r") as zip_ref:
           zip_ref.extractall(unzip_path)
        



# import os
# import zipfile
# import shutil
# from pathlib import Path
# from src.cnn_classifier import logger
# from src.cnn_classifier.utils.common import get_size
# from src.cnn_classifier.entity.config_entity import DataIngestionConfig
# import gdown

# class DataIngestion:
#     def __init__(self, config: DataIngestionConfig):
#         self.config = config

#     def download_file(self):
#         """
#         Download file from Google Drive using gdown
#         """
#         try:
#             dataset_url = self.config.source_URL
#             zip_download_dir = self.config.local_data_file
            
#             # Create directory using config, not hardcoded path
#             os.makedirs(os.path.dirname(zip_download_dir), exist_ok=True)
            
#             logger.info(f"Downloading file from: {dataset_url} into file: {zip_download_dir}")

#             # ✅ CORRECT WAY to extract file ID from Google Drive URL
#             if 'file/d/' in dataset_url:
#                 file_id = dataset_url.split('file/d/')[1].split('/')[0]
#             elif 'id=' in dataset_url:
#                 file_id = dataset_url.split('id=')[1].split('&')[0]
#             else:
#                 # Fallback: try to get the ID from URL segments
#                 file_id = dataset_url.split('/')[-2] if '/d/' in dataset_url else None
                
#             if not file_id:
#                 raise ValueError(f"Could not extract file ID from URL: {dataset_url}")

#             # ✅ CORRECT Google Drive download URL format
#             prefix = 'https://drive.google.com/uc?export=download&id='
#             download_url = prefix + file_id
            
#             logger.info(f"Download URL: {download_url}")
            
#             # Download the file
#             gdown.download(download_url, str(zip_download_dir), quiet=False)

#             logger.info(f"Downloaded data from: {dataset_url} into file: {zip_download_dir} of size: {get_size(Path(zip_download_dir))}")

#         except Exception as e:
#             logger.error(f"Error downloading file: {e}")
#             raise e

#     def extract_zip_file(self):
#         """
#         Extracts the zip file into the data directory and fixes nested folders
#         """
#         unzip_path = Path(self.config.unzip_dir)
#         unzip_path.mkdir(parents=True, exist_ok=True)
        
#         # Verify the file is a valid zip
#         if not zipfile.is_zipfile(self.config.local_data_file):
#             raise ValueError(f"File is not a valid zip: {self.config.local_data_file}")
        
#         with zipfile.ZipFile(self.config.local_data_file, 'r') as zip_ref:
#             zip_ref.extractall(unzip_path)
        
#         logger.info("Zip file extracted successfully")
        
#         # Fix nested folders
#         self.fix_nested_structure()

#     def fix_nested_structure(self):
#         """
#         Automatically detect and fix nested folder structure from Google Drive downloads
#         """
#         unzip_path = Path(self.config.unzip_dir)
        
#         logger.info("Checking for nested folder structure...")
        
#         # Get all items in the unzip directory
#         items = list(unzip_path.iterdir())
        
#         # Case 1: If there's only one directory and it's the dataset, move its contents up
#         if len(items) == 1 and items[0].is_dir():
#             nested_dir = items[0]
#             logger.info(f"Found nested directory: {nested_dir}")
            
#             # Move all contents from nested directory to parent
#             for item in nested_dir.iterdir():
#                 destination = unzip_path / item.name
#                 if destination.exists():
#                     # If destination exists, handle conflicts
#                     if item.is_dir():
#                         # Merge directories
#                         self.merge_directories(item, destination)
#                     else:
#                         # Rename conflicting file
#                         new_name = f"{item.stem}_backup{item.suffix}"
#                         shutil.move(str(item), str(unzip_path / new_name))
#                 else:
#                     shutil.move(str(item), str(destination))
            
#             # Remove the now-empty nested directory
#             try:
#                 nested_dir.rmdir()
#                 logger.info(f"Removed empty nested directory: {nested_dir}")
#             except OSError as e:
#                 logger.info(f"Could not remove {nested_dir}: {e}")
        
#         # Case 2: Check if class folders are nested one level deeper
#         elif self.are_classes_nested(unzip_path):
#             logger.info("Class folders are nested, fixing structure...")
#             self.flatten_nested_classes(unzip_path)
        
#         else:
#             logger.info("Directory structure is already correct")

#     def are_classes_nested(self, base_path):
#         """Check if class folders are nested one level deep"""
#         expected_classes = ['Cyst', 'Normal', 'Stone', 'Tumor']
        
#         for item in base_path.iterdir():
#             if item.is_dir():
#                 # Check if this directory contains our class folders
#                 sub_items = list(item.iterdir())
#                 if any(sub_item.name in expected_classes and sub_item.is_dir() for sub_item in sub_items):
#                     return True
#         return False

#     def flatten_nested_classes(self, base_path):
#         """Flatten nested class folder structure"""
#         expected_classes = ['Cyst', 'Normal', 'Stone', 'Tumor']
        
#         for item in base_path.iterdir():
#             if item.is_dir():
#                 # Check if this directory contains our class folders
#                 for class_name in expected_classes:
#                     class_path = item / class_name
#                     if class_path.exists() and class_path.is_dir():
#                         target_path = base_path / class_name
#                         # Move class directory to top level
#                         if target_path.exists():
#                             self.merge_directories(class_path, target_path)
#                         else:
#                             shutil.move(str(class_path), str(target_path))
#                         logger.info(f"Moved {class_name} to top level")
                
#                 # Try to remove the now-empty parent directory
#                 try:
#                     item.rmdir()
#                     logger.info(f"Removed empty directory: {item}")
#                 except OSError:
#                     logger.info(f"Could not remove {item} (may not be empty)")

#     def merge_directories(self, source_dir, target_dir):
#         """Merge contents of source directory into target directory"""
#         target_dir.mkdir(parents=True, exist_ok=True)
        
#         for item in source_dir.iterdir():
#             destination = target_dir / item.name
#             if destination.exists():
#                 if item.is_dir():
#                     # Recursively merge subdirectories
#                     self.merge_directories(item, destination)
#                 else:
#                     # Rename conflicting files
#                     counter = 1
#                     while destination.exists():
#                         new_name = f"{item.stem}_{counter}{item.suffix}"
#                         destination = target_dir / new_name
#                         counter += 1
#                     shutil.move(str(item), str(destination))
#             else:
#                 shutil.move(str(item), str(destination))

#     def initiate_data_ingestion(self):
#         """
#         Main method to initiate data ingestion process
#         """
#         try:
#             logger.info("Starting data ingestion...")
            
#             # Download the file
#             self.download_file()
            
#             # Extract and fix nested structure
#             self.extract_zip_file()
            
#             # Verify final structure
#             self.verify_structure()
            
#             logger.info("Data ingestion completed successfully!")
#             return self.config.unzip_dir
            
#         except Exception as e:
#             logger.error(f"Error in data ingestion: {e}")
#             raise e

#     def verify_structure(self):
#         """Verify that the final structure is correct"""
#         unzip_path = Path(self.config.unzip_dir)
#         expected_classes = ['Cyst', 'Normal', 'Stone', 'Tumor']
        
#         logger.info("VERIFYING FINAL STRUCTURE:")
#         found_classes = []
        
#         for item in unzip_path.iterdir():
#             if item.is_dir() and item.name in expected_classes:
#                 image_count = len([f for f in item.iterdir() if f.is_file() and f.suffix.lower() in ['.jpg', '.jpeg', '.png']])
#                 found_classes.append(item.name)
#                 logger.info(f"  ✅ {item.name}: {image_count} images")
        
#         missing_classes = set(expected_classes) - set(found_classes)
#         if missing_classes:
#             logger.warning(f"  ❌ Missing classes: {missing_classes}")
#             return False
#         else:
#             logger.info("  🎉 All classes found with correct structure!")
#             return True