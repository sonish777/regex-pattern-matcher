# utils.py
import csv
import io
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


def process_csv(file):
    file_content = file.read().decode('utf-8')
    io_string = io.StringIO(file_content)
    csv_reader = csv.reader(io_string, delimiter=',')
    headers = next(csv_reader)
    rows = []
    for row in csv_reader:
        row_dict = dict(zip(headers, row))
        rows.append(row_dict)
    return rows


def process_excel(file):
    df = pd.read_excel(file)
    return df.to_dict(orient='records')
