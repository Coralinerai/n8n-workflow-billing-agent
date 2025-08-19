import cv2
import numpy as np
import pytesseract
from collections import defaultdict
import re

from pdf2image import convert_from_path
import os

def pdf_to_image(pdf_path, dpi=300):
    images = convert_from_path(pdf_path, dpi=dpi)
    return images[0]

def preprocessing(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(10, 10))
    enhanced = clahe.apply(gray)
    thresh = cv2.adaptiveThreshold(
        enhanced, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV, 25, 8
    )
    return thresh




def detect_text_blocks(thresh):
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 5))
    dilated = cv2.dilate(thresh, kernel, iterations=1)
    contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    min_area = 300
    blocks = []
    for cnt in contours:
        if cv2.contourArea(cnt) > min_area:
            x, y, w, h = cv2.boundingRect(cnt)
            blocks.append((x, y, w, h))
    
    # Sort blocks by Y position (top to bottom) then X (left to right)
    blocks.sort(key=lambda b: (b[1], b[0]))  # (y, x) sorting
    # Group by approximate Y positions first
    blocks.sort(key=lambda b: (round(b[1]/50)*50, b[0]))  # 50px Y tolerance   
    return blocks

def extract_text_from_blocks(image, blocks):
    results = {}
    for i, (x, y, w, h) in enumerate(blocks):
        roi = image[y:y+h, x:x+w]
        text = pytesseract.image_to_string(roi, config='--psm 6 -l fra+eng')
        if len(text.strip()) > 0:
            results[f"zone_{i}"] = {
                "text": text.strip()
            }
    return results



def process_invoice(pdf_path):
    pil_image=pdf_to_image(pdf_path)
    img = np.array(pil_image)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    processed_img = preprocessing(img)
    all_blocks = detect_text_blocks(processed_img)
    block_results = extract_text_from_blocks(img, all_blocks)

    return {
        "detected_blocks": block_results
    }