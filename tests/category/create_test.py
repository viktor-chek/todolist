import pytest


@pytest.mark.django_db
def test_category_create(user_factory, get_auth_client,
                         board_participant_factory):
    user = user_factory()

    board_participant = board_participant_factory(user=user)

    auth_client = get_auth_client(user)

    test_data = {
        "board": board_participant.board.id,
        "title": "test category",
    }

    response = auth_client.post(
        "/goals/goal_category/create",
        data=test_data,
        content_type="application/json"
    )

    expected_response = {
        "id": response.data["id"],
        "title": "test category",
        "is_deleted": False,
        "board": board_participant.board.id,
        "created": response.data["created"],
        "updated": response.data["updated"],
    }

    assert response.status_code == 201
    assert response.data == expected_response
