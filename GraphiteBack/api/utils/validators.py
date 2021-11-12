from datetime import datetime


def datetime_check_and_convert(time_str: str) -> datetime or None:
    """ Конвертирует строку в Datetime если возможно"""

    try:
        return datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S.%f%z')
    except ValueError:
        try:
            return datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S.%f')
        except ValueError:
            try:
                return datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S%z')
            except ValueError:
                try:
                    return datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
                except ValueError:
                    return None
