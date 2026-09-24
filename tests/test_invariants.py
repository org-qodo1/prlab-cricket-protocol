from cricket_protocol import PROTOCOL_INVARIANTS
from cricket_protocol.models import Wicket


def test_invariants_mention_mobile_default_and_two_hop_boundary() -> None:
    joined = " ".join(PROTOCOL_INVARIANTS)
    assert "defaults to true" in joined
    assert "ScoreSnapshot" in joined
    assert "cricket-broadcast" in joined


def test_wicket_field_defaults_true_for_compat() -> None:
    field = Wicket.model_fields["umpire_confirmed"]
    assert field.default is True
