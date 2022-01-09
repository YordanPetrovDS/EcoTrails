import base64
import os
import re
import uuid

from constants import TEMP_FILE_FOLDER
from models.ecotrail import EcotrailModel
from services.s3 import S3Service
from sqlalchemy.orm import class_mapper
from werkzeug.exceptions import BadRequest

s3 = S3Service()


def decode_photo(encoded_photo, path):
    with open(path, "wb") as file:
        try:
            file.write(base64.b64decode(encoded_photo.encode("utf-8")))
        except Exception:
            raise BadRequest("Invalid photo encoding")


def upload_photo_and_return_photo_url(data):
    encoded_photo = data.pop("photo")
    extension = data.pop("photo_extension")
    name = f"{str(uuid.uuid4())}"
    path = os.path.join(TEMP_FILE_FOLDER, f"{name}.{extension}")
    photo_name = f"{name}.{extension}"

    try:
        decode_photo(encoded_photo, path)
        photo_url = s3.upload_photo(path, photo_name)
    except Exception as ex:
        raise ex
    finally:
        os.remove(path)

    data["photo_url"] = photo_url
    return data


def procces_query_filters(filter_by):
    def computed_operator(column, v):
        if re.match(r"^!", v):
            """__ne__"""
            val = re.sub(r"!", "", v)
            return column.__ne__(val)
        if re.match(r">(?!=)", v):
            """__gt__"""
            val = re.sub(r">(?!=)", "", v)
            return column.__gt__(val)
        if re.match(r"<(?!=)", v):
            """__lt__"""
            val = re.sub(r"<(?!=)", "", v)
            return column.__lt__(val)
        if re.match(r">=", v):
            """__ge__"""
            val = re.sub(r">=", "", v)
            return column.__ge__(val)
        if re.match(r"<=", v):
            """__le__"""
            val = re.sub(r"<=", "", v)
            return column.__le__(val)
        if re.match(r"(\w*)-(\w*)", v):
            """between"""
            a, b = re.split(r"-", v)
            return column.between(a, b)
        """ default __eq__ """
        return column.__eq__(v)

    filters = []
    mapper = class_mapper(EcotrailModel)
    for k, v in filter_by.items():
        if not hasattr(mapper.columns, k):
            continue
        filters.append(computed_operator(mapper.columns[k], "{}".format(v)))
    return filters
