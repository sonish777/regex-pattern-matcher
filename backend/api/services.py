import re
from .utils import extract_json_from_plain_text


class RegexParserService:

    def parse(self, regex_json_string):
        regex_json = extract_json_from_plain_text(regex_json_string)
        self.compiled_regex = re.compile(regex_json.get("regex")) \
            if regex_json.get("regex") else None
        self.column = regex_json.get("column")
        return self

    def apply_replacement(self, rows, replacement):
        if not self.compiled_regex or not self.column:
            return rows
        for row in rows:
            if self.column in row:
                row[self.column] = self.compiled_regex.sub(
                    replacement,
                    str(row[self.column]).strip())
        return rows


class DataTransformationService:

    def parse(self, transformation_json_string):
        self.transformations = extract_json_from_plain_text(
            transformation_json_string)
        return self

    def apply_transformations(self, rows):
        if not rows or not self.transformations:
            return rows

        for row in rows:
            for column, transformation in self.transformations.items():
                if column in row:
                    row[column] = self \
                        ._apply_single_transformation(
                            row[column],
                            transformation)
        return rows

    def _apply_single_transformation(self, value, transformation):

        transformation_map = {
            "capitalize": lambda v: str(v).strip().title(),
            "normalize_email": lambda v: str(v).strip().lower(),
            "format_currency": lambda v: f"{float(v):,.2f}"
            if v.replace(',', '').isdigit() else v
        }

        return transformation_map.get(transformation, lambda v: v)(value)
