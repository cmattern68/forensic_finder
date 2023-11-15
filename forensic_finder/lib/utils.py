from datetime import datetime


def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i: i + n]


def transform_datetime(val):
    return datetime.strptime(val, "%Y:%m:%d %H:%M:%S")
