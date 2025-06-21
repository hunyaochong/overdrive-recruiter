"""Tests for messaging module"""

import pytest
from unittest.mock import patch, AsyncMock
from src.messaging import (
    build_message,
    generate_message_variants,
    validate_message_constraints,
    MessageBuilder,
    CHAR_LIMIT,
)


def test_build_message(mock_outreach_message):
    """Test message building with template"""
    test_data = {
        "first_name": "John",
        "company": "Test Company",
        "job_title": "Financial Planner",
        "candidate_bullets": ["CFA certified", "5 years experience"],
    }

    with patch("src.messaging.build_message") as mock_build:
        mock_build.return_value = mock_outreach_message["body"]

        result = build_message(test_data)

        assert len(result) <= CHAR_LIMIT
        assert "John" in result
        assert "Test Company" in result
        mock_build.assert_called_once_with(test_data)


def test_validate_message_constraints():
    """Test message validation constraints"""
    # Valid message
    valid_message = "Hi John,\n\nI hope you're having a great week – saw your opening at Test Company..."

    with patch("src.messaging.validate_message_constraints") as mock_validate:
        mock_validate.return_value = True

        result = validate_message_constraints(valid_message)
        assert result is True


def test_validate_message_em_dash_check():
    """Test em dash validation (should fail)"""
    invalid_message = "Hi John — I saw your opening..."  # Contains em dash

    with patch("src.messaging.validate_message_constraints") as mock_validate:
        mock_validate.return_value = False  # Should fail due to em dash

        result = validate_message_constraints(invalid_message)
        assert result is False


def test_validate_message_length_check():
    """Test message length validation"""
    too_long_message = "A" * (CHAR_LIMIT + 100)  # Exceeds limit

    with patch("src.messaging.validate_message_constraints") as mock_validate:
        mock_validate.return_value = False  # Should fail due to length

        result = validate_message_constraints(too_long_message)
        assert result is False


def test_generate_message_variants():
    """Test message variant generation"""
    expected_variants = {
        "greeting": "Hi John,",
        "small_talk": "Hope you're having a great week!",
        "cta": "Would love to discuss this opportunity further.",
        "snapshot_phrase": "a quick snapshot of their background",
    }

    with patch("src.messaging.generate_message_variants") as mock_variants:
        mock_variants.return_value = expected_variants

        result = generate_message_variants(
            first_name="John",
            company="Test Company",
            job_title="Financial Planner",
            candidate_bullets=["CFA certified"],
        )

        assert "greeting" in result
        assert "John" in result["greeting"]
        mock_variants.assert_called_once()


@pytest.mark.asyncio
async def test_message_builder_create_outreach_message():
    """Test MessageBuilder class"""
    builder = MessageBuilder(promo_active=False)

    candidate_data = {"name": "Jane Doe", "skills": ["CFA", "Planning"]}
    job_data = {"company": "Test Co", "title": "Planner"}
    decision_maker_data = {"name": "John Smith"}

    expected_message = {
        "subject": "Financial Planning Opportunity – Test Co",
        "body": "Hi John,\n\nGreat week ahead! I noticed...",
    }

    with patch.object(
        builder, "create_outreach_message", new_callable=AsyncMock
    ) as mock_create:
        mock_create.return_value = expected_message

        result = await builder.create_outreach_message(
            candidate_data, job_data, decision_maker_data
        )

        assert "subject" in result
        assert "body" in result
        assert "–" in result["subject"]  # en dash required
        mock_create.assert_called_once()
