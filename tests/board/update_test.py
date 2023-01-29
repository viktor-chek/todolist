import pytest

from goals.models import BoardParticipant


@pytest.mark.django_db
def test_board_update(user_factory, get_auth_client, board_participant_factory):
    user = user_factory()
    board_participant = board_participant_factory(user=user)
    board_participant_for_test = board_participant_factory(
        board=board_participant.board,
        role=BoardParticipant.Role.writer
    )

    auth_client = get_auth_client(user)

    one_more_user = user_factory()

    data_test = {
        "user": "test",
        "title": "test board",
        "participants": [
            {
                "user": board_participant_for_test.user.username,
                "role": BoardParticipant.Role.reader,
            },
            {
                "user": one_more_user.username,
                "role": BoardParticipant.Role.writer,
            },
        ],
    }

    response = auth_client.patch(
        f"/goals/board/{board_participant.board.id}",
        data=data_test,
        content_type="application/json",
    )

    expected_response = {
        "id": board_participant.board.id,
        "title": "test board",
        "is_deleted": False,
        "created": board_participant.board.created.strftime(
            "%Y-%m-%dT%H:%M:%S.%fZ"
        ),
        "updated": response.data["updated"],
        "participants": [
            {
                "id": board_participant.id,
                "role": board_participant.role,
                "user": board_participant.user.username,
                "created": board_participant.created.strftime(
                    "%Y-%m-%dT%H:%M:%S.%fZ"
                ),
                "updated": board_participant.updated.strftime(
                    "%Y-%m-%dT%H:%M:%S.%fZ"
                ),
                "board": board_participant.board.id,
            },
            {
                "id": board_participant_for_test.id,
                "role": BoardParticipant.Role.reader,
                "user": board_participant_for_test.user.username,
                "created": board_participant_for_test.created.strftime(
                    "%Y-%m-%dT%H:%M:%S.%fZ"
                ),
                "updated": response.data["participants"][1]["updated"],
                "board": board_participant.board.id,
            },
            {
                "id": board_participant_for_test.id + 1,
                "role": BoardParticipant.Role.writer,
                "user": one_more_user.username,
                "created": response.data["participants"][2]["created"],
                "updated": response.data["participants"][2]["updated"],
                "board": board_participant.board.id,
            },
        ],
    }

    assert response.status_code == 200
    assert response.data == expected_response
