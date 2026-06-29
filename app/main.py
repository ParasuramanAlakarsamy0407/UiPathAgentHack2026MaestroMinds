from fastapi import FastAPI
from docxtpl import DocxTemplate
from datetime import datetime
from typing import Dict, Any
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import os
import json
from pydantic import BaseModel
from weasyprint import HTML

class HtmlToPdfRequest(BaseModel):
    html_content: str
    output_file_name: str | None = None
app = FastAPI(
    title="AgentHack Document Generator",
    version="1.0"
)

GOOGLE_DRIVE_FOLDER_ID = os.getenv("GOOGLE_DRIVE_FOLDER_ID")

TEMPLATE_FILE = "templates/Carrier_Quote_Template.docx"
OUTPUT_FOLDER = "generated"
TOKEN_FILE = "/etc/secrets/token.json"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)


from google.oauth2.credentials import Credentials

def upload_to_google_drive(file_path: str, mime_type: str):

    creds = Credentials.from_authorized_user_file(
        TOKEN_FILE,
        ["https://www.googleapis.com/auth/drive.file"]
    )

    service = build(
        "drive",
        "v3",
        credentials=creds
    )

    file_name = os.path.basename(file_path)

    file_metadata = {
        "name": file_name,
        "parents": [GOOGLE_DRIVE_FOLDER_ID]
    }

    media = MediaFileUpload(
        file_path,
        mimetype=mime_type
    )

    uploaded_file = service.files().create(
        body=file_metadata,
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

    return f"https://drive.google.com/file/d/{file_id}/view"


@app.get("/")
def health_check():
    return {
        "status": "running"
    }


@app.post("/generate")
async def generate_document(payload: Dict[str, Any]):

    try:

        if not GOOGLE_DRIVE_FOLDER_ID:
            raise Exception(
                "GOOGLE_DRIVE_FOLDER_ID environment variable not configured"
            )

        request_id = payload.get("Transaction", {}).get("Request_ID")

        if not request_id:
            raise Exception("Request_ID not found in payload")

        json2_path = os.path.join(
            "AppData",
            f"{request_id}.json"
        )

        if not os.path.exists(json2_path):
            raise Exception(
                f"JSON2 file not found: {json2_path}"
            )

        with open(json2_path, "r", encoding="utf-8") as f:
            json2 = json.load(f)

        merged_payload = {
            **payload,
            **json2
        }

        doc = DocxTemplate(TEMPLATE_FILE)

        doc.render(merged_payload)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        file_name = f"Quote_{timestamp}.docx"

        output_path = os.path.join(
            OUTPUT_FOLDER,
            file_name
        )

        doc.save(output_path)

        file_url = upload_to_google_drive(
    output_path,
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
)

        return {
            "status": "success",
            "file_name": file_name,
            "file_url": file_url
        }

    except Exception as ex:

        return {
            "status": "failed",
            "error": str(ex)
        }

@app.get("/debug-token")
def debug_token():

    import os

    path = TOKEN_FILE

    if not os.path.exists(path):
        return {"exists": False}

    with open(path, "rb") as f:
        first_20_bytes = f.read(20)

    return {
        "exists": True,
        "first_bytes": str(first_20_bytes)
    }


@app.post("/html-to-pdf")
async def html_to_pdf(request: HtmlToPdfRequest):

    try:

        if not GOOGLE_DRIVE_FOLDER_ID:
            raise Exception(
                "GOOGLE_DRIVE_FOLDER_ID environment variable not configured"
            )

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        file_name = (
            request.output_file_name
            if request.output_file_name
            else f"HTML_{timestamp}.pdf"
        )

        if not file_name.lower().endswith(".pdf"):
            file_name += ".pdf"

        output_path = os.path.join(
            OUTPUT_FOLDER,
            file_name
        )

        HTML(string=request.html_content).write_pdf(output_path)

        file_url = upload_to_google_drive(
            output_path,
            "application/pdf"
        )

        return {
            "status": "success",
            "file_name": file_name,
            "file_url": file_url
        }

    except Exception as ex:

        return {
            "status": "failed",
            "error": str(ex)
        }


