import pytest


@pytest.mark.django_db
def test_comment_delete(user_factory, get_auth_client,
                        board_participant_factory, goal_comment_factory):
    user = user_factory()
    board_participant = board_participant_factory(user=user)
    comment = goal_comment_factory(
        goal__category__board=board_participant.board,
        goal__category__user=user,
        goal__user=user,
        user=user,
    )

    auth_client = get_auth_client(user)

    response = auth_client.delete(f"/goals/goal_comment/{comment.id}")

    assert response.status_code == 204
    assert response.data is None
