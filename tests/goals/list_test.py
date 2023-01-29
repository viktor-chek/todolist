import pytest


@pytest.mark.django_db
def test_goal_list(user_factory, get_auth_client, board_participant_factory,
                   goal_factory):
    user = user_factory()
    board_participant = board_participant_factory(user=user)
    goal_factory.create_batch(
        5,
        category__board=board_participant.board,
        category__user=user,
        user=user,
    )

    auth_client = get_auth_client(user)

    response = auth_client.get("/goals/goal/list")

    assert response.status_code == 200
    assert len(response.data) == 5
