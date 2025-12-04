from fastapi import FastAPI, UploadFile, File, HTTPException
import pdfplumber
from typing import List

app = FastAPI()

COLUMN_NAMES = [
    "Research Assistant Name",
    "Date (dd/mm/yyyy)",
    "Start Time (HH:MM)",
    "End Time (HH:MM)",
    "Location",
    "Number of persons"
]

@app.post("/process")
async def process_pdf(file: UploadFile = File(...)):
    if file.content_type not in ["application/pdf"]:
        raise HTTPException(status_code=400, detail="Please upload a PDF file.")

    pdf_bytes = await file.read()

    rows = []

    with pdfplumber.open(file.file) as pdf:
        for page in pdf.pages:
            table = page.extract_table()
            if table:
                for row in table[1:]:  # skip header row
                    rows.append({
                        "Research Assistant Name": row[0],
                        "Date (dd/mm/yyyy)": row[1],
                        "Start Time (HH:MM)": row[2],
                        "End Time (HH:MM)": row[3],
                        "Location": row[4],
                        "Number of persons": int(row[5])
                    })

    return rows
