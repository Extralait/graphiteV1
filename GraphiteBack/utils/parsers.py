import json
import re
from pprint import pprint

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
            print(bool(re.search(value, r"(? <= \s)[-]?\d + [.]\d * (?:[eE][+-]\d+)?(?=\s)")))
            print(key,value)

            if value == '':
                continue
            if '{' in value or "[" in value:
                try:
                    data[key] = json.loads(value)
                    print(key, value, type(value))
                    continue
                except ValueError:
                    data[key] = value
                    continue
            if type(value) != str:
                data[key] = value
                print(key, value, type(value))
                continue
            if value in ['true', 'false']:
                data[key] = bool(value)
                print(key, value, type(value))
                continue
            if value == 'null':
                data[key]=None
                continue
            if str(value).isdigit():
                data[key] = int(value)
                print(key, value, type(value))
                continue
            if bool(re.search(value, r"(? <= \s)[-]?\d + [.]\d * (?:[eE][+-]\d+)?(?=\s)")):
                print(value)
                data[key] = float(value)
                print(key, value, type(value))
                continue
            else:
                data[key] = value
        pprint(data)
        return parsers.DataAndFiles(data, result.files)
