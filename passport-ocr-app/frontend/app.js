const fileInput = document.getElementById("fileInput");
const dropzone = document.getElementById("dropzone");
const previewSection = document.getElementById("preview");
const previewImage = document.getElementById("preview-image");
const processBtn = document.getElementById("processBtn");

const loading = document.getElementById("loading");
const results = document.getElementById("results");
const mrzTable = document.getElementById("mrz-table");
const ocrText = document.getElementById("ocr-text");
const faceImage = document.getElementById("face-image");
const errorBox = document.getElementById("error-box");

let selectedFile = null;

// ============================
// File Upload Handlers
// ============================
dropzone.addEventListener("click", () => fileInput.click());

fileInput.addEventListener("change", (e) => {
  selectedFile = e.target.files[0];
  if (selectedFile) {
    showPreview();
  }
});

dropzone.addEventListener("dragover", (e) => {
  e.preventDefault();
  dropzone.style.borderColor = "#764ba2";
  dropzone.style.background = "#f0f2ff";
});

dropzone.addEventListener("dragleave", (e) => {
  e.preventDefault();
  dropzone.style.borderColor = "#667eea";
  dropzone.style.background = "#f8f9ff";
});

dropzone.addEventListener("drop", (e) => {
  e.preventDefault();
  dropzone.style.borderColor = "#667eea";
  dropzone.style.background = "#f8f9ff";
  
  selectedFile = e.dataTransfer.files[0];
  if (selectedFile && selectedFile.type.startsWith("image/")) {
    showPreview();
  } else {
    showError("Please upload a valid image file.");
  }
});

function showPreview() {
  if (!selectedFile) return;
  
  previewSection.style.display = "block";
  const reader = new FileReader();
  reader.onload = (e) => {
    previewImage.src = e.target.result;
  };
  reader.readAsDataURL(selectedFile);
  
  // Hide previous results and errors
  results.style.display = "none";
  errorBox.style.display = "none";
}

// ============================
// Processing the Passport
// ============================
processBtn.addEventListener("click", async () => {
  if (!selectedFile) {
    showError("Please select a passport image first.");
    return;
  }

  results.style.display = "none";
  errorBox.style.display = "none";
  loading.style.display = "block";

  const formData = new FormData();
  formData.append("file", selectedFile);

  try {
    const res = await fetch("http://localhost:5000/process-passport", {
      method: "POST",
      body: formData
    });

    const data = await res.json();
    loading.style.display = "none";

    if (data.error) {
      showError(data.error);
      return;
    }

    // FACE
    if (data.face_image) {
      faceImage.src = "data:image/jpeg;base64," + data.face_image;
      faceImage.style.display = "block";
    } else {
      faceImage.src = "";
      faceImage.style.display = "none";
    }

    // OCR
    ocrText.textContent = data.ocr_text || "No OCR text extracted.";

    // MRZ TABLE
    mrzTable.innerHTML = "";
    if (data.mrz_data && Object.keys(data.mrz_data).length > 0) {
      Object.entries(data.mrz_data).forEach(([key, val]) => {
        const row = document.createElement("tr");
        const keyCell = document.createElement("td");
        const valCell = document.createElement("td");
        
        keyCell.textContent = key;
        valCell.textContent = val || "N/A";
        
        row.appendChild(keyCell);
        row.appendChild(valCell);
        mrzTable.appendChild(row);
      });
    } else {
      const row = document.createElement("tr");
      const cell = document.createElement("td");
      cell.colSpan = 2;
      cell.textContent = "No MRZ data found.";
      cell.style.textAlign = "center";
      cell.style.color = "#999";
      row.appendChild(cell);
      mrzTable.appendChild(row);
    }

    results.style.display = "block";
    
    // Smooth scroll to results
    results.scrollIntoView({ behavior: "smooth", block: "start" });

  } catch (err) {
    loading.style.display = "none";
    showError("Server error: " + err.message + ". Make sure the backend is running on http://localhost:5000");
  }
});

function showError(msg) {
  errorBox.textContent = msg;
  errorBox.style.display = "block";
  errorBox.scrollIntoView({ behavior: "smooth", block: "center" });
}

