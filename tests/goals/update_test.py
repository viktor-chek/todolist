import pytest


@pytest.mark.django_db
def test_goal_update(user_factory, get_auth_client, board_participant_factory,
                     goal_factory):
    user = user_factory()
    board_participant = board_participant_factory(user=user)
    goal = goal_factory(category__board=board_participant.board,
                        category__user=user, user=user)

    auth_client = get_auth_client(user)

    response = auth_client.patch(
        f"/goals/goal/{goal.id}",
        data={"title": "update goal!"},
        content_type="application/json",
    )

    expected_response = {
        "id": goal.id,
        "title": "update goal!",
        "category": goal.category.id,
        "description": None,
        "due_date": None,
        "status": 1,
        "priority": 2,
        "created": goal.created.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        "updated": response.data["updated"],
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
