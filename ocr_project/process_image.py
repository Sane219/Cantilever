import os
import zipfile
import logging
from ocr_processor import extract_text
from database import store_ocr_result
import subprocess

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def download_kaggle_dataset(dataset='suvroo/scanned-images-dataset-for-ocr-and-vlm-finetuning', download_path='static/images'):
    """Download and extract Kaggle dataset."""
    try:
        if not os.path.exists(download_path):
            os.makedirs(download_path)
        
        # Download dataset using Kaggle API
        zip_path = os.path.join(download_path, 'scanned-images-dataset.zip')
        logger.info(f"Downloading dataset {dataset} to {zip_path}")
        subprocess.run(['kaggle', 'datasets', 'download', '-d', dataset, '-p', download_path], check=True)
        
        # Extract ZIP
        logger.info(f"Extracting {zip_path}")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(download_path)
        
        # Remove ZIP file
        os.remove(zip_path)
        logger.info("Dataset downloaded and extracted")
    except subprocess.CalledProcessError as e:
        logger.error(f"Kaggle API error: {e}. Ensure kaggle.json is in ~/.kaggle/ and permissions are set.")
        raise
    except Exception as e:
        logger.error(f"Error downloading dataset: {e}")
        raise

def process_dataset(image_dir='static/images', max_images=10):
    """Process images in the specified directory."""
    try:
        if not os.path.exists(image_dir):
            os.makedirs(image_dir)
        
        # Download Kaggle dataset if no images exist
        if not any(f.endswith(('.png', '.jpg', '.jpeg')) for f in os.listdir(image_dir)):
            download_kaggle_dataset(download_path=image_dir)
        
        # Process images (limit to max_images for efficiency)
        image_count = 0
        for filename in os.listdir(image_dir):
            if filename.endswith(('.png', '.jpg', '.jpeg')) and image_count < max_images:
                image_path = os.path.join(image_dir, filename)
                result = extract_text(image_path)
                store_ocr_result(result)
                logger.info(f"Processed {image_path}: {result['text'][:50]}...")
                image_count += 1
        
        if image_count == 0:
            logger.warning(f"No valid images found in {image_dir}")
        else:
            logger.info(f"Processed {image_count} images")
    except Exception as e:
        logger.error(f"Error processing dataset: {e}")

if __name__ == '__main__':
    process_dataset()