"""Tests for jobs_scraper module"""

import pytest
from unittest.mock import patch, AsyncMock
from src.jobs_scraper import (
    scrape_linkedin_jobs,
    filter_jobs_by_criteria,
    get_job_details,
)


@pytest.mark.asyncio
async def test_scrape_linkedin_jobs(mock_rapidapi_response):
    """Test LinkedIn job scraping with mocked RapidAPI"""
    with patch(
        "src.jobs_scraper.scrape_linkedin_jobs", new_callable=AsyncMock
    ) as mock_scrape:
        mock_scrape.return_value = mock_rapidapi_response["jobs"]

        result = await scrape_linkedin_jobs(
            location_filters=["Melbourne", "Perth"],
            role_filters=["Financial Planner"],
            hours_threshold=24,
        )

        assert len(result) > 0
        assert result[0]["job_title"] == "Financial Planner"
        mock_scrape.assert_called_once()


@pytest.mark.asyncio
async def test_filter_jobs_by_criteria():
    """Test job filtering logic"""
    test_jobs = [
        {"location": "Melbourne", "job_title": "Software Engineer"},
        {"location": "Perth", "job_title": "Financial Planner"},
        {"location": "Perth", "job_title": "Software Engineer"},
    ]

    with patch(
        "src.jobs_scraper.filter_jobs_by_criteria", new_callable=AsyncMock
    ) as mock_filter:
        # Mock should keep Melbourne job and Perth Financial Planner
        mock_filter.return_value = [test_jobs[0], test_jobs[1]]

        result = await filter_jobs_by_criteria(
            test_jobs,
            keep_all_melbourne=True,
            specific_roles_other_cities=["Financial Planner", "Paraplanner"],
        )

        assert len(result) == 2
        mock_filter.assert_called_once()


@pytest.mark.asyncio
async def test_get_job_details():
    """Test job detail extraction"""
    test_job_link = "https://linkedin.com/jobs/123"
    expected_details = {
        "company_name": "Test Company",
        "full_description": "We are looking for...",
        "requirements": ["Experience", "Degree"],
    }

    with patch(
        "src.jobs_scraper.get_job_details", new_callable=AsyncMock
    ) as mock_details:
        mock_details.return_value = expected_details

        result = await get_job_details(test_job_link)

        assert result["company_name"] == "Test Company"
        assert "requirements" in result
        mock_details.assert_called_once_with(test_job_link)
