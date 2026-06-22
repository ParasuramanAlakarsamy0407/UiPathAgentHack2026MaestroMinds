from fastapi import FastAPI
from docxtpl import DocxTemplate
from datetime import datetime
from typing import Dict, Any
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import os
import json

app = FastAPI()

TEMPLATE_FILE = "Carrier_Quote_Template.docx"
OUTPUT_FOLDER = "GeneratedDocs"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# ==========================================
# GOOGLE DRIVE CONFIG FROM ENV VARIABLES
# ==========================================

GOOGLE_DRIVE_FOLDER_ID = os.getenv("GOOGLE_DRIVE_FOLDER_ID")

service_account_info = json.loads(
    os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")
)

SCOPES = [
    "https://www.googleapis.com/auth/drive"
]


def upload_to_drive(file_path: str):

    credentials = service_account.Credentials.from_service_account_info(
        service_account_info,
        scopes=SCOPES
    )

    service = build(
        "drive",
        "v3",
        credentials=credentials
    )

    file_name = os.path.basename(file_path)

    metadata = {
        "name": file_name,
        "parents": [GOOGLE_DRIVE_FOLDER_ID]
    }

    media = MediaFileUpload(
        file_path,
        resumable=True
    )

    uploaded_file = service.files().create(
        body=metadata,
        media_body=media,
        fields="id,name"
    ).execute()

    file_id = uploaded_file["id"]

    service.permissions().create(
        fileId=file_id,
        body={
            "type": "anyone",
            "role": "reader"
        }
    ).execute()

    file_url = f"https://drive.google.com/file/d/{file_id}/view"

    return {
        "file_id": file_id,
        "file_url": file_url
    }


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

        drive_result = upload_to_drive(output_path)

        try:
            os.remove(output_path)
        except:
            pass

        return {
            "status": "success",
            "file_name": file_name,
            "file_id": drive_result["file_id"],
            "file_url": drive_result["file_url"]
        }

    except Exception as ex:

        return {
            "status": "failed",
            "error": str(ex)
        }
