"""
Flask backend application for Passport OCR, MRZ parsing, and face extraction.
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
import io
import sys
import os

# Add utils directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))

from utils.ocr import extract_text
from utils.mrz_parser import parse_mrz
from utils.face_extract import extract_face

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({"status": "healthy"}), 200


@app.route('/process-passport', methods=['POST'])
def process_passport():
    """
    Process passport image: extract OCR text, parse MRZ, and extract face.
    
    Expected request:
        - POST with multipart/form-data
        - File field named 'file'
    
    Returns:
        JSON response with:
        - ocr_text: Extracted text from OCR
        - mrz_data: Parsed MRZ fields (dict)
        - face_image: Base64 encoded face image (or null)
        - error: Error message if any
    """
    try:
        # Check if file is present
        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        
        # Read image
        image_bytes = file.read()
        image = Image.open(io.BytesIO(image_bytes))
        
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Process image
        results = {
            "ocr_text": "",
            "mrz_data": {},
            "face_image": None,
            "error": None
        }
        
        # Extract OCR text
        try:
            results["ocr_text"] = extract_text(image)
        except Exception as e:
            results["error"] = f"OCR error: {str(e)}"
        
        # Parse MRZ
        try:
            results["mrz_data"] = parse_mrz(image)
        except Exception as e:
            if results["error"]:
                results["error"] += f" | MRZ error: {str(e)}"
            else:
                results["error"] = f"MRZ error: {str(e)}"
        
        # Extract face
        try:
            face_base64 = extract_face(image)
            results["face_image"] = face_base64
        except Exception as e:
            if results["error"]:
                results["error"] += f" | Face extraction error: {str(e)}"
            else:
                results["error"] = f"Face extraction error: {str(e)}"
        
        # Return results
        return jsonify(results), 200
        
    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

