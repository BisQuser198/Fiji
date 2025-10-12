import os, json
import pandas as pd
from docx import Document

def process_file(path):
    """
    Read file at `path` based on extension.
    Returns a one-line summary string.
    """
    ext = os.path.splitext(path)[1].lower()

    if ext == '.csv':
        df = pd.read_csv(path)
        return f'CSV rows: {len(df)}'

    if ext in ('.xls', '.xlsx'):
        df = pd.read_excel(path)
        return f'Excel rows: {len(df)}'

    if ext == '.json':
        data = json.load(open(path))
        count = len(data) if isinstance(data, list) else len(data.keys())
        return f'JSON items: {count}'

    if ext == '.docx':
        doc = Document(path)
        return f'DOCX paragraphs: {len(doc.paragraphs)}'

    return 'Unsupported file type'
