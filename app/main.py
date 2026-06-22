```python
from fastapi import FastAPI
from docxtpl import DocxTemplate
from datetime import datetime
from typing import Dict, Any
import base64
import os

from config import TEMPLATE_FILE, OUTPUT_FOLDER

app = FastAPI(
    title="AgentHack Document Generator",
    version="1.0"
)

@app.get("/")
def health_check():
    return {
        "status": "running"
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

        with open(output_path, "rb") as file:
            file_content = base64.b64encode(
                file.read()
            ).decode("utf-8")

        try:
            os.remove(output_path)
        except:
            pass

        return {
            "status": "success",
            "file_name": file_name,
            "file_content": file_content
        }

    except Exception as ex:

        return {
            "status": "failed",
            "error": str(ex)
        }
```
