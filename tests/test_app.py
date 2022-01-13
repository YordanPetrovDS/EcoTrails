import json

from config import create_app
from db import db
from flask_testing import TestCase
from models.enums import RoleType

from tests.factories import UserFactory
from tests.helpers import generate_token


class TestApplication(TestCase):
    def create_app(self):
        return create_app("config.TestingConfig")

    def setUp(self):
        db.init_app(self.app)
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_authentication_missing_auth_header_raises(self):
        """
        Test if a user is login when register endpoint is hit.
        """
        url_methods = [
            ("/profile/ecotrails", "GET"),
            ("/profile/ecotrails", "POST"),
            ("/profile/ecotrails/1", "PUT"),
            ("/profile/ecotrails/1", "DELETE"),
            ("/moderators/ecotrails/1/approve", "PUT"),
            ("/moderators/ecotrails/1/reject", "PUT"),
            ("/admins/users/1/create-admin", "PUT"),
            ("/admins/users/1/create-moderator", "PUT"),
            ("/admins/moderators/1", "PUT"),
            ("/ecotrails/1/visited", "PUT"),
            ("/ecotrails/1/planned", "PUT"),
            ("/profile/ecotrails/visited", "GET"),
            ("/profile/ecotrails/planned", "GET"),
            ("/profile/ecotrails/visited/1", "DELETE"),
            ("/profile/ecotrails/planned/1", "DELETE"),
        ]

        for url, method in url_methods:
            if method == "POST":
                resp = self.client.post(
                    url,
                    data=json.dumps({}),
                )
            elif method == "GET":
                resp = self.client.get(url)
            elif method == "PUT":
                resp = self.client.put(
                    url,
                    data=json.dumps({}),
                )
            else:
                resp = self.client.delete(url)

            self.assert400(resp, {"message": "Invalid token"})

    def test_permission_required_endpoints_admin_access_raises(self):
        """
        Test if a user is an admin when registered endpoint is hit.
        """
        url_methods = [
            "/admins/users/1/create-admin",
            "/admins/users/1/create-moderator",
            "/admins/moderators/1",
        ]
        for url in url_methods:
            user = UserFactory()
            token = generate_token(user)
            headers = {"Authorization": f"Bearer {token}"}
            resp = self.client.put(url, data=json.dumps({}), headers=headers)
            expected_message = {
                "message": "You do not have the rights to access this resource"
            }
            self.assert403(resp, expected_message)

            moderator = UserFactory()
            moderator.role = RoleType.moderator
            token = generate_token(moderator)
            headers = {"Authorization": f"Bearer {token}"}
            resp = self.client.put(url, data=json.dumps({}), headers=headers)
            expected_message = {
                "message": "You do not have the rights to access this resource"
            }
            self.assert403(resp, expected_message)

    def test_permission_required_endpoints_moderator_access_raises(self):
        """
        Test if a user is a moderator when registered endpoint is hit.
        """
        url_methods = [
            "/moderators/ecotrails/1/approve",
            "/moderators/ecotrails/1/reject",
        ]
        for url in url_methods:
            user = UserFactory()
            token = generate_token(user)
            headers = {"Authorization": f"Bearer {token}"}
            resp = self.client.put(url, data=json.dumps({}), headers=headers)
            expected_message = {
                "message": "You do not have the rights to access this resource"
            }
            self.assert403(resp, expected_message)

            admin = UserFactory()
            admin.role = RoleType.administrator
            token = generate_token(admin)
            headers = {"Authorization": f"Bearer {token}"}
            resp = self.client.put(url, data=json.dumps({}), headers=headers)
            expected_message = {
                "message": "You do not have the rights to access this resource"
            }
            self.assert403(resp, expected_message)
