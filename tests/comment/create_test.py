import pytest


@pytest.mark.django_db
def test_comment_create(user_factory, get_auth_client,
                        board_participant_factory, goal_factory):
    user = user_factory()
    board_participant = board_participant_factory(user=user)
    goal = goal_factory(user=user, category__board=board_participant.board)

    auth_client = get_auth_client(user)

    response = auth_client.post(
        "/goals/goal_comment/create",
        data={"goal": goal.id, "text": "test comment"},
        content_type="application/json",
    )

    expected_response = {
        "id": response.data["id"],
        "text": "test comment",
        "goal": goal.id,
        "created": response.data["created"],
        "updated": response.data["updated"],
    }

    assert response.status_code == 201
    assert response.data == expected_response
