"""
Face extraction utility for passport images.
"""
import cv2
import numpy as np
from PIL import Image
import base64
import io


def extract_face(image):
    """
    Extract face from passport image.
    
    Args:
        image: PIL Image object or numpy array
        
    Returns:
        str: Base64 encoded JPEG image of extracted face, or None if no face found
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
        
        # Load face cascade classifier
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        # Convert to grayscale for face detection
        gray = cv2.cvtColor(img_array, cv2.COLOR_BGR2GRAY)
        
        # Detect faces
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )
        
        if len(faces) == 0:
            return None
        
        # Get the largest face (usually the passport photo)
        largest_face = max(faces, key=lambda rect: rect[2] * rect[3])
        x, y, w, h = largest_face
        
        # Extract face region with some padding
        padding = 10
        x_start = max(0, x - padding)
        y_start = max(0, y - padding)
        x_end = min(img_array.shape[1], x + w + padding)
        y_end = min(img_array.shape[0], y + h + padding)
        
        face_roi = img_array[y_start:y_end, x_start:x_end]
        
        # Convert back to RGB for PIL
        face_rgb = cv2.cvtColor(face_roi, cv2.COLOR_BGR2RGB)
        face_pil = Image.fromarray(face_rgb)
        
        # Convert to base64
        buffered = io.BytesIO()
        face_pil.save(buffered, format="JPEG")
        img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
        
        return img_base64
    except Exception as e:
        raise Exception(f"Face extraction failed: {str(e)}")

