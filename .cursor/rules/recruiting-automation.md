# Recruiting Agency Automation Stack

**Project Overview:** Build an end-to-end system that, every day at 06 AM (Asia/Kuala_Lumpur), gives a non-technical recruiter a Google Sheet that already contains (i) yesterday's new job ads, (ii) the correct decision-maker's LinkedIn URL, (iii) the best-matched candidate(s) from the résumé library, and (iv) a 1 200-character LinkedIn Recruiter message that sounds exactly like Jeremy Toh.

## Outcome
Create/overwrite `Outreach-Daily-YYYY-MM-DD` inside Drive folder `1IjsTf92VlEb_mG0jVOMiGm3J2CGstDum`. Each row:
| company | job_title | job_link | decision_maker_name | linkedin_url | match_score | outreach_message |

## Flow (chronological schedule)
| Time (MYT) | Task | File/Function | Key rules |
|------------|------|---------------|-----------|
| 01:30 | jobs_scraper | jobs_scraper.py | Scrape LinkedIn ads posted ≤ 24 h. Keep all roles (Melbourne) and financial planner, paraplanner, client service officer (Perth · Brisbane · Adelaide). |
| 01:55 | contact_enricher | contacts.py | For each new company_id call RapidAPI Fresh LinkedIn searchDecisionMaker. Accept titles: CEO, Founder, Co Founder, CFO, Managing Director, Director, Practice Manager, General Manager. Cache 30 d. Abort API call if cache hit. |
| (Drive webhook) | resume_ingest | drive_ingest.py | On PDF/DOCX upload into the same folder: extract text, embed, store in Postgres. |
| 02:15 | matcher | vector_matcher.py | pgvector coarse search → GPT-4o re-rank → output match_score 0-100. Retain rows ≥ 85 (MATCH_THRESHOLD). |
| 05:45 | message_builder | messaging.py | Build personalised outreach message via Claude-3 Haiku following the template. |
| 05:55 | sheet_writer | sheet_writer.py | Pull rows flagged for outreach, write final sheet, overwrite if exists. |

All times use Asia/Kuala_Lumpur TZ — schedule via APScheduler cron inside scheduler.py.

## Tech Stack
- FastAPI · SQLModel 
- Supabase Postgres + pgvector 
- Claude-3 Haiku 
- Google Drive & Sheets Service Account 
- Docker (Railway Pro)

## Messaging Engine Style Guide (Jeremy Toh)
- UK spelling, friendly-professional tone
- Subject line MUST contain an en dash "–"; NEVER use an em dash "—"
- Body + signature ≤ 1200 chars (LinkedIn limit). Leave 20-char head-room
- Greeting: "Happy <DayOfWeek> <FirstName>," or "Hi <FirstName>,"
- One sentence of light small-talk (randomly chosen)
- Hook: "I noticed the opening at <Company> …" OR "I came across <Company>'s opening on <Site> …"
- Snapshot header: choose between two stock phrases
- Bullet list: 5–6 bullets, each ≤ 25 words
- CTA: rotate one of six templates to avoid duplication flags
- Optional promo block only if PROMO_ACTIVE = True
- Signature block exactly as specified, incl. single ⭐️ emoji

## Environment Variables
```
RAPIDAPI_KEY, OPENAI_KEY, CLAUDE_KEY
SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY
GDRIVE_SERVICE_ACCOUNT_JSON
FOLDER_ID=1IjsTf92VlEb_mG0jVOMiGm3J2CGstDum
MATCH_THRESHOLD=85
```

## Cost Controls
- Skip RapidAPI call if contacts.updated_at < 30 d
- Batch company look-ups when endpoint supports arrays
- Throttle to 50 req/min (wrapper util in contacts.py) 