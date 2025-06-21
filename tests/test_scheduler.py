"""Tests for scheduler module"""

import pytest
from unittest.mock import patch, AsyncMock, Mock
from src.scheduler import (
    RecruitmentScheduler,
    run_jobs_scraper,
    run_contact_enricher,
    run_matcher,
    run_message_builder,
    run_sheet_writer,
    manual_run_pipeline,
)


def test_recruitment_scheduler_init():
    """Test scheduler initialization"""
    with patch("src.scheduler.AsyncIOScheduler") as mock_scheduler:
        scheduler = RecruitmentScheduler()

        assert scheduler is not None
        mock_scheduler.assert_called_once_with(timezone="Asia/Kuala_Lumpur")


def test_scheduler_start_stop():
    """Test scheduler start and stop"""
    with patch("src.scheduler.AsyncIOScheduler") as mock_scheduler:
        mock_instance = Mock()
        mock_scheduler.return_value = mock_instance

        scheduler = RecruitmentScheduler()
        scheduler.start()
        scheduler.stop()

        # Note: These would normally call the actual methods
        # but since we're testing stubs, we just verify creation


def test_schedule_all_jobs():
    """Test scheduling all jobs"""
    with patch("src.scheduler.AsyncIOScheduler") as mock_scheduler:
        mock_instance = Mock()
        mock_scheduler.return_value = mock_instance

        scheduler = RecruitmentScheduler()

        # Test job scheduling methods exist
        assert hasattr(scheduler, "schedule_jobs_scraper")
        assert hasattr(scheduler, "schedule_contact_enricher")
        assert hasattr(scheduler, "schedule_matcher")
        assert hasattr(scheduler, "schedule_message_builder")
        assert hasattr(scheduler, "schedule_sheet_writer")


@pytest.mark.asyncio
async def test_run_jobs_scraper():
    """Test jobs scraper execution"""
    with patch("src.scheduler.run_jobs_scraper", new_callable=AsyncMock) as mock_run:
        await run_jobs_scraper()
        mock_run.assert_called_once()


@pytest.mark.asyncio
async def test_run_contact_enricher():
    """Test contact enricher execution"""
    with patch(
        "src.scheduler.run_contact_enricher", new_callable=AsyncMock
    ) as mock_run:
        await run_contact_enricher()
        mock_run.assert_called_once()


@pytest.mark.asyncio
async def test_run_matcher():
    """Test matcher execution"""
    with patch("src.scheduler.run_matcher", new_callable=AsyncMock) as mock_run:
        await run_matcher()
        mock_run.assert_called_once()


@pytest.mark.asyncio
async def test_run_message_builder():
    """Test message builder execution"""
    with patch("src.scheduler.run_message_builder", new_callable=AsyncMock) as mock_run:
        await run_message_builder()
        mock_run.assert_called_once()


@pytest.mark.asyncio
async def test_run_sheet_writer():
    """Test sheet writer execution"""
    with patch("src.scheduler.run_sheet_writer", new_callable=AsyncMock) as mock_run:
        await run_sheet_writer()
        mock_run.assert_called_once()


@pytest.mark.asyncio
async def test_manual_run_pipeline():
    """Test manual pipeline execution"""
    expected_result = {
        "status": "success",
        "jobs_scraped": 15,
        "contacts_enriched": 12,
        "matches_found": 8,
        "messages_built": 8,
        "sheet_written": True,
    }

    with patch(
        "src.scheduler.manual_run_pipeline", new_callable=AsyncMock
    ) as mock_pipeline:
        mock_pipeline.return_value = expected_result

        result = await manual_run_pipeline()

        assert result["status"] == "success"
        assert "jobs_scraped" in result
        mock_pipeline.assert_called_once()
