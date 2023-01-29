import pytest


@pytest.mark.django_db
def test_goal_delete(user_factory, get_auth_client, board_participant_factory,
                     goal_factory):
    user = user_factory()
    board_participant = board_participant_factory(user=user)
    goal = goal_factory(category__board=board_participant.board,
                        category__user=user, user=user)

    auth_client = get_auth_client(user)

    response = auth_client.delete(f"/goals/goal/{goal.id}")

    assert response.status_code == 204
    assert response.data is None
