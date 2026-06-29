# AgentHack 2026 - Document Generator API

## Overview

This API accepts JSON input and generates a Microsoft Word document using a DOCX template.

The generated document is returned as Base64 content which can be decoded and uploaded to UiPath Storage Buckets.

## Endpoint

POST /generate

## Request

```json
{
  "Client_Firmographics": {
    "Company_Name": "Acme Global Solutions"
  }
}
```

## Response

```json
{
  "status": "success",
  "file_name": "Quote_20260623_101500.docx",
  "file_content": "<base64 string>"
}
```

## Run Locally

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## UiPath Flow

Maestro → HTTP Request → FastAPI → Base64 Response → Write File → Upload Storage File
