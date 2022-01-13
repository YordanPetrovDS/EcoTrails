import json

from config import create_app
from db import db
from flask_testing import TestCase
from models.enums import RoleType
from models.user import UserModel

from tests.helpers import object_as_dict


class TestAuth(TestCase):
    def create_app(self):
        self.headers = {"Content-Type": "application/json"}
        return create_app("config.TestingConfig")

    def setUp(self):
        db.init_app(self.app)
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_register_user(self):
        """
        Test if a user is in database when register endpoint is hit.
        Assure that the role assing is a User role.
        """
        url = "/register"
        data = {
            "email": "DjordjanoPetkov@abv.bg",
            "password": "djordjano123",
            "first_name": "Djordjano",
            "last_name": "Petkov",
        }

        users = UserModel.query.all()
        assert len(users) == 0

        resp = self.client.post(url, data=json.dumps(data), headers=self.headers)

        assert resp.status_code == 201
        assert "token" in resp.json

        # users = UserModel.query.all()
        # assert len(users) == 1

        user = object_as_dict(users[0])
        user.pop("password")
        data.pop("password")
        assert user == {"id": user["id"], "role": RoleType.user, **data}
