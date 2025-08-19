from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import shutil
import tempfile
import os

from main import process_invoice  
app = FastAPI()

@app.post("/ocr")
async def ocr_invoice(file: UploadFile = File(...)):
    try:
        # Save uploaded file to a temporary location
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            shutil.copyfileobj(file.file, tmp)
            tmp_path = tmp.name

        # Run OCR on the saved PDF
        result = process_invoice(tmp_path)

        # Clean up the temporary file
        os.remove(tmp_path)

        return result

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"An error occurred: {str(e)}"}
        )


