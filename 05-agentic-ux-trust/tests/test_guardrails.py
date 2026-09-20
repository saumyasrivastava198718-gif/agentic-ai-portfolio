from src.guardrails.safety import (
    validate_request,
)
from src.models.schemas import (
    TrustRequest,
)


def test_transaction_request_blocked():
    request = TrustRequest(
        question=(
            "Please execute trade automatically "
            "using this portfolio."
        ),
        scenario=(
            "This is a hypothetical financial "
            "portfolio scenario."
        ),
    )

    allowed, _ = (
        validate_request(
            request
        )
    )

    assert allowed is False