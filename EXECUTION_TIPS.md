# Execution Tips & Expected Outputs

This document provides step-by-step instructions for running the Enterprise Data Migration Platform, along with expected outputs for each endpoint.

## Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running
- Git installed on your system
- Terminal/Command Prompt access

## Quick Start Guide

### 1. Clone and Setup

```bash
# Clone repository
git clone https://github.com/DKMirza/enterprise-data-agent.git
cd enterprise-data-agent

# Build and run containers
docker compose up --build
```

**Expected Output:**
```
 [+] Running 2/2
 ⠿ Container enterprise-data-agent-db-1       Started
 ⠿ Container enterprise-data-agent-backend-1  Started
```

### 2. Verify Services are Running

```bash
# Check container status
docker ps

# View backend logs
docker logs enterprise-data-agent-backend-1 --tail 30
```

**Expected Output:**
```
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

### 3. Generate Synthetic Data

```bash
# Using curl (Linux/Mac)
curl -X POST "http://localhost:8000/generate-synthetic-data" \
  -H "Content-Type: application/json" \
  -d '{"num_records": 100}'

# Using PowerShell (Windows)
Invoke-WebRequest -Uri "http://localhost:8000/generate-synthetic-data" -Method POST -ContentType "application/json" -Body '{"num_records": 100}'
```

**Expected Output:**
```json
{
  "message": "Synthetic data generated successfully",
  "records_created": 100,
  "file_path": "data/synthetic/legacy_crm_data.csv"
}
```

### 4. Get Quality Report

```bash
curl http://localhost:8000/quality-report
```

**Expected Output:**
```json
{
  "total_records": 100,
  "issues_found": {
    "duplicates": 15,
    "missing_fields": 23,
    "invalid_formats": 8
  },
  "quality_score": 0.72,
  "recommendations": [
    "Review duplicate records before migration",
    "Fill missing email addresses"
  ]
}
```

### 5. Detect Duplicates (Phase 2)

```bash
curl -X POST "http://localhost:8000/detect-duplicates" \
  -H "Content-Type: application/json" \
  -d '{}'
```

**Expected Output:**
```json
{
  "total_duplicates_found": 15,
  "duplicate_groups": [
    {
      "group_id": 1,
      "records": ["R1", "R2"],
      "confidence": 0.97,
      "reason": "Same domain + similar name"
    }
  ],
  "risk_summary": {
    "LOW": 8,
    "MEDIUM": 5,
    "HIGH": 2
  }
}
```

### 6. Entity Resolution - Batch Processing (Phase 3)

**Endpoint:** `POST /resolve-entities`

**Request Example:**
```bash
curl -X POST "http://localhost:8000/resolve-entities" \
  -H "Content-Type: application/json" \
  -d '{
    "records": [
      {"id": "R1", "name": "Acme Corp", "domain": "acme.com"},
      {"id": "R2", "name": "Acme Corporation", "domain": "acme.com"}
    ],
    "min_confidence": 0.75
  }'
```

**Expected Output:**
```json
{
  "total_matches": 1,
  "summary": {
    "by_risk_level": {"LOW": 1, "MEDIUM": 0, "HIGH": 0},
    "by_action": {"AUTO_MERGE": 1},
    "avg_confidence": 0.944
  },
  "recommendations": [
    {
      "record_1_id": "R1",
      "record_2_id": "R2",
      "confidence": 0.944,
      "risk_level": "LOW",
      "action": "AUTO_MERGE",
      "evidence": [
        {"type": "DOMAIN_MATCH", "score": 1.0, "details": "Same domain: acme.com"},
        {"type": "PHONE_MATCH", "score": 1.0, "details": "Same phone number"}
      ]
    }
  ]
}
```

### 7. Entity Resolution - Single Record Lookup (Phase 3)

**Endpoint:** `POST /find-best-match`

**Request Example:**
```bash
curl -X POST "http://localhost:8000/find-best-match" \
  -H "Content-Type: application/json" \
  -d '{
    "target_record": {"id": "Q1", "name": "Acme Corp Inc", "domain": "acme.com"},
    "candidate_records": [
      {"id": "C1", "name": "Acme Corporation", "domain": "acme.com"}
    ],
    "threshold": 0.85
  }'
```

**Expected Output:**
```json
{
  "match_found": true,
  "best_match": {
    "candidate_id": "C1",
    "confidence": 1.0,
    "evidence": [
      {"type": "DOMAIN_MATCH", "score": 1.0, "details": "Same domain: acme.com"}
    ],
    "risk_level": "LOW",
    "action": "AUTO_MERGE"
  },
  "message": "Match found with 100.0% confidence. Recommended action: AUTO_MERGE"
}
```

### 8. Health Check

```bash
curl http://localhost:8000/health
```

**Expected Output:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2025-01-15T10:30:00Z"
}
```

## API Documentation Access

Once the backend is running, visit the auto-generated Swagger UI:

**URL:** http://localhost:8000/docs

This provides interactive documentation for all endpoints with request/response schemas.

## Confidence Thresholds Reference

| Confidence Range | Risk Level | Action | Description |
|-----------------|------------|--------|-------------|
| ≥ 0.90 | LOW | AUTO_MERGE | Records are highly likely duplicates, safe to merge automatically |
| 0.75 - 0.89 | MEDIUM | REVIEW_REQUIRED | Manual review recommended before merging |
| 0.60 - 0.74 | HIGH | INVESTIGATE | Low confidence match, investigate further |

## Algorithm Weights

The entity resolution algorithm uses the following field weights:
- **Name Similarity**: 35% (fuzzy string matching)
- **Domain Match**: 25% (exact email domain comparison)
- **Industry Similarity**: 15% (semantic similarity)
- **Address Similarity**: 10% (normalized address comparison)
- **Phone Similarity**: 10% (formatted phone number match)
- **Email Domain Match**: 5% (email domain consistency)

## Troubleshooting

### Container Won't Start

**Problem:** `docker compose up` fails or containers exit immediately.

**Solution:**
```bash
# Check logs for errors
docker logs enterprise-data-agent-backend-1

# Restart PostgreSQL container
docker compose restart db

# Rebuild backend if needed
docker compose build --no-cache
docker compose up -d
```

### Port Already in Use

**Problem:** Error "Port 8000 is already allocated" or "Address already in use".

**Solution:**
```bash
# Find process using port 8000 (Linux/Mac)
lsof -i :8000

# Find process using port 8000 (Windows PowerShell)
netstat -ano | findstr :8000

# Kill the process or change port in docker-compose.yml
```

### 404 Not Found on New Endpoints

**Problem:** New endpoints return 404 after code changes.

**Solution:**
```bash
# Restart containers to load updated code
docker compose down && docker compose up -d
```

### Database Connection Issues

**Problem:** Backend can't connect to PostgreSQL.

**Solution:**
```bash
# Ensure database container is running
docker ps | grep db

# Check backend logs for connection errors
docker logs enterprise-data-agent-backend-1

# Restart both containers together
docker compose restart
```

### Synthetic Data Not Generated

**Problem:** `/generate-synthetic-data` returns error or file not created.

**Solution:**
```bash
# Ensure data directory exists
mkdir -p data/synthetic

# Check permissions (Linux/Mac)
chmod 755 data/synthetic

# Try generating with smaller dataset first
curl -X POST "http://localhost:8000/generate-synthetic-data" \
  -H "Content-Type: application/json" \
  -d '{"num_records": 10}'
```

## Stopping the Platform

```bash
# Stop containers (keep data)
docker compose down

# Stop and remove volumes (clears database)
docker compose down -v

# Remove images as well
docker compose down --rmi all
```

## Next Steps

After running these endpoints successfully, you can:
1. Access Swagger UI at http://localhost:8000/docs for interactive testing
2. Review generated CSV files in `data/synthetic/` directory
3. Proceed to Phase 4 (Human Approval UI) development
4. Implement migration sandbox for validation

## Additional Resources

- **Main README**: See [README.md](README.md) for architecture and project overview
- **API Docs**: http://localhost:8000/docs (when running)
- **GitHub Repository**: https://github.com/DKMirza/enterprise-data-agent
