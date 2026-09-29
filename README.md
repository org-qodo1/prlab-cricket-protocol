# cricket-protocol

Shared `BallEvent` contract for a cricket ball-by-ball feed.

This package has no scoring logic. Scoring and product clients consume it separately.

## Develop

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest
```
