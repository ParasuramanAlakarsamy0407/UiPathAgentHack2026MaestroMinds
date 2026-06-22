from fastapi import FastAPI
from docxtpl import DocxTemplate
from datetime import datetime
from typing import Dict, Any
import os

app = FastAPI()

TEMPLATE_FILE = "Carrier_Quote_Template.docx"

OUTPUT_FOLDER = "GeneratedDocs"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)


@app.post("/generate")
async def generate_document(payload: Dict[str, Any]):

    try:

        doc = DocxTemplate(TEMPLATE_FILE)

        doc.render(payload)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        file_name = f"Quote_{timestamp}.docx"

        output_path = os.path.join(
            OUTPUT_FOLDER,
            file_name
        )

        doc.save(output_path)

        return {
            "status": "success",
            "file_name": file_name,
            "local_path": os.path.abspath(output_path)
        }

    except Exception as ex:

        return {
            "status": "failed",
            "error": str(ex)
        }