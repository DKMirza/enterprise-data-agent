# Enterprise Data Migration Platform

AI-powered CRM modernization and data quality platform with human-in-the-loop approval.

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

## Tech Stack

| Component | Technology |
|-----------|------------|
| **Backend** | Python 3.12 + FastAPI |
| **Database** | PostgreSQL (Docker) |
| **Containerization** | Docker Compose |
| **Data Generation** | Faker Library |
| **Analysis** | Pandas + Standard Library |

## Quick Start

### Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running.
- Git installed on your system.

### Installation & Run

```bash
# Clone repository
git clone https://github.com/DKMirza/enterprise-data-agent.git
cd enterprise-data-agent

# Build and run containers
docker compose up --build

# Generate synthetic data (POST request)
curl -X POST http://localhost:8000/generate-synthetic-data

# Get quality report (GET request)
curl http://localhost:8000/quality-report
```

## API Documentation

Once running, visit the auto-generated Swagger UI at http://localhost:8000/docs

## Project Status

| Phase | Description | Status |
|-----------|------------|------------|
| **1** | Data Engine & Synthetic Generation | ✅ |
| **2** | AI Analysis (LLM Duplicate Detection) | ⏳ |
| **3** | Entity Resolution (Fuzzy Matching + AI)	 | 🔜 |
| **4** | Human Approval UI (React Frontend) | 🔜 |
| **5** | Migration Simulator & Sandbox | 🔜 |
| **6** | Production Engineering (CI/CD, Tests) | 🔜 |