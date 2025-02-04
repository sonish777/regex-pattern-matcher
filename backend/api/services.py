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
                    str(row[self.column]))
        return rows
