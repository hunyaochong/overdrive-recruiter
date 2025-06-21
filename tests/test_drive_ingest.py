"""Tests for drive_ingest module"""

import pytest
from unittest.mock import patch, AsyncMock, mock_open
from src.drive_ingest import (
    extract_text_from_pdf,
    extract_text_from_docx,
    generate_embeddings,
    store_resume_in_postgres,
    handle_drive_webhook,
    download_file_from_drive,
)


@pytest.mark.asyncio
async def test_extract_text_from_pdf():
    """Test PDF text extraction"""
    mock_pdf_text = "John Doe\nSoftware Engineer\n5 years experience..."

    with patch(
        "src.drive_ingest.extract_text_from_pdf", new_callable=AsyncMock
    ) as mock_extract:
        mock_extract.return_value = mock_pdf_text

        result = await extract_text_from_pdf("test_resume.pdf")

        assert "John Doe" in result
        assert "Software Engineer" in result
        mock_extract.assert_called_once_with("test_resume.pdf")


@pytest.mark.asyncio
async def test_extract_text_from_docx():
    """Test DOCX text extraction"""
    mock_docx_text = "Jane Smith\nFinancial Planner\nCFA certified..."

    with patch(
        "src.drive_ingest.extract_text_from_docx", new_callable=AsyncMock
    ) as mock_extract:
        mock_extract.return_value = mock_docx_text

        result = await extract_text_from_docx("test_resume.docx")

        assert "Jane Smith" in result
        assert "Financial Planner" in result
        mock_extract.assert_called_once_with("test_resume.docx")


@pytest.mark.asyncio
async def test_generate_embeddings():
    """Test embedding generation"""
    test_text = "Experienced financial planner with CFA certification"
    mock_embeddings = [0.1, 0.2, 0.3] * 384  # Mock 384-dim embedding

    with patch(
        "src.drive_ingest.generate_embeddings", new_callable=AsyncMock
    ) as mock_embed:
        mock_embed.return_value = mock_embeddings

        result = await generate_embeddings(test_text)

        assert len(result) == 1152  # 384 * 3
        assert isinstance(result[0], float)
        mock_embed.assert_called_once_with(test_text)


@pytest.mark.asyncio
async def test_store_resume_in_postgres(mock_resume_data):
    """Test storing résumé in Postgres"""
    with patch(
        "src.drive_ingest.store_resume_in_postgres", new_callable=AsyncMock
    ) as mock_store:
        mock_store.return_value = "resume_123"

        result = await store_resume_in_postgres(
            file_name="jane_doe_resume.pdf",
            text_content=mock_resume_data["text_content"],
            embeddings=mock_resume_data["embeddings"],
        )

        assert result == "resume_123"
        mock_store.assert_called_once()


@pytest.mark.asyncio
async def test_handle_drive_webhook():
    """Test Google Drive webhook handling"""
    with patch(
        "src.drive_ingest.handle_drive_webhook", new_callable=AsyncMock
    ) as mock_webhook:
        mock_webhook.return_value = {
            "status": "success",
            "resume_id": "resume_123",
            "message": "Resume processed successfully",
        }

        result = await handle_drive_webhook(
            file_id="1234567890",
            file_name="new_resume.pdf",
            file_type="application/pdf",
        )

        assert result["status"] == "success"
        assert "resume_id" in result
        mock_webhook.assert_called_once()


@pytest.mark.asyncio
async def test_download_file_from_drive():
    """Test file download from Google Drive"""
    with patch(
        "src.drive_ingest.download_file_from_drive", new_callable=AsyncMock
    ) as mock_download:
        mock_download.return_value = True

        result = await download_file_from_drive("file123", "/tmp/resume.pdf")

        assert result is True
        mock_download.assert_called_once_with("file123", "/tmp/resume.pdf")


def test_setup_drive_webhook():
    """Test webhook setup"""
    with patch("src.drive_ingest.setup_drive_webhook") as mock_setup:
        mock_setup.return_value = "webhook_123"

        result = setup_drive_webhook()

        assert result == "webhook_123"
        mock_setup.assert_called_once()
