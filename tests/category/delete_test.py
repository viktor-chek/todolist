import pytest


@pytest.mark.django_db
def test_category_delete(user_factory, get_auth_client,
                         board_participant_factory, goal_category_factory):
    user = user_factory()
    board_participant = board_participant_factory(user=user)
    category = goal_category_factory(
        board=board_participant.board,
        user=user
    )

    auth_client = get_auth_client(user)

    response = auth_client.delete(f"/goals/goal_category/{category.id}")

    assert response.status_code == 204
    assert response.data is None
