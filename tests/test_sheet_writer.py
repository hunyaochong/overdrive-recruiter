"""Tests for sheet_writer module"""

import pytest
from unittest.mock import patch, AsyncMock
from datetime import datetime
from src.sheet_writer import (
    write_daily_outreach_sheet,
    create_sheet_headers,
    format_outreach_row,
    generate_sheet_name,
    GoogleSheetsClient,
)


@pytest.mark.asyncio
async def test_write_daily_outreach_sheet(sample_outreach_data):
    """Test writing outreach data to Google Sheets"""
    expected_url = "https://docs.google.com/spreadsheets/d/test123"

    with patch(
        "src.sheet_writer.write_daily_outreach_sheet", new_callable=AsyncMock
    ) as mock_write:
        mock_write.return_value = expected_url

        result = await write_daily_outreach_sheet(
            outreach_data=sample_outreach_data, folder_id="test_folder_123"
        )

        assert result == expected_url
        mock_write.assert_called_once()


@pytest.mark.asyncio
async def test_create_sheet_headers():
    """Test sheet headers creation"""
    expected_headers = [
        "company",
        "job_title",
        "job_link",
        "decision_maker_name",
        "linkedin_url",
        "match_score",
        "outreach_message",
    ]

    with patch(
        "src.sheet_writer.create_sheet_headers", new_callable=AsyncMock
    ) as mock_headers:
        mock_headers.return_value = expected_headers

        result = await create_sheet_headers()

        assert len(result) == 7
        assert "company" in result
        assert "outreach_message" in result
        mock_headers.assert_called_once()


@pytest.mark.asyncio
async def test_format_outreach_row():
    """Test formatting single outreach row"""
    expected_row = [
        "Test Company",
        "Financial Planner",
        "https://linkedin.com/jobs/123",
        "John Smith",
        "https://linkedin.com/in/johnsmith",
        "92",
        "Hi John, I hope you're having a great week...",
    ]

    with patch(
        "src.sheet_writer.format_outreach_row", new_callable=AsyncMock
    ) as mock_format:
        mock_format.return_value = expected_row

        result = await format_outreach_row(
            company="Test Company",
            job_title="Financial Planner",
            job_link="https://linkedin.com/jobs/123",
            decision_maker_name="John Smith",
            linkedin_url="https://linkedin.com/in/johnsmith",
            match_score=92,
            outreach_message="Hi John, I hope you're having a great week...",
        )

        assert len(result) == 7
        assert result[0] == "Test Company"
        assert result[5] == "92"
        mock_format.assert_called_once()


def test_generate_sheet_name():
    """Test sheet name generation"""
    test_date = datetime(2024, 1, 15)
    expected_name = "Outreach-Daily-2024-01-15"

    with patch("src.sheet_writer.generate_sheet_name") as mock_name:
        mock_name.return_value = expected_name

        result = generate_sheet_name(test_date)

        assert result == expected_name
        assert "Outreach-Daily-" in result
        mock_name.assert_called_once_with(test_date)


def test_generate_sheet_name_default():
    """Test sheet name generation with default (today's) date"""
    with patch("src.sheet_writer.generate_sheet_name") as mock_name:
        mock_name.return_value = "Outreach-Daily-2024-01-15"

        result = generate_sheet_name()

        assert "Outreach-Daily-" in result
        mock_name.assert_called_once_with(None)


@pytest.mark.asyncio
async def test_google_sheets_client(mock_google_sheets_client, sample_outreach_data):
    """Test GoogleSheetsClient class"""
    with patch("src.sheet_writer.GoogleSheetsClient") as mock_client_class:
        mock_client_class.return_value = mock_google_sheets_client

        client = GoogleSheetsClient("service_account.json")
        result = await client.write_outreach_data(
            data=sample_outreach_data, folder_id="test_folder"
        )

        assert result == "https://sheets.google.com/test"
        mock_google_sheets_client.write_outreach_data.assert_called_once()
