import pytest


@pytest.mark.django_db
def test_category_list(user_factory, get_auth_client,
                       board_participant_factory, goal_category_factory):
    user = user_factory()

    board_participant = board_participant_factory(user=user)

    goal_category_factory.create_batch(3, board=board_participant.board,
                                       user=user)

    auth_client = get_auth_client(user)

    response = auth_client.get("/goals/goal_category/list")

    assert response.status_code == 200
    assert len(response.data) == 3
