from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pyzbar.pyzbar import decode
from PIL import Image
import pytesseract
import cv2
import re
import requests
import numpy as np
import io

app = FastAPI()

class ImageURL(BaseModel):
    image_url: str

def download_image_from_url(url):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        image = Image.open(io.BytesIO(response.content))
        return image
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=400, detail=f"Failed to download image: {str(e)}")

def read_barcodes(image):
    barcodes = decode(image)
    return [barcode.data.decode('utf-8') for barcode in barcodes]

def perform_ocr(image):
    text = pytesseract.image_to_string(image, lang='eng+ara', config='--psm 6') # Experiment with PSM values
    return text.strip()

def extract_sku_and_serial_numbers(text):
    ean_pattern = r"EAN[:\s]*(\d+)"
    sku_pattern = r"SKU[:\s]*([\d\.]+)"
    product_pattern = r"Desc[:\s]*(.*)"
    serial_pattern = r"S/N[:\s]*([A-Z0-9]+)"
    last_numeric_pattern = r"(\d{3}\.\d{4}\.\d{3}[A-Z0-9]+)"

    ean = re.search(ean_pattern, text)
    sku = re.search(sku_pattern, text)
    product_model = re.search(product_pattern, text)
    serial = re.search(serial_pattern, text)
    last_numeric = re.search(last_numeric_pattern, text)

    return {
        "EAN": ean.group(1) if ean else "Not found",
        "SKU": sku.group(1) if sku else "Not found",
        "Product Model": product_model.group(1) if product_model else "Not found",
        "Serial Number": serial.group(1) if serial else "Not found",
        "Last Numeric Code": last_numeric.group(1) if last_numeric else "Not found"
    }

def extract_id_card_details(text):
    aadhar_pattern = r'\b\d{4}\s\d{4}\s\d{4}\b'
    pan_pattern = r'\b[A-Z]{5}[0-9]{4}[A-Z]{1}\b'
    dob_pattern = r'DOB\s*[:\-]?\s*(\d{2}\/\d{2}\/\d{4})'
    name_pattern = r'Name\s*[:\-]?\s*([A-Za-z\s]+)'

    aadhar_no = re.search(aadhar_pattern, text)
    pan_no = re.search(pan_pattern, text)
    dob = re.search(dob_pattern, text)
    name = re.search(name_pattern, text)

    return {
        "Aadhar Number": aadhar_no.group(0) if aadhar_no else "Not found",
        "PAN Number": pan_no.group(0) if pan_no else "Not found",
        "Date of Birth": dob.group(1) if dob else "Not found",
        "Name": name.group(1) if name else "Not found"
    }

def extract_receipt_details(text):
    details = {}

    store_name_match = re.search(r"(?i)(?:[A-Za-z\s&]+(?:Mart|Supermarket|Store|Hypermarket)?)\s*(?:Mihijam)?", text)
    details['Store Name'] = store_name_match.group(0).strip() if store_name_match else "Not found"

    receipt_num_match = re.search(r"(?i)TRN #\s*(\d+)", text)  # TRN number
    details['Receipt Number'] = receipt_num_match.group(1) if receipt_num_match else "Not found"

    date_time_match = re.search(r"(?i)(\d{2}[.\-/]\d{2}[.\-/]\d{4})\s*(?:Time:)?\s*(\d{2}:\d{2})?", text)
    if date_time_match:
        details['Date'] = date_time_match.group(1)
        details['Time'] = date_time_match.group(2) or "Not found"
    else:
        details['Date'] = "Not found"
        details['Time'] = "Not found"

    total_amount_match = re.search(r"(?i)Bill Amount:?\s*([\d,]+(?:\.\d{1,2})?)", text)
    details['Total Amount'] = total_amount_match.group(1) if total_amount_match else "Not found"

    items = []
    item_lines = re.findall(r"(.+?)\s*(\d+(?:\.\d+)?)\s*(?:[\d,]+\.\d+)?", text) # Quantity can be float
    for item_line in item_lines[1:]: # Skip the first line (header)
        try:
            name, quantity = item_line[0].strip(), item_line[1].strip()

            # Extract price from the line above if not found in the same line
            price_match = re.search(r"([\d,]+\.\d+)$", text.splitlines()[text.splitlines().index(item_line[0])-1])
            price = price_match.group(1) if price_match else "Not found"

            items.append({"name": name, "quantity": quantity, "price": price})

        except (ValueError, IndexError):
            print("Skipping invalid item line:", item_line)
            continue


    details['Items'] = items

    return details


@app.post("/process-image-url")
async def process_image_url(image_data: ImageURL):
    try:
        image = download_image_from_url(image_data.image_url)
        barcode_data = read_barcodes(image)
        extracted_text = perform_ocr(image)

        product_details = extract_sku_and_serial_numbers(extracted_text)
        id_details = extract_id_card_details(extracted_text)
        receipt_details = extract_receipt_details(extracted_text)

        return {
            "status": "success",
            "barcodes": barcode_data if barcode_data else "No barcodes found",
            "product_details": product_details,
            "id_card_details": id_details,
            "receipt_details": receipt_details,
            "ocr_text": extracted_text
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))