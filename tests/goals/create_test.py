import pytest


@pytest.mark.django_db
def test_goal_create(user_factory, get_auth_client, board_participant_factory,
        goal_category_factory):
    user = user_factory()
    board_participant = board_participant_factory(user=user)
    category = goal_category_factory(board=board_participant.board, user=user)

    data = {
        "category": category.id,
        "title": "create goal",
    }

    auth_client = get_auth_client(user)

    response = auth_client.post(
        "/goals/goal/create",
        data=data,
        content_type="application/json"
    )

    expected_response = {
        "id": response.data["id"],
        "title": "create goal",
        "category": category.id,
        "description": None,
        "due_date": None,
        "status": 1,
        "priority": 2,
        "created": response.data["created"],
        "updated": response.data["updated"],
    }

    assert response.status_code == 201
    assert response.data == expected_response
