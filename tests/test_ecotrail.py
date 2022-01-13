import json
import os
from unittest.mock import patch

from config import create_app
from constants import TEMP_FILE_FOLDER
from db import db
from flask_testing import TestCase
from models import EcotrailModel
from models.enums import State
from services.s3 import S3Service

from tests.factories import UserFactory
from tests.helpers import encoded_photo, generate_token, mock_uuid, object_as_dict


class TestEcotrail(TestCase):
    def create_app(self):
        self.headers = {"Content-Type": "application/json"}
        return create_app("config.TestingConfig")

    def setUp(self):
        db.init_app(self.app)
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    @patch("uuid.uuid4", mock_uuid)
    @patch.object(S3Service, "upload_photo", return_value="some.s3.url")
    def test_create_ecotrail_post(self, s3_mock):
        url = "/profile/ecotrails"
        data = {
            "title": "Test Title",
            "description": "Test Description",
            "photo": encoded_photo,
            "photo_extension": "jpg",
            "area": "Sofia",
            "mountain": "Sredna Gora",
            "length": 12.5,
            "denivelation": 492,
            "difficulty": 3,
        }
        user = UserFactory()
        token = generate_token(user)
        self.headers.update({"Authorization": f"Bearer {token}"})

        ecotrails = EcotrailModel.query.all()
        assert len(ecotrails) == 0

        resp = self.client.post(url, data=json.dumps(data), headers=self.headers)

        ecotrails = EcotrailModel.query.all()
        assert len(ecotrails) == 1
        data.pop("photo")
        photo_ext = data.pop("photo_extension")

        created_ecotrail = object_as_dict(ecotrails[0])
        created_ecotrail.pop("create_on")

        assert created_ecotrail == {
            "id": ecotrails[0].id,
            "status": State.pending,
            "photo_url": "some.s3.url",
            "user_id": user.id,
            **data,
        }

        expected_response = {
            "id": ecotrails[0].id,
            "status": State.pending.value,
            "photo_url": "some.s3.url",
            **data,
        }
        actual_response = resp.json
        actual_response.pop("create_on")

        assert resp.status_code == 201
        assert actual_response == expected_response

        photo_name = f"{mock_uuid()}.{photo_ext}"
        path = os.path.join(TEMP_FILE_FOLDER, photo_name)

        s3_mock.assert_called_once_with(path, photo_name)
