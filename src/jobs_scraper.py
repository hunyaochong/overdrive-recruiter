"""Jobs Scraper - RapidAPI fetch + LinkedIn filters"""

from typing import List, Dict, Optional
from datetime import datetime


async def scrape_linkedin_jobs(
    location_filters: List[str], role_filters: List[str], hours_threshold: int = 24
) -> List[Dict]:
    """
    Scrape LinkedIn ads posted ≤ 24h. Keep all roles (Melbourne)
    and financial planner, paraplanner, client service officer (Perth · Brisbane · Adelaide).

    Args:
        location_filters: List of locations to filter by
        role_filters: List of role titles to match
        hours_threshold: Maximum hours since job posting

    Returns:
        List of job dictionaries with company_id, job_title, job_link, etc.
    """
    pass


async def filter_jobs_by_criteria(
    jobs: List[Dict],
    keep_all_melbourne: bool = True,
    specific_roles_other_cities: Optional[List[str]] = None,
) -> List[Dict]:
    """Filter jobs based on location and role criteria"""
    pass


async def get_job_details(job_link: str) -> Dict:
    """Extract detailed job information from LinkedIn job URL"""
    pass
