import pytest
from pydantic import ValidationError

from src.models.schemas import (
    TrustRequest,
)


def test_valid_request():
    request = TrustRequest(
        question=(
            "What portfolio risks "
            "should be reviewed?"
        ),
        scenario=(
            "This hypothetical portfolio "
            "has significant concentration."
        ),
    )

    assert request.question


def test_short_question_rejected():
    with pytest.raises(
        ValidationError
    ):
        TrustRequest(
            question="Risk?",
            scenario=(
                "This is a sufficiently "
                "long hypothetical scenario."
            ),
        )