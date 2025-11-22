"""
MRZ (Machine Readable Zone) parser for passport images.
"""
from passporteye import read_mrz
import cv2
import numpy as np
from PIL import Image


def parse_mrz(image):
    """
    Parse MRZ data from passport image.
    
    Args:
        image: PIL Image object or numpy array
        
    Returns:
        dict: Parsed MRZ data with fields like surname, given_names, passport_number, etc.
    """
    try:
        # Convert PIL Image to numpy array if needed
        if isinstance(image, Image.Image):
            img_array = np.array(image)
            # Convert RGB to BGR for OpenCV
            if len(img_array.shape) == 3 and img_array.shape[2] == 3:
                img_array = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
        else:
            img_array = image
        
        # Use passporteye to read MRZ
        mrz = read_mrz(img_array)
        
        if mrz is None:
            return {}
        
        # Extract MRZ data
        mrz_data = {}
        
        if hasattr(mrz, 'surname') and mrz.surname:
            mrz_data['Surname'] = mrz.surname
        if hasattr(mrz, 'names') and mrz.names:
            mrz_data['Given Names'] = ' '.join(mrz.names)
        if hasattr(mrz, 'passport_number') and mrz.passport_number:
            mrz_data['Passport Number'] = mrz.passport_number
        if hasattr(mrz, 'nationality') and mrz.nationality:
            mrz_data['Nationality'] = mrz.nationality
        if hasattr(mrz, 'date_of_birth') and mrz.date_of_birth:
            mrz_data['DOB'] = str(mrz.date_of_birth)
        if hasattr(mrz, 'sex') and mrz.sex:
            mrz_data['Sex'] = mrz.sex
        if hasattr(mrz, 'expiration_date') and mrz.expiration_date:
            mrz_data['Expiry Date'] = str(mrz.expiration_date)
        
        return mrz_data
    except Exception as e:
        raise Exception(f"MRZ parsing failed: {str(e)}")

