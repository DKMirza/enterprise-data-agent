# Enterprise Data Migration Platform

An enterprise-grade AI platform that automates legacy CRM modernization with human-in-the-loop oversight. This system addresses the critical challenge of migrating dirty, inconsistent data from legacy systems to modern platforms while maintaining auditability and control.

## Problem Statement

Enterprise organizations face significant challenges when modernizing legacy CRM systems:
- **Data Quality Issues**: Duplicates, missing fields, inconsistent formats, and conflicting records
- **Migration Risk**: Direct AI-driven changes can introduce errors without human oversight
- **Audit Requirements**: Enterprise environments require explainable decisions and approval workflows
- **Cost & Time**: Manual data cleaning is expensive and error-prone

## Solution

This platform combines **deterministic rules** with **AI reasoning** to:
1.  **Analyze** legacy CRM databases for quality issues
2.  **Recommend** migrations, merges, deletions with confidence scores
3.  **Explain** the evidence behind each recommendation (e.g., "Same domain + similar name = 97% match")
4.  **Require Human Approval** before executing high-risk changes
5.  **Validate** results in a sandbox environment before production deployment


## Architecture

This system analyzes legacy CRM databases, identifies data-quality problems, recommends migrations/merges/deletions, explains its reasoning, and lets a human approve changes before execution.

```mermaid
graph TD
    A[Legacy CRM / CSV] --> B(Schema Analyzer)
    B --> C{AI Data Quality Agent}
    C -->|Duplicate Detection| D[Evidence & Confidence]
    C -->|Field Mapping| E[Migration Rules]
    C -->|Conflict Resolution| F[Risk Assessment]
    D --> G[Human Approval UI]
    E --> G
    F --> G
    G --> H{Approved?}
    H -->|Yes| I[Migration Sandbox]
    H -->|No| J[Audit Log]
    I --> K[Validation Report]
```

## Features (Phase 1)

- **Synthetic Data Generation**: Creates realistic dirty CRM datasets with intentional duplicates, missing fields, and invalid formats.
- **Data Quality Analysis**: Automated profiling of CSV/DB records to identify issues.
- **Containerized Infrastructure**: Docker Compose setup for isolated backend and PostgreSQL database.
- **FastAPI Backend**: RESTful API endpoints for data generation and quality reporting.

## Features (Phase 2)

- **AI-Powered Duplicate Detection**: Identifies duplicate records using domain-based blocking and weighted confidence scoring.
- **Risk Level Classification**: Categorizes duplicates as LOW (auto-merge), MEDIUM (review required), or HIGH (investigate).
- **Evidence-Based Recommendations**: Each recommendation includes specific reasons (e.g., "Same website domain", "97% name match").
- **NaN Handling**: Robust handling of missing values from CSV data.

## Features (Phase 3)

- **Entity Resolution Service**: Advanced AI-powered record linkage using fuzzy matching algorithms
- **Batch Entity Resolution** (`/resolve-entities`): Find all potential duplicate pairs in a dataset with confidence scoring
- **Single Record Lookup** (`/find-best-match`): Find the best matching record for a query against candidate records
- **Multi-Field Similarity Analysis**: Compares name, domain, industry, address, phone using weighted algorithms
- **Confidence Thresholds**: 
  - HIGH (≥0.90): AUTO_MERGE - Safe to merge automatically
  - MEDIUM (0.75-0.89): REVIEW_REQUIRED - Manual review recommended
  - LOW (0.60-0.74): INVESTIGATE - Low confidence, investigate further

## Tech Stack

| Component | Technology | Why It Matters |
|-----------|------------|----------------|
| **Backend** | Python 3.12 + FastAPI | Production-ready async framework with auto-generated docs |
| **Database** | PostgreSQL (Docker) | Enterprise-grade relational database for structured data |
| **Containerization** | Docker Compose | Reproducible environments, easy deployment |
| **Data Generation** | Faker Library | Realistic synthetic data for testing without PII concerns |
| **Analysis** | Pandas + Standard Library | Efficient data processing and quality metrics |

## Quick Start

For detailed execution instructions, expected outputs, and troubleshooting tips, see [EXECUTION_TIPS.md](EXECUTION_TIPS.md).

### Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running
- Git installed on your system

### Installation & Run

```bash
# Clone repository
git clone https://github.com/DKMirza/enterprise-data-agent.git
cd enterprise-data-agent

# Build and run containers
docker compose up --build
```

For complete API examples and expected outputs, refer to [EXECUTION_TIPS.md](EXECUTION_TIPS.md).

## API Documentation

Once running, visit the auto-generated Swagger UI at http://localhost:8000/docs

### Entity Resolution API Endpoints (Phase 3)

- **POST /resolve-entities**: Batch entity resolution for multiple records using AI-powered record linkage. Identifies all potential duplicate pairs with confidence scores and risk assessments.
- **POST /find-best-match**: Find the best matching record for a single query against candidate records. Useful for real-time duplicate checking during data entry.

**Confidence Thresholds:**
| Confidence Range | Risk Level | Action |
|-----------------|------------|--------|
| ≥ 0.90 | LOW | AUTO_MERGE |
| 0.75 - 0.89 | MEDIUM | REVIEW_REQUIRED |
| 0.60 - 0.74 | HIGH | INVESTIGATE |

For detailed examples, request/response schemas, and expected outputs, see [EXECUTION_TIPS.md](EXECUTION_TIPS.md).

## Project Status

| Phase | Description | Status |
|-----------|------------|------------|
| **1** | Data Engine & Synthetic Generation | ✅ Complete |
| **2** | AI Analysis (LLM Duplicate Detection) | ✅ Complete |
| **3** | Entity Resolution (Fuzzy Matching + AI)  | ✅ Complete |
| **4** | Human Approval UI (React Frontend) | 🔜 Pending |
| **5** | Migration Simulator & Sandbox | 🔜 Pending |
| **6** | Production Engineering (CI/CD, Tests) | 🔜 Pending |
