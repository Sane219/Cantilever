import cv2
import pytesseract
from PIL import Image
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def preprocess_image(image_path):
    """
    Preprocess image for better OCR accuracy.
    Args:
        image_path (str): Path to the input image
    Returns:
        Processed image
    """
    try:
        # Read image with OpenCV
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Failed to load image: {image_path}")
        
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Apply thresholding to enhance text
        _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        return thresh
    except Exception as e:
        logger.error(f"Preprocessing error for {image_path}: {e}")
        return None

def extract_text(image_path):
    """
    Extract text from an image using Tesseract OCR.
    Args:
        image_path (str): Path to the input image
    Returns:
        dict: Extracted text and metadata
    """
    try:
        # Preprocess image
        processed_img = preprocess_image(image_path)
        if processed_img is None:
            return {'image_path': image_path, 'text': 'N/A', 'error': 'Image preprocessing failed'}
        
        # Configure Tesseract
        custom_config = r'--oem 3 --psm 6'  # Default OCR engine, assume block of text
        text = pytesseract.image_to_string(processed_img, config=custom_config)
        
        logger.info(f"Extracted text from {image_path}")
        return {'image_path': image_path, 'text': text.strip(), 'error': None}
    except Exception as e:
        logger.error(f"OCR error for {image_path}: {e}")
        return {'image_path': image_path, 'text': 'N/A', 'error': str(e)}