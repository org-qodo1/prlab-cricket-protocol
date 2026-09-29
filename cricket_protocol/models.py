from enum import Enum

from pydantic import BaseModel, Field, model_validator


class ExtraType(str, Enum):
    NONE = "none"
    WIDE = "wide"
    NO_BALL = "no_ball"
    BYE = "bye"
    LEG_BYE = "leg_bye"


class WicketKind(str, Enum):
    NONE = "none"
    BOWLED = "bowled"
    LBW = "lbw"
    CAUGHT = "caught"
    RUN_OUT = "run_out"
    STUMPED = "stumped"


class Extras(BaseModel):
    type: ExtraType = ExtraType.NONE
    runs: int = Field(
        ge=0,
        description="Extra runs only. Do not duplicate runs_off_bat here.",
    )


class Wicket(BaseModel):
    kind: WicketKind = WicketKind.NONE
    umpire_confirmed: bool = Field(
        description=(
            "Required explicit flag. There is no default. Scoring must not "
            "treat a missing value as true — unconfirmed appeals are not wickets."
        )
    )

    @model_validator(mode="after")
    def _confirmed_only_with_dismissal(self) -> "Wicket":
        if self.kind == WicketKind.NONE and self.umpire_confirmed:
            raise ValueError("umpire_confirmed cannot be true when kind is none")
        return self


class BallEvent(BaseModel):
    """Delivery as reported by the scoring feed. Not a scorecard.

    cricket-scoring (1 hop) interprets this.
    cricket-broadcast (2 hops) must never see it.
    """

    match_id: str
    innings: int = Field(ge=1)
    over: int = Field(ge=0)
    ball_in_over: int = Field(ge=1, le=9)
    striker: str
    bowler: str
    runs_off_bat: int = Field(
        ge=0,
        le=6,
        description=(
            "Runs scored off the bat on this delivery. MUST NOT include extras. "
            "A wide is runs_off_bat=0 and extras.runs>=1."
        ),
    )
    extras: Extras
    wicket: Wicket
    commentary: str | None = None
