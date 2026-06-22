import os

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

TEMPLATE_FILE = os.path.join(
    BASE_DIR,
    "templates",
    "Carrier_Quote_Template.docx"
)

OUTPUT_FOLDER = os.path.join(
    BASE_DIR,
    "generated"
)

os.makedirs(
    OUTPUT_FOLDER,
    exist_ok=True
)
