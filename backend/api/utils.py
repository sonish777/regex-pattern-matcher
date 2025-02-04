# utils.py
import csv
import io
import re
import json
import pandas as pd
from rest_framework.response import Response
from rest_framework import status


def api_response(data=None,
                 error=None,
                 errors=None,
                 status_code=status.HTTP_200_OK):
    """Utility function to standardize API responses."""
    if status_code == status.HTTP_422_UNPROCESSABLE_ENTITY:
        response_data = {
            "status": "error",
            "errors": errors
        }
    elif status_code >= status.HTTP_400_BAD_REQUEST:
        response_data = {
            "status": "error",
            "error": error
        }
    else:
        response_data = {
            "status": "success",
            "data": data or [],
        }
    return Response(response_data, status=status_code)


def detect_delimiter(file_content):
    if ',' in file_content.splitlines()[0]:
        return ','
    elif ';' in file_content.splitlines()[0]:
        return ';'
    else:
        raise ValueError("Unable to detect delimiter")


def process_csv(file):
    file_content = file.read().decode('utf-8')
    delimiter = detect_delimiter(file_content)
    io_string = io.StringIO(file_content)
    csv_reader = csv.reader(io_string, delimiter=delimiter)
    headers = next(csv_reader)
    rows = []
    for row in csv_reader:
        row_dict = dict(zip(headers, row))
        rows.append(row_dict)
    return rows


def process_excel(file):
    df = pd.read_excel(file)
    return df.to_dict(orient='records')


def extract_json_from_plain_text(text):
    try:
        json_match = re.search(r'\{.*\}', text, re.DOTALL)
        if not json_match:
            return {"regex": None, "column": None}
        json_text = json_match.group(0)
        return json.loads(json_text)
    except json.JSONDecodeError:
        return {"regex": None, "column": None}
