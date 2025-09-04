import os
import sys
import pytest
from jsonschema import validate

import requests
from sample_ptc.clients import ReqResClient

def test_get_user_success():
    user_id = 2
    user_data = ReqResClient.get_user(user_id)
    assert user_data['data']['id'] == user_id
    assert 'email' in user_data['data']
    assert 'first_name' in user_data['data']
    assert 'last_name' in user_data['data']

def test_get_user_json_schema():
        user_id = 2
        user_data = ReqResClient.get_user(user_id)
        schema = {
            "type": "object",
            "properties": {
                "data": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer"},
                        "email": {"type": "string"},
                        "first_name": {"type": "string"},
                        "last_name": {"type": "string"},
                        "avatar": {"type": "string"}
                    },
                    "required": ["id", "email", "first_name", "last_name", "avatar"]
                }
            },
            "required": ["data"]
        }
        validate(instance=user_data, schema=schema)

        # Validate partial match: check that some expected keys/values exist in the response
        expected_partial = {
            "data": {
                "id": user_id,
                'email': 'janet.weaver@reqres.in', 'first_name': 'Janet', 'last_name': 'Weaver', 'avatar': 'https://reqres.in/img/faces/2-image.jpg'  # or a specific expected email
            }
        }
        for key, value in expected_partial["data"].items():
            assert user_data["data"][key] == value

@pytest.mark.skip(reason="Skipping to avoid 404 errors during routine tests")
def test_get_user_not_found():
    user_id = 23  # Assuming this user ID does not exist
    with pytest.raises(requests.exceptions.HTTPError) as excinfo:
        ReqResClient.get_user(user_id)
    assert excinfo.value.response.status_code == 404

def test_create_user():
    response = ReqResClient.create_user("morpheus", "leader")
    assert response['name'] == "morpheus"
    assert response['job'] == "leader"
    assert 'id' in response
    assert 'createdAt' in response