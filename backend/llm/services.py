from huggingface_hub import InferenceClient
from django.conf import settings
import json


class LLMService:
    def __init__(self, model='Qwen/Qwen2.5-Coder-32B-Instruct'):
        self.client = InferenceClient(api_key=settings.HF_API_KEY, model=model)

    def generate_regex_from_description(self, description, headers=[]):
        prompt = f"""
        Given the user input description: '{description}', and the list of column headers: {json.dumps(headers)}, generate a response in JSON format with two fields:
        1. **regex**: The regular expression that matches the pattern described in the user input.
        2. **column**: The column where the regex should be applied, based on the headers provided.

        The user input may describe entities such as names, emails, phone numbers, or addresses. Your task is to:
        - Identify the correct column based on the context of the description and the provided column headers.
        - Generate a regex that matches the described entity, taking into account the column headers and avoiding mistakes like matching locations when searching for names.

        ### Example Input:
        - **User Description:** 'Find all the full names of the users'
        - **Column Headers:** ['name', 'email', 'phone', 'address']

        ### Expected Output (JSON format):
        {{
        "regex": "\\b[A-Z][a-z]+ [A-Z][a-z]+\\b",
        "column": "name"
        }}

        Rules:
        - Return only JSON. No explanations or extra text.
        - The `regex` field uses **double backslashes (\\\\) for escaping**.
        - If unsure, choose the most relevant column.
        - If no relevant column exists, return null values for both.
        """  # noqa: E501
        response = self.client.chat.completions.create(
            model="Qwen/Qwen2.5-Coder-32B-Instruct",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=500
        )
        return response.choices[0].message.content or '{}'

    def suggest_transformations(self, headers=[]):
        """Uses LLM to analyze column headers and suggest transformations."""
        prompt = f"""
        Given the list of column headers: {json.dumps(headers)}, suggest appropriate data transformations.
        The transformations should be useful for data cleaning and consistency.
        Return a JSON response with column names as keys and the suggested transformations as values.

        Supported transformations:
        - 'capitalize': Capitalize words in text columns (e.g., names, addresses).
        - 'normalize_email': Convert emails to lowercase.
        - 'format_currency': Ensure numbers in currency columns are formatted with commas and two decimal places.

        ### Example Input:
        - **Column Headers:** ['customer_name', 'email_address', 'price', 'phone_number']

        ### Expected Output (JSON format):
        {{
        "customer_name": "capitalize",
        "email_address": "normalize_email",
        "price": "format_currency"
        }}

        Rules:
        - Return JSON only, no explanations.
        - If no transformation is needed, omit the column.
        """  # noqa: E501
        response = self.client.chat.completions.create(
            model=self.client.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500
        )
        return response.choices[0].message.content or "{}"
