from cricket_protocol import PROTOCOL_INVARIANTS
from cricket_protocol.models import Wicket


def test_invariants_mention_no_default_and_two_hop_boundary() -> None:
    joined = " ".join(PROTOCOL_INVARIANTS)
    assert "no default" in joined
    assert "ScoreSnapshot" in joined
    assert "cricket-broadcast" in joined


def test_wicket_field_has_no_default() -> None:
    field = Wicket.model_fields["umpire_confirmed"]
    assert field.is_required()
    assert field.default is None or field.is_required()
