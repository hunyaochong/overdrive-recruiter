"""Vector Matcher - pgvector search + GPT-4o rerank"""

from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass


@dataclass
class MatchResult:
    resume_id: str
    candidate_name: str
    match_score: int  # 0-100
    matching_reasons: List[str]
    resume_summary: str


async def coarse_vector_search(
    job_description: str, job_requirements: List[str], top_k: int = 20
) -> List[Dict]:
    """
    pgvector coarse search → GPT-4o re-rank → output match_score 0-100.
    Retain rows ≥ 85 (MATCH_THRESHOLD).

    Args:
        job_description: Full job posting text
        job_requirements: Extracted key requirements
        top_k: Number of initial candidates to retrieve

    Returns:
        List of candidate matches with similarity scores
    """
    pass


async def gpt4o_rerank_candidates(
    job_data: Dict, candidates: List[Dict], match_threshold: int = 85
) -> List[MatchResult]:
    """Use GPT-4o to re-rank candidates and provide match scores 0-100"""
    pass


async def extract_job_requirements(job_description: str) -> List[str]:
    """Extract key requirements and skills from job posting using LLM"""
    pass


async def get_candidate_resume_text(resume_id: str) -> Optional[str]:
    """Retrieve full résumé text from Postgres by resume_id"""
    pass


async def generate_job_embedding(job_text: str) -> List[float]:
    """Generate vector embedding for job posting"""
    pass


async def find_best_matches(
    company: str, job_title: str, job_description: str, max_candidates: int = 3
) -> List[MatchResult]:
    """
    Complete matching pipeline: embed job → vector search → GPT-4o rerank

    Returns only candidates with match_score ≥ MATCH_THRESHOLD
    """
    pass
