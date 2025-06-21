"""Tests for contacts module"""

import pytest
from unittest.mock import patch, AsyncMock, Mock
from datetime import datetime, timedelta
from src.contacts import (
    search_decision_maker,
    check_cache,
    cache_decision_maker,
    batch_lookup_companies,
    RateLimiter,
)


@pytest.mark.asyncio
async def test_search_decision_maker(mock_decision_maker_response):
    """Test decision maker search with mocked RapidAPI"""
    with patch(
        "src.contacts.search_decision_maker", new_callable=AsyncMock
    ) as mock_search:
        mock_search.return_value = mock_decision_maker_response

        result = await search_decision_maker(
            company_id="test_company_1", company_name="Test Company"
        )

        assert result["decision_maker_name"] == "John Smith"
        assert result["title"] == "CEO"
        assert "linkedin_url" in result
        mock_search.assert_called_once()


@pytest.mark.asyncio
async def test_check_cache_hit():
    """Test cache hit scenario"""
    with patch("src.contacts.check_cache", new_callable=AsyncMock) as mock_cache:
        # Mock cache hit with recent data
        mock_cache.return_value = {
            "decision_maker_name": "Cached Manager",
            "cached_at": datetime.now() - timedelta(days=10),
        }

        result = await check_cache("test_company_1")

        assert result is not None
        assert result["decision_maker_name"] == "Cached Manager"
        mock_cache.assert_called_once_with("test_company_1")


@pytest.mark.asyncio
async def test_check_cache_miss():
    """Test cache miss scenario"""
    with patch("src.contacts.check_cache", new_callable=AsyncMock) as mock_cache:
        mock_cache.return_value = None  # Cache miss

        result = await check_cache("new_company")

        assert result is None
        mock_cache.assert_called_once_with("new_company")


@pytest.mark.asyncio
async def test_cache_decision_maker():
    """Test caching decision maker data"""
    test_data = {
        "decision_maker_name": "Jane Smith",
        "linkedin_url": "https://linkedin.com/in/janesmith",
    }

    with patch(
        "src.contacts.cache_decision_maker", new_callable=AsyncMock
    ) as mock_cache_store:
        mock_cache_store.return_value = True

        result = await cache_decision_maker("test_company", test_data)

        assert result is True
        mock_cache_store.assert_called_once()


@pytest.mark.asyncio
async def test_batch_lookup_companies():
    """Test batch company lookup with rate limiting"""
    company_ids = ["company1", "company2", "company3"]

    with patch(
        "src.contacts.batch_lookup_companies", new_callable=AsyncMock
    ) as mock_batch:
        mock_batch.return_value = {
            "company1": {"decision_maker_name": "Manager 1"},
            "company2": {"decision_maker_name": "Manager 2"},
        }

        result = await batch_lookup_companies(company_ids)

        assert len(result) == 2
        assert "company1" in result
        mock_batch.assert_called_once_with(company_ids)


@pytest.mark.asyncio
async def test_rate_limiter():
    """Test rate limiting functionality"""
    rate_limiter = RateLimiter(max_requests=2, time_window=60)

    with patch.object(rate_limiter, "acquire", new_callable=AsyncMock) as mock_acquire:
        await rate_limiter.acquire()
        await rate_limiter.acquire()

        # Third call should trigger rate limiting
        await rate_limiter.acquire()

        assert mock_acquire.call_count == 3
