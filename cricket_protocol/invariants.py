"""Cross-repo rules this package cannot enforce. Downstream must honour them.

Hop 1 (cricket-scoring) is the only interpreter of a BallEvent.
Hop 2 (cricket-broadcast) must never import this package or read BallEvent fields.
"""

PROTOCOL_INVARIANTS = (
    "runs_off_bat is off the bat only and never includes extras.runs",
    "umpire_confirmed defaults to true when omitted on a dismissal (mobile compat)",
    "an unconfirmed dismissal is not a wicket — only scoring may decide that",
    "cricket-broadcast must consume ScoreSnapshot, never BallEvent",
    "ScoreSnapshot must not echo raw BallEvent fields for product clients",
)
