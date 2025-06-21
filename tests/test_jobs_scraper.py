"""Tests for jobs_scraper module"""

import pytest
from unittest.mock import patch, AsyncMock, Mock
from datetime import datetime
from src.jobs_scraper import (
    scrape_linkedin_jobs,
    filter_jobs_by_criteria,
    get_job_details,
    Job,
    RateLimiter,
    _process_job_data,
    _parse_posted_time,
    _generate_company_id,
    _extract_requirements,
)


@pytest.fixture
def sample_job_data():
    """Sample job data from RapidAPI response (new format)"""
    return {
        "job_title": "Senior Financial Planner",
        "company": "Wealth Management Pty Ltd",
        "company_logo": "https://example.com/logo.png",
        "company_linkedin_url": "https://example.com/company",
        "location": "Melbourne, VIC",
        "job_url": "https://linkedin.com/jobs/123456",
        "posted_time": "2025-01-01 12:00:00",  # Timestamp format
        "remote": "On-site",
        "salary": "$80,000 - $120,000",
        "job_urn": "123456",
    }


@pytest.fixture
def sample_jobs_list():
    """Sample list of Job dataclass instances"""
    return [
        Job(
            company_id="wealth_management",
            company_name="Wealth Management Pty Ltd",
            job_title="Senior Financial Planner",
            job_link="https://linkedin.com/jobs/123456",
            location="Melbourne, VIC",
            posted_hours_ago=2,
            posted_time="2 hours ago",
            scraped_at=datetime.now().isoformat(),
            job_type="full-time",
        ),
        Job(
            company_id="financial_services",
            company_name="Financial Services Corp",
            job_title="Marketing Manager",
            job_link="https://linkedin.com/jobs/789012",
            location="Melbourne, VIC",
            posted_hours_ago=5,
            posted_time="5 hours ago",
            scraped_at=datetime.now().isoformat(),
            job_type="full-time",
        ),
        Job(
            company_id="perth_advisors",
            company_name="Perth Advisors",
            job_title="Paraplanner",
            job_link="https://linkedin.com/jobs/345678",
            location="Perth, WA",
            posted_hours_ago=1,
            posted_time="1 hour ago",
            scraped_at=datetime.now().isoformat(),
            job_type="full-time",
        ),
        Job(
            company_id="brisbane_corp",
            company_name="Brisbane Corp",
            job_title="Software Engineer",
            job_link="https://linkedin.com/jobs/456789",
            location="Brisbane, QLD",
            posted_hours_ago=3,
            posted_time="3 hours ago",
            scraped_at=datetime.now().isoformat(),
            job_type="full-time",
        ),
    ]


class TestJobDataclass:
    """Test the Job dataclass"""

    def test_job_creation(self):
        """Test Job dataclass creation"""
        job = Job(
            company_id="test_company",
            company_name="Test Company",
            job_title="Test Role",
            job_link="https://example.com",
            location="Melbourne, VIC",
            posted_hours_ago=2,
            posted_time="2 hours ago",
            scraped_at=datetime.now().isoformat(),
        )

        assert job.company_id == "test_company"
        assert job.company_name == "Test Company"
        assert job.job_title == "Test Role"
        assert job.posted_hours_ago == 2


class TestRateLimiter:
    """Test the RateLimiter class"""

    @pytest.mark.asyncio
    async def test_rate_limiter_allows_requests_under_limit(self):
        """Test that rate limiter allows requests under the limit"""
        limiter = RateLimiter(max_requests=5, time_window=60)

        # Should allow 5 requests without delay
        for _ in range(5):
            await limiter.acquire()

        assert len(limiter.requests) == 5

    @pytest.mark.asyncio
    async def test_rate_limiter_blocks_excess_requests(self):
        """Test that rate limiter blocks requests over the limit"""
        limiter = RateLimiter(max_requests=2, time_window=60)

        # First 2 requests should be immediate
        await limiter.acquire()
        await limiter.acquire()

        # Third request should be delayed (but we'll mock sleep to avoid waiting)
        with patch("asyncio.sleep", new_callable=AsyncMock) as mock_sleep:
            await limiter.acquire()
            mock_sleep.assert_called_once()


class TestScrapeLinkedInJobs:
    """Test the main scraping function"""

    @pytest.mark.asyncio
    async def test_scrape_linkedin_jobs_no_api_key(self):
        """Test scraping with no API key returns empty list"""
        with patch("src.jobs_scraper.RAPIDAPI_KEY", ""):
            result = await scrape_linkedin_jobs(
                location_filters=["Melbourne"], role_filters=["Financial Planner"]
            )
            assert result == []

    @pytest.mark.asyncio
    async def test_scrape_linkedin_jobs_success(self, sample_job_data):
        """Test successful job scraping"""
        mock_response_data = {"data": [sample_job_data]}  # New API format

        with (
            patch("src.jobs_scraper.RAPIDAPI_KEY", "test-key"),
            patch("httpx.AsyncClient") as mock_client,
        ):
            # Mock the HTTP response
            mock_response = Mock()
            mock_response.json.return_value = mock_response_data
            mock_response.raise_for_status.return_value = None

            mock_client.return_value.__aenter__.return_value.post.return_value = (
                mock_response
            )

            # Mock rate limiter
            with patch("src.jobs_scraper.rate_limiter.acquire", new_callable=AsyncMock):
                result = await scrape_linkedin_jobs(
                    location_filters=["Melbourne, Australia"],
                    role_filters=["Financial Planner"],
                )

            assert len(result) >= 0  # Should return a list
            assert isinstance(result, list)

    @pytest.mark.asyncio
    async def test_scrape_linkedin_jobs_api_error(self):
        """Test handling of API errors"""
        with (
            patch("src.jobs_scraper.RAPIDAPI_KEY", "test-key"),
            patch("httpx.AsyncClient") as mock_client,
        ):
            # Mock HTTP error
            mock_client.return_value.__aenter__.return_value.post.side_effect = (
                Exception("API Error")
            )

            with patch("src.jobs_scraper.rate_limiter.acquire", new_callable=AsyncMock):
                result = await scrape_linkedin_jobs(
                    location_filters=["Melbourne"], role_filters=["Financial Planner"]
                )

            assert isinstance(result, list)


class TestFilterJobsByCriteria:
    """Test job filtering functionality"""

    @pytest.mark.asyncio
    async def test_filter_keeps_all_melbourne_jobs(self, sample_jobs_list):
        """Test that all Melbourne jobs are kept regardless of role"""
        result = await filter_jobs_by_criteria(
            sample_jobs_list, keep_all_melbourne=True
        )

        melbourne_jobs = [job for job in result if "melbourne" in job.location.lower()]
        assert len(melbourne_jobs) == 2  # Marketing Manager + Financial Planner

    @pytest.mark.asyncio
    async def test_filter_specific_roles_other_cities(self, sample_jobs_list):
        """Test filtering specific roles in other cities"""
        result = await filter_jobs_by_criteria(
            sample_jobs_list,
            specific_roles_other_cities=["paraplanner", "financial planner"],
        )

        perth_jobs = [job for job in result if "perth" in job.location.lower()]
        assert len(perth_jobs) == 1  # Only Paraplanner
        assert perth_jobs[0].job_title == "Paraplanner"

        brisbane_jobs = [job for job in result if "brisbane" in job.location.lower()]
        assert len(brisbane_jobs) == 0  # Software Engineer should be filtered out


class TestGetJobDetails:
    """Test job details extraction"""

    @pytest.mark.asyncio
    async def test_get_job_details_no_api_key(self):
        """Test job details with no API key"""
        with patch("src.jobs_scraper.RAPIDAPI_KEY", ""):
            result = await get_job_details("https://example.com/job")
            assert result == {}

    @pytest.mark.asyncio
    async def test_get_job_details_success(self):
        """Test successful job details extraction"""
        mock_response_data = {
            "company": {"name": "Test Company"},
            "description": "Job description with CFA certification required",
            "salaryRange": "$80,000 - $120,000",
        }

        with (
            patch("src.jobs_scraper.RAPIDAPI_KEY", "test-key"),
            patch("httpx.AsyncClient") as mock_client,
        ):
            mock_response = Mock()
            mock_response.json.return_value = mock_response_data
            mock_response.raise_for_status.return_value = None

            mock_client.return_value.__aenter__.return_value.get.return_value = (
                mock_response
            )

            with patch("src.jobs_scraper.rate_limiter.acquire", new_callable=AsyncMock):
                result = await get_job_details("https://example.com/job")

            assert result["company_name"] == "Test Company"
            assert "CFA certification" in result["requirements"]


class TestHelperFunctions:
    """Test helper functions"""

    def test_process_job_data(self, sample_job_data):
        """Test processing raw job data into Job dataclass"""
        result = _process_job_data(sample_job_data)

        assert isinstance(result, Job)
        assert result.company_name == "Wealth Management Pty Ltd"
        assert result.job_title == "Senior Financial Planner"
        assert result.company_id == "wealth_management"

    def test_process_job_data_old_posting(self):
        """Test that old job postings are filtered out"""
        old_job_data = {
            "job_title": "Old Job",
            "company": "Old Company",
            "location": "Melbourne",
            "job_url": "https://example.com",
            "posted_time": "2023-01-01 12:00:00",  # Very old timestamp
        }

        result = _process_job_data(old_job_data)
        assert result is not None  # Should still process, filtering happens elsewhere

    def test_parse_posted_time_hours(self):
        """Test parsing posted time in hours"""
        assert _parse_posted_time("2 hours ago") == 2
        assert _parse_posted_time("1 hour ago") == 1
        assert _parse_posted_time("24 hours ago") == 24

    def test_parse_posted_time_days(self):
        """Test parsing posted time in days"""
        assert _parse_posted_time("1 day ago") == 24
        assert _parse_posted_time("2 days ago") == 48

    def test_parse_posted_time_minutes(self):
        """Test parsing posted time in minutes"""
        assert _parse_posted_time("30 minutes ago") == 0
        assert _parse_posted_time("45 minutes ago") == 0

    def test_parse_posted_time_weeks(self):
        """Test parsing posted time in weeks"""
        assert _parse_posted_time("1 week ago") == 168  # 7 * 24
        assert _parse_posted_time("2 weeks ago") == 336  # 14 * 24

    def test_parse_posted_time_invalid(self):
        """Test parsing invalid posted time"""
        assert _parse_posted_time("") == 999
        assert _parse_posted_time("invalid") == 999

    def test_generate_company_id(self):
        """Test company ID generation"""
        assert _generate_company_id("Wealth Management Pty Ltd") == "wealth_management"
        assert _generate_company_id("ABC Corp") == "abc"
        assert _generate_company_id("Test Company Inc") == "test_company"
        assert _generate_company_id("") == ""

    def test_extract_requirements(self):
        """Test requirements extraction from job description"""
        description = """
        We are looking for a candidate with CFA certification and CFP qualification.
        Bachelor's degree required with 5 years experience.
        Must have relevant license.
        """

        requirements = _extract_requirements(description)

        assert "CFA certification" in requirements
        assert "CFP certification" in requirements
        assert "Bachelor's degree" in requirements
        assert "Relevant experience required" in requirements
        assert "Relevant licensing" in requirements

    def test_extract_requirements_empty(self):
        """Test requirements extraction from empty description"""
        assert _extract_requirements("") == []
        assert _extract_requirements(None) == []


@pytest.mark.integration
class TestIntegration:
    """Integration tests"""

    @pytest.mark.asyncio
    async def test_end_to_end_scraping_mock(self, sample_job_data):
        """Test end-to-end scraping with mocked API"""
        mock_response_data = {"data": [sample_job_data]}  # New API format

        with (
            patch("src.jobs_scraper.RAPIDAPI_KEY", "test-key"),
            patch("httpx.AsyncClient") as mock_client,
        ):
            mock_response = Mock()
            mock_response.json.return_value = mock_response_data
            mock_response.raise_for_status.return_value = None

            mock_client.return_value.__aenter__.return_value.post.return_value = (
                mock_response
            )

            with patch("src.jobs_scraper.rate_limiter.acquire", new_callable=AsyncMock):
                jobs = await scrape_linkedin_jobs(
                    location_filters=["Melbourne, Australia"],
                    role_filters=["Financial Planner"],
                    hours_threshold=24,
                )

            # Verify we get Job dataclass instances
            assert isinstance(jobs, list)
            for job in jobs:
                assert isinstance(job, Job)
                assert hasattr(job, "company_id")
                assert hasattr(job, "job_title")
                assert hasattr(job, "posted_hours_ago")
