# 🛂 Passport OCR Web Application

A complete, production-ready web application for extracting information from passport images using OCR, MRZ parsing, and face detection.

## ✨ Features

- **OCR Text Extraction**: Extract all text from passport images using Tesseract OCR
- **MRZ Parsing**: Automatically parse Machine Readable Zone (MRZ) data from passports
- **Face Extraction**: Detect and extract passport photo using OpenCV face detection
- **Beautiful UI**: Modern, responsive frontend with drag-and-drop file upload
- **Real-time Processing**: Live preview and step-by-step results display

## 📁 Project Structure

```
passport-ocr-app/
├── backend/
│   ├── app.py                 # Flask application
│   ├── requirements.txt       # Python dependencies
│   ├── Dockerfile            # Docker configuration
│   └── utils/
│       ├── ocr.py            # OCR text extraction
│       ├── mrz_parser.py     # MRZ data parsing
│       └── face_extract.py   # Face detection and extraction
├── frontend/
│   ├── index.html            # Main HTML page
│   ├── styles.css            # Styling
│   └── app.js                # Frontend JavaScript
├── docker-compose.yml        # Docker Compose configuration
└── README.md                 # This file
```

## 🚀 Quick Start

### Option 1: Using Docker Compose (Recommended)

1. **Start the backend service:**
   ```bash
   cd passport-ocr-app
   docker-compose up --build
   ```

2. **Open the frontend:**
   - Simply open `frontend/index.html` in your web browser
   - Or use a local server:
     ```bash
     cd frontend
     python -m http.server 8000
     ```
     Then visit `http://localhost:8000`

### Option 2: Manual Setup

#### Backend Setup

1. **Install system dependencies:**
   ```bash
   # Ubuntu/Debian
   sudo apt-get update
   sudo apt-get install tesseract-ocr tesseract-ocr-eng

   # macOS
   brew install tesseract

   # Windows
   # Download and install from: https://github.com/UB-Mannheim/tesseract/wiki
   ```

2. **Install Python dependencies:**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. **Run the Flask server:**
   ```bash
   python app.py
   ```

   The backend will be available at `http://localhost:5000`

#### Frontend Setup

1. **Open the frontend:**
   - Simply open `frontend/index.html` in your web browser
   - Or use a local server:
     ```bash
     cd frontend
     python -m http.server 8000
     ```
     Then visit `http://localhost:8000`

## 📡 API Documentation

### Endpoints

#### `GET /health`
Health check endpoint.

**Response:**
```json
{
  "status": "healthy"
}
```

#### `POST /process-passport`
Process a passport image and extract OCR text, MRZ data, and face image.

**Request:**
- Method: `POST`
- Content-Type: `multipart/form-data`
- Body: Form data with `file` field containing the passport image

**Response:**
```json
{
  "ocr_text": "Extracted text from passport...",
  "mrz_data": {
    "Surname": "DOE",
    "Given Names": "JOHN",
    "Passport Number": "A12345678",
    "Nationality": "USA",
    "DOB": "1990-01-01",
    "Sex": "M",
    "Expiry Date": "2030-01-01"
  },
  "face_image": "base64_encoded_image_string",
  "error": null
}
```

**Error Response:**
```json
{
  "error": "Error message here",
  "ocr_text": "",
  "mrz_data": {},
  "face_image": null
}
```

## 🎯 Usage

1. **Upload Passport Image:**
   - Drag and drop a passport image onto the upload area, or
   - Click the upload area to select a file from your computer

2. **Preview:**
   - Once uploaded, you'll see a preview of the passport image
   - Click the "Process Passport" button to start extraction

3. **View Results:**
   - **Extracted Face**: Shows the detected passport photo
   - **MRZ Parsed Data**: Displays parsed fields in a table format
   - **OCR Text**: Shows all extracted text in a scrollable panel

## 🔧 Technologies Used

### Backend
- **Flask**: Web framework
- **pytesseract**: Python wrapper for Tesseract OCR
- **passporteye**: MRZ parsing library
- **OpenCV**: Face detection and image processing
- **Pillow**: Image manipulation
- **NumPy**: Numerical operations

### Frontend
- **HTML5**: Structure
- **CSS3**: Styling with modern gradients and animations
- **JavaScript (ES6+)**: Client-side logic

## 📋 Supported Passport Types

The application supports standard passport formats including:
- ICAO 9303 compliant passports (most modern passports)
- Passports with Machine Readable Zone (MRZ)
- Various image formats (JPEG, PNG, etc.)

## ⚠️ Requirements

- **Backend:**
  - Python 3.8+
  - Tesseract OCR installed on the system
  - Docker (if using Docker setup)

- **Frontend:**
  - Modern web browser (Chrome, Firefox, Safari, Edge)
  - No additional dependencies required

## 🐛 Troubleshooting

### Backend Issues

1. **Tesseract not found:**
   - Ensure Tesseract OCR is installed and available in PATH
   - On Linux/Mac, verify with: `tesseract --version`

2. **MRZ parsing fails:**
   - Ensure the passport image is clear and the MRZ zone is visible
   - Try with a higher resolution image

3. **Face detection fails:**
   - Ensure the passport photo is clearly visible
   - Try with images that have good lighting and contrast

### Frontend Issues

1. **Cannot connect to backend:**
   - Ensure the backend is running on `http://localhost:5000`
   - Check browser console for CORS errors
   - Verify the backend URL in `app.js` if using a different port

2. **File upload not working:**
   - Ensure you're using a modern browser
   - Check browser console for JavaScript errors

## 📝 License

This project is provided as-is for educational and development purposes.

## 🤝 Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## 📧 Support

For issues or questions, please open an issue on the repository.

