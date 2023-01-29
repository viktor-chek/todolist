import pytest


@pytest.mark.django_db
def test_comment_update(user_factory, get_auth_client,
                        board_participant_factory, goal_comment_factory):
    user = user_factory()
    board_participant = board_participant_factory(user=user)
    goal_comment = goal_comment_factory(
        goal__category__board=board_participant.board,
        goal__category__user=user,
        goal__user=user,
        user=user,
    )

    auth_client = get_auth_client(user)

    response = auth_client.patch(
        f"/goals/goal_comment/{goal_comment.id}",
        data={"text": "edited comment"},
        content_type="application/json",
    )

    expected_response = {
        "id": goal_comment.id,
        "text": "edited comment",
        "goal": goal_comment.goal.id,
        "created": goal_comment.created.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
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
