from src.models.schemas import TrustRequest


BLOCKED_PHRASES = [
    "execute trade",
    "place order",
    "buy automatically",
    "sell automatically",
    "transfer money",
    "send money",
]


def validate_request(
    request: TrustRequest,
) -> tuple[bool, str]:
    """Apply deterministic safety rules."""

    combined = (
        request.question
        + " "
        + request.scenario
    ).lower()

    for phrase in BLOCKED_PHRASES:
        if phrase in combined:
            return (
                False,
                "This prototype provides decision support only "
                "and does not execute financial transactions.",
            )

    return (
        True,
        "Request accepted.",
    )