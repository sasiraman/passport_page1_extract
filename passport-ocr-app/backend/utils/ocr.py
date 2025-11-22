"""
OCR utility for extracting text from passport images.
"""
import pytesseract
from PIL import Image
import io


def extract_text(image):
    """
    Extract text from passport image using OCR.
    
    Args:
        image: PIL Image object or numpy array
        
    Returns:
        str: Extracted text
    """
    try:
        if not isinstance(image, Image.Image):
            image = Image.fromarray(image)
        
        # Use Tesseract OCR with English language
        text = pytesseract.image_to_string(image, lang='eng')
        return text.strip()
    except Exception as e:
        raise Exception(f"OCR extraction failed: {str(e)}")

