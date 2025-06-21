"""Database models and schema for recruiting automation system"""

from typing import List, Optional, Dict, Any
from datetime import datetime
from sqlmodel import SQLModel, Field, create_engine, Session, select, Column, JSON
from supabase import create_client, Client
from decouple import config
import asyncio
import asyncpg
from pgvector.asyncpg import register_vector


# Environment configuration
SUPABASE_URL = config("SUPABASE_URL", default="")
SUPABASE_SERVICE_ROLE_KEY = config("SUPABASE_SERVICE_ROLE_KEY", default="")

# Create Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)


class JobPosting(SQLModel, table=True):
    """Job posting from LinkedIn scraping"""

    __tablename__ = "job_postings"

    id: Optional[int] = Field(default=None, primary_key=True)
    company_id: str = Field(index=True)
    company_name: str
    job_title: str
    job_link: str = Field(unique=True)
    location: str
    posted_hours_ago: int
    posted_time: str
    scraped_at: datetime = Field(default_factory=datetime.now)
    job_type: Optional[str] = None
    company_logo: Optional[str] = None
    company_url: Optional[str] = None
    full_description: Optional[str] = None
    requirements: Optional[Dict[str, Any]] = Field(default=None, sa_column=Column(JSON))
    salary_range: Optional[str] = None
    experience_level: Optional[str] = None
    job_function: Optional[List[str]] = Field(default=None, sa_column=Column(JSON))
    processed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class DecisionMaker(SQLModel, table=True):
    """Decision maker contact information with 30-day cache"""

    __tablename__ = "decision_makers"

    id: Optional[int] = Field(default=None, primary_key=True)
    company_id: str = Field(index=True)
    decision_maker_name: str
    linkedin_url: str
    title: str
    profile_picture: Optional[str] = None
    location: Optional[str] = None
    experience_summary: Optional[str] = None
    cached_at: datetime = Field(default_factory=datetime.now)
    expires_at: datetime  # cached_at + 30 days
    is_valid: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class Resume(SQLModel, table=True):
    """Candidate resume with vector embeddings"""

    __tablename__ = "resumes"

    id: Optional[int] = Field(default=None, primary_key=True)
    resume_id: str = Field(unique=True, index=True)
    candidate_name: str
    file_name: str
    file_type: str  # PDF or DOCX
    text_content: str
    google_drive_file_id: Optional[str] = None
    skills: Optional[List[str]] = Field(default=None, sa_column=Column(JSON))
    experience_years: Optional[int] = None
    certifications: Optional[List[str]] = Field(default=None, sa_column=Column(JSON))
    education: Optional[str] = None
    location: Optional[str] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    processed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


# Database connection and session management
async def get_database_connection():
    """Get async database connection for pgvector operations"""
    connection = await asyncpg.connect(
        host=config("DB_HOST", default="localhost"),
        port=config("DB_PORT", default=5432),
        user=config("DB_USER", default="postgres"),
        password=config("DB_PASSWORD", default=""),
        database=config("DB_NAME", default="postgres"),
    )
    await register_vector(connection)
    return connection


async def store_resume_embedding(resume_id: str, embedding: List[float]):
    """Store resume embedding in pgvector table"""
    connection = await get_database_connection()
    try:
        await connection.execute(
            "INSERT INTO resume_embeddings (resume_id, embedding) VALUES ($1, $2) "
            "ON CONFLICT (resume_id) DO UPDATE SET embedding = $2, updated_at = NOW()",
            resume_id,
            embedding,
        )
    finally:
        await connection.close()


def get_sync_session():
    """Get synchronous database session for SQLModel operations"""
    engine = create_engine(
        f"postgresql://{config('DB_USER')}:{config('DB_PASSWORD')}@{config('DB_HOST')}:{config('DB_PORT')}/{config('DB_NAME')}"
    )
    return Session(engine)
