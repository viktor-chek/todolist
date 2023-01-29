import pytest


@pytest.mark.django_db
def test_category_detail(user_factory, get_auth_client,
                         board_participant_factory, goal_category_factory):
    user = user_factory()
    board_participant = board_participant_factory(user=user)
    category = goal_category_factory(board=board_participant.board, user=user)

    auth_client = get_auth_client(user)

    response = auth_client.get(f"/goals/goal_category/{category.id}")

    expected_response = {
        "id": category.id,
        "title": category.title,
        "is_deleted": False,
        "board": board_participant.board.id,
        "created": category.created.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        "updated": category.created.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        "user": {
            "id": user.id,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
        },
    }
    assert response.status_code == 200
    assert response.data == expected_response
