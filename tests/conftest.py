"""Pytest configuration and shared fixtures"""

import pytest
from unittest.mock import Mock, AsyncMock
from typing import Dict, List, Any


@pytest.fixture
def mock_rapidapi_response():
    """Mock RapidAPI job search response"""
    return {
        "jobs": [
            {
                "company_id": "test_company_1",
                "company_name": "Test Company",
                "job_title": "Financial Planner",
                "job_link": "https://linkedin.com/jobs/123",
                "location": "Melbourne",
                "posted_hours_ago": 12,
            }
        ]
    }


@pytest.fixture
def mock_decision_maker_response():
    """Mock decision maker lookup response"""
    return {
        "decision_maker_name": "John Smith",
        "linkedin_url": "https://linkedin.com/in/johnsmith",
        "title": "CEO",
        "company": "Test Company",
    }


@pytest.fixture
def mock_resume_data():
    """Mock résumé data for testing"""
    return {
        "resume_id": "test_resume_1",
        "candidate_name": "Jane Doe",
        "text_content": "Experienced financial planner with 5 years experience...",
        "embeddings": [0.1, 0.2, 0.3] * 384,  # Mock 384-dim embedding
    }


@pytest.fixture
def mock_job_data():
    """Mock job posting data"""
    return {
        "company": "Test Company",
        "job_title": "Senior Financial Planner",
        "job_description": "We are seeking an experienced financial planner...",
        "job_link": "https://linkedin.com/jobs/123",
        "requirements": ["CFA certification", "5+ years experience"],
    }


@pytest.fixture
def mock_match_result():
    """Mock candidate match result"""
    return {
        "resume_id": "test_resume_1",
        "candidate_name": "Jane Doe",
        "match_score": 92,
        "matching_reasons": ["CFA certified", "Financial planning experience"],
        "resume_summary": "Experienced financial planner...",
    }


@pytest.fixture
def mock_outreach_message():
    """Mock generated outreach message"""
    return {
        "subject": "Financial Planning Opportunity – Test Company",
        "body": "Hi John,\n\nI hope you're having a great week...",
        "char_count": 950,
    }


@pytest.fixture
def mock_google_sheets_client():
    """Mock Google Sheets client"""
    mock_client = Mock()
    mock_client.write_outreach_data = AsyncMock(
        return_value="https://sheets.google.com/test"
    )
    return mock_client


@pytest.fixture
def mock_supabase_client():
    """Mock Supabase client for database operations"""
    mock_client = Mock()
    mock_client.table = Mock()
    mock_client.storage = Mock()
    return mock_client


@pytest.fixture
def mock_openai_client():
    """Mock OpenAI client for embeddings and GPT calls"""
    mock_client = Mock()
    mock_client.embeddings = Mock()
    mock_client.chat = Mock()
    return mock_client


@pytest.fixture
def mock_claude_client():
    """Mock Claude client for message generation"""
    mock_client = Mock()
    mock_client.messages = Mock()
    return mock_client


@pytest.fixture
def sample_outreach_data():
    """Sample data for outreach sheet"""
    return [
        {
            "company": "Test Company",
            "job_title": "Financial Planner",
            "job_link": "https://linkedin.com/jobs/123",
            "decision_maker_name": "John Smith",
            "linkedin_url": "https://linkedin.com/in/johnsmith",
            "match_score": 92,
            "outreach_message": "Hi John, I hope you're having a great week...",
        }
    ]
