import json
import re

from django.utils.dateparse import parse_datetime
from django.utils.timezone import is_aware, make_aware
from rest_framework import parsers


class MultipartJsonParser(parsers.MultiPartParser):

    def parse(self, stream, media_type=None, parser_context=None):
        result = super().parse(
            stream,
            media_type=media_type,
            parser_context=parser_context
        )
        data = {}

        for key, value in result.data.items():
            if value == '':
                continue
            if '{' in value or "[" in value:
                try:
                    data[key] = json.loads(value)
                    continue
                except ValueError:
                    data[key] = value
                    continue
            if type(value) != str:
                data[key] = value
                continue
            if value in ['true', 'false']:
                data[key] = bool(value)
                continue
            if value == 'null':
                data[key]=None
                continue
            if str(value).isdigit():
                data[key] = int(value)
                continue
            if bool(re.search(value, r"(? <= \s)[-]?\d + [.]\d * (?:[eE][+-]\d+)?(?=\s)")):
                data[key] = float(value)
                continue
            else:
                data[key] = value
        return parsers.DataAndFiles(data, result.files)


def get_aware_datetime(date_str):
    ret = parse_datetime(date_str)
    if not is_aware(ret):
        ret = make_aware(ret)
    return ret