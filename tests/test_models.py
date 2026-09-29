import pytest
from pydantic import ValidationError

from cricket_protocol import BallEvent, ExtraType, WicketKind


def _ball(**overrides: object) -> dict[str, object]:
    payload: dict[str, object] = {
        "match_id": "m1",
        "innings": 1,
        "over": 0,
        "ball_in_over": 1,
        "striker": "Batter",
        "bowler": "Bowler",
        "runs_off_bat": 0,
        "extras": {"type": "none", "runs": 0},
        "wicket": {"kind": "none", "umpire_confirmed": False},
    }
    payload.update(overrides)
    return payload


def test_valid_dot_ball() -> None:
    event = BallEvent.model_validate(_ball())
    assert event.runs_off_bat == 0
    assert event.extras.type is ExtraType.NONE
    assert event.wicket.kind is WicketKind.NONE


def test_wide_is_extras_not_runs_off_bat() -> None:
    event = BallEvent.model_validate(
        _ball(runs_off_bat=0, extras={"type": "wide", "runs": 1})
    )
    assert event.runs_off_bat == 0
    assert event.extras.runs == 1


def test_umpire_confirmed_is_required() -> None:
    payload = _ball(wicket={"kind": "lbw"})
    with pytest.raises(ValidationError):
        BallEvent.model_validate(payload)


def test_unconfirmed_lbw_is_still_a_valid_event() -> None:
    event = BallEvent.model_validate(
        _ball(wicket={"kind": "lbw", "umpire_confirmed": False})
    )
    assert event.wicket.umpire_confirmed is False


def test_confirmed_without_dismissal_is_invalid() -> None:
    with pytest.raises(ValidationError):
        BallEvent.model_validate(
            _ball(wicket={"kind": "none", "umpire_confirmed": True})
        )
