# 🧾 OCR - Intelligent Image Data Extractor
# 📌 Overview
This project is a FastAPI-based OCR (Optical Character Recognition) service that extracts structured data from images. It supports reading:

Product labels (SKU, Serial No., EAN, etc.)
Government IDs (Aadhar, PAN, Name, DOB)
Retail receipts (Items, Prices, Total, Store Info)
Barcodes (via pyzbar)
The API can process images via a public URL and return neatly structured JSON responses.

# 🛠️ Features
🔍 OCR using Tesseract (eng+ara support)
🧾 Receipt Parsing: Extracts store name, date, time, total amount, item details
📇 ID Card Extraction: Supports Aadhar and PAN card formats
📦 Product Info Parsing: EAN, SKU, Product Model, Serial Number
📷 Barcode Scanning: Supports 1D/2D barcode decoding via pyzbar
🚀 Built with FastAPI for high performance
🚀 API Endpoint
POST /process-image-url
Takes an image URL and returns extracted information.

# Request:

json
Copy
Edit
{
  "image_url": "https://example.com/image.jpg"
}
# Response:

json
Copy
Edit
{
  "status": "success",
  "barcodes": ["123456789012"],
  "product_details": {
    "EAN": "8901234567890",
    "SKU": "102.567",
    "Product Model": "Widget X200",
    "Serial Number": "ABCD1234",
    "Last Numeric Code": "123.4567.890XYZ"
  },
  "id_card_details": {
    "Aadhar Number": "1234 5678 9012",
    "PAN Number": "ABCDE1234F",
    "Date of Birth": "01/01/1990",
    "Name": "John Doe"
  },
  "receipt_details": {
    "Store Name": "SuperMart",
    "Receipt Number": "987654321",
    "Date": "15/03/2024",
    "Time": "14:35",
    "Total Amount": "1,299.00",
    "Items": [
      { "name": "Item A", "quantity": "2", "price": "199.00" },
      { "name": "Item B", "quantity": "1", "price": "899.00" }
    ]
  },
  "ocr_text": "<Raw extracted text from the image>"
}
# 🧱 Tech Stack
Python
FastAPI – Web framework
pytesseract – OCR engine
pyzbar – Barcode reader
Pillow – Image processing
OpenCV – Image enhancements (optional)
Regex – Pattern-based info extraction
# 📦 Setup
Install Dependencies
bash
Copy
Edit
pip install fastapi uvicorn pytesseract pyzbar pillow opencv-python requests
Install Tesseract

Windows: Download here
Ubuntu:
bash
Copy
Edit
sudo apt install tesseract-ocr
Run the API

bash
Copy
Edit
uvicorn main:app --reload
# 📌 Example Use Case
Want to scan receipts, extract inventory data, or pull key ID details from an uploaded document? Just pass the image URL, and this API returns structured data ready for database entry, dashboards, or analytics.

# 🙋‍♂️ Contributions
This tool was developed for real-world applications in document digitization and automation workflows. Feel free to fork it and adapt it to your needs.

