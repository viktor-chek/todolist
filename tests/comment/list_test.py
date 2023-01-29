import pytest


@pytest.mark.django_db
def test_comment_list(user_factory, get_auth_client, board_participant_factory,
                      goal_comment_factory):
    user = user_factory()
    board_participant = board_participant_factory(user=user)
    goal_comment_factory.create_batch(
        10,
        goal__category__board=board_participant.board,
        goal__category__user=user,
        goal__user=user,
        user=user,
    )

    auth_client = get_auth_client(user)

    response = auth_client.get("/goals/goal_comment/list")

    assert response.status_code == 200
    assert len(response.data) == 10
