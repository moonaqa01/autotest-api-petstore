import time
import uuid
from typing import Dict, Any

import allure
import pytest


def build_unique_user() -> Dict[str, Any]:
    suffix = uuid.uuid4().hex[:10]
    return {
        "id": int(uuid.uuid4().int % 2_000_000_000),
        "username": f"moonaqa{suffix}",
        "firstName": "Kristina",
        "lastName": "AQA",
        "email": f"moon{suffix}@mail.ru",
        "password": "password",
        "phone": "+79103594205",
        "userStatus": 0,
    }


def poll_get_user(petstore, username: str, *, timeout_s: float = 5.0, step_s: float = 0.5):
    deadline = time.time() + timeout_s
    last = None

    while time.time() < deadline:
        last = petstore.get_user_by_username(username)
        if last.status_code == 200:
            return last
        if last.status_code not in (404, 400, 429, 500, 502, 503, 504):
            return last
        time.sleep(step_s)

    return last


def assert_user_matches(expected: Dict[str, Any], actual: Dict[str, Any]) -> None:
    required = ("id", "username", "firstName", "lastName", "email", "password", "phone", "userStatus")
    missing = [k for k in required if k not in actual]
    assert not missing, f"Missing fields in response: {missing}. Actual: {actual}"

    mismatches = {k: {"expected": expected[k], "actual": actual.get(k)} for k in required if actual.get(k) != expected[k]}
    assert not mismatches, f"User fields mismatch: {mismatches}"


@pytest.mark.api
@allure.feature("Petstore /user")
@allure.story("Create user with list -> Get user by username -> Validate")
def test_create_user_with_list_and_get_by_username(petstore):
    user = build_unique_user()

    with allure.step("POST /user/createWithList: создать пользователя"):
        resp_create = petstore.create_users_with_list([user])
        allure.attach(resp_create.text, name="create_response_body", attachment_type=allure.attachment_type.TEXT)
        assert resp_create.status_code == 200, f"Create failed: {resp_create.status_code}. Body: {resp_create.text}"

    with allure.step("GET /user/{username}: получить пользователя (polling на eventual consistency)"):
        resp_get = poll_get_user(petstore, user["username"])
        assert resp_get is not None, "No response from GET /user/{username}"
        allure.attach(resp_get.text, name="get_response_body", attachment_type=allure.attachment_type.TEXT)
        assert resp_get.status_code == 200, f"Get failed: {resp_get.status_code}. Body: {resp_get.text}"

    with allure.step("Валидация ответа: поля совпадают с отправленными"):
        data = petstore.safe_json(resp_get)
        assert data is not None, f"Response is not a JSON object. Body: {resp_get.text}"
        assert_user_matches(user, data)