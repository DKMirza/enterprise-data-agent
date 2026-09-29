# Testing Instructions for Enterprise Data Migration Platform (Updated)

Here's a complete guide to test all the work done so far, based on the **actual implemented endpoints**.

---

## Step 1: Verify Repository State

First, confirm you're in the correct directory and check git status:

```bash
cd C:\Users\danya\Documents\enterprise-data-agent
git log --oneline -5
```

**Expected output:** You should see commit `6c93238` (or similar) with message about documentation refactor, followed by Phase 3 commits.

---

## Step 2: Start Docker Containers

If containers aren't running yet:

```bash
docker compose up --build -d
```

**Wait ~10 seconds** for the backend to initialize. Then verify it's running:

```bash
docker ps
```

**Expected:** You should see two containers:
- `enterprise-data-agent-backend-1` (status: Up)
- `enterprise-data-agent-db-1` (PostgreSQL, status: Up)

---

## Step 3: Health Check & API Info

### Test 3.1: Root Endpoint
```bash
curl "http://localhost:8000/"
```

**Expected:** 
```json
{"message": "Enterprise Data Migration Platform API", "version": "1.0.0"}
```

### Test 3.2: Health Check Endpoint
```bash
curl "http://localhost:8000/health"
```

**Expected:** 
```json
{"status": "healthy", "database": "connected"}
```

---

## Step 4: Setup - Generate Synthetic Data (Phase 1 Alternative)

The platform uses synthetic data generation instead of file uploads. First, generate test data:

### Test 4.1: Generate Synthetic CRM Data
```bash
curl -X POST "http://localhost:8000/generate-synthetic-data" \
  -H "Content-Type: application/json" \
  -d '{"num_records": 100}'
```

**Expected:** 
```json
{
  "message": "Generated 100 synthetic records",
  "file": "data/synthetic/legacy_crm_data.csv"
}
```

---

## Step 5: Test Phase 1 Endpoints (Data Quality Analysis)

### Test 5.1: Get Data Quality Report
```bash
curl "http://localhost:8000/quality-report"
```

**Expected:** 
```json
{
  "total_records": 100,
  "duplicates_found": <number>,
  "missing_fields": {
    "industry": <number>
  },
  "invalid_emails": <number>,
  "recommendations": [
    "Run duplicate detection on company names",
    "Impute missing industry values using AI inference",
    "Validate and correct email formats"
  ]
}
```

---

## Step 6: Test Phase 2 Endpoints (Duplicate Detection)

### Test 6.1: Detect Duplicates with AI
```bash
curl -X POST "http://localhost:8000/detect-duplicates" \
  -H "Content-Type: application/json" \
  -d '{}'
```

**Expected:** 
```json
{
  "total_recommendations": <number>,
  "summary": {
    "by_risk_level": {
      "LOW": <count>,
      "MEDIUM": <count>,
      "HIGH": <count>
    },
    "by_action": {
      "AUTO_MERGE": <count>,
      "REVIEW_REQUIRED": <count>,
      "INVESTIGATE": <count>
    },
    "avg_confidence": <0.0-1.0>
  },
  "recommendations": [
    {
      "record_1_id": "<id>",
      "record_2_id": "<id>",
      "confidence": <0.0-1.0>,
      "risk_level": "LOW|MEDIUM|HIGH",
      "action": "AUTO_MERGE|REVIEW_REQUIRED|INVESTIGATE",
      "evidence": ["<reason 1>", "<reason 2>"],
      "recommendation": "<merge recommendation>"
    }
  ]
}
```

**Note:** This endpoint requires synthetic data to be generated first (Step 4).

---

## Step 7: Test Phase 3 Endpoints (Entity Resolution)

### Test 7.1: Resolve Entities (Batch Matching) - Using Synthetic Data
```bash
curl -X POST "http://localhost:8000/resolve-entities" \
  -H "Content-Type: application/json" \
  -d '{"min_confidence": 0.75}'
```

**Expected:** 
```json
{
  "total_matches": <number>,
  "summary": {
    "total_matches": <number>,
    "by_risk_level": {
      "LOW": <count>,
      "MEDIUM": <count>,
      "HIGH": <count>
    },
    "by_action": {
      "AUTO_MERGE": <count>,
      "REVIEW_REQUIRED": <count>,
      "INVESTIGATE": <count>
    },
    "avg_confidence": <0.0-1.0>,
    "high_confidence_count": <number>,
    "unique_record_pairs": <number>
  },
  "recommendations": [
    {
      "record_1_id": "<id>",
      "record_2_id": "<id>",
      "confidence": <0.0-1.0>,
      "risk_level": "LOW|MEDIUM|HIGH",
      "action": "AUTO_MERGE|REVIEW_REQUIRED|INVESTIGATE",
      "evidence": [
        {
          "type": "DOMAIN_MATCH|NAME_SIMILARITY|PHONE_MATCH|etc",
          "score": <0.0-1.0>,
          "details": "<explanation>",
          "weight": <0.0-1.0>
        }
      ],
      "recommendation": "<merge recommendation>",
      "record_1_preview": {...},
      "record_2_preview": {...}
    }
  ]
}
```

### Test 7.2: Resolve Entities (Batch Matching) - With Custom Records
```bash
curl -X POST "http://localhost:8000/resolve-entities" \
  -H "Content-Type: application/json" \
  -d '{"records": [{"id": "R1", "name": "Acme Corp", "domain": "acme.com"}, {"id": "R2", "name": "Acme Corporation", "domain": "acme.com"}], "min_confidence": 0.75}'
```

**Expected:** Similar response structure as Test 7.1, but with your custom records.

### Test 7.3: Find Best Match (Single Record Lookup)
```bash
curl -X POST "http://localhost:8000/find-best-match" \
  -H "Content-Type: application/json" \
  -d '{"target_record": {"id": "Q1", "name": "Acme Corp Inc", "domain": "acme.com"}, "candidate_records": [{"id": "C1", "name": "Acme Corporation", "domain": "acme.com"}], "threshold": 0.85}'
```

**Expected:** 
```json
{
  "match_found": true,
  "best_match": {
    "candidate_id": "C1",
    "confidence": <0.0-1.0>,
    "evidence": [
      {
        "type": "DOMAIN_MATCH|NAME_SIMILARITY|etc",
        "score": <0.0-1.0>,
        "details": "<explanation>",
        "weight": <0.0-1.0>
      }
    ],
    "risk_level": "LOW|MEDIUM|HIGH",
    "action": "AUTO_MERGE|REVIEW_REQUIRED|INVESTIGATE",
    "preview": {...}
  },
  "message": "Match found with <confidence>% confidence. Recommended action: <action>"
}
```

### Test 7.4: Find Best Match - No Match Found
```bash
curl -X POST "http://localhost:8000/find-best-match" \
  -H "Content-Type: application/json" \
  -d '{"target_record": {"id": "Q1", "name": "Unique Company XYZ", "domain": "unique-xyz.com"}, "candidate_records": [{"id": "C1", "name": "Acme Corporation", "domain": "acme.com"}], "threshold": 0.85}'
```

**Expected:** 
```json
{
  "match_found": false,
  "best_match": null,
  "message": "No match found above 85% confidence threshold"
}
```

---

## Step 8: Verify Documentation Files

Check that both documentation files exist and contain the expected content:

```bash
# Check README.md exists
type README.md | findstr /C:"EXECUTION_TIPS"

# Check EXECUTION_TIPS.md exists
type EXECUTION_TIPS.md | findstr /C:"Phase 3"
```

**Expected:** Both files should exist and contain references to each other.

---

## Step 9: Interactive API Documentation (Optional)

Open your browser and visit the auto-generated Swagger UI:

**URL:** http://localhost:8000/docs

This provides interactive documentation for all endpoints with request/response schemas, allowing you to test endpoints directly from the browser.

---

## Confidence Thresholds Reference

| Confidence Range | Risk Level | Action | Description |
|-----------------|------------|--------|-------------|
| ≥ 0.90 | LOW | AUTO_MERGE | Records are highly likely duplicates, safe to merge automatically |
| 0.75 - 0.89 | MEDIUM | REVIEW_REQUIRED | Manual review recommended before merging |
| 0.60 - 0.74 | HIGH | INVESTIGATE | Low confidence match, investigate further |

---

## Algorithm Weights

The entity resolution algorithm uses the following field weights:
- **Name Similarity**: 35% (fuzzy string matching)
- **Domain Match**: 25% (exact email domain comparison)
- **Industry Similarity**: 15% (semantic similarity)
- **Address Similarity**: 10% (normalized address comparison)
- **Phone Similarity**: 10% (formatted phone number match)
- **Email Domain Match**: 5% (email domain consistency)

---

## What to Report Back

Please share any output that:
- ❌ Returns **404 Not Found** (endpoint missing)
- ❌ Returns **500 Internal Server Error** (backend error)
- ❌ Shows unexpected JSON structure
- ⚠️ Has warnings or errors in the response
- 🤔 You don't understand what a particular field means

---

## Troubleshooting

### Container Won't Start
```bash
# Check logs for errors
docker logs enterprise-data-agent-backend-1

# Restart containers
docker compose restart
```

### Port Already in Use
```bash
# Find process using port 8000 (Windows PowerShell)
netstat -ano | findstr :8000

# Kill the process or change port in docker-compose.yml
```

### Synthetic Data Not Generated
```bash
# Ensure data directory exists
mkdir -p data/synthetic

# Try generating with smaller dataset first
curl -X POST "http://localhost:8000/generate-synthetic-data" \
  -H "Content-Type: application/json" \
  -d '{"num_records": 10}'
```

### 404 Not Found on Endpoints
```bash
# Restart containers to load updated code
docker compose down && docker compose up -d
```

---

## Summary of All Working Endpoints

| Endpoint | Method | Description | Phase |
|----------|--------|-------------|-------|
| `/` | GET | API info and version | - |
| `/health` | GET | Health check | - |
| `/generate-synthetic-data` | POST | Generate test CRM data | Setup |
| `/quality-report` | GET | Data quality analysis | Phase 1 |
| `/detect-duplicates` | POST | AI duplicate detection | Phase 2 |
| `/resolve-entities` | POST | Batch entity resolution | Phase 3 |
| `/find-best-match` | POST | Single record lookup | Phase 3 |

---

**Note:** The original test instructions referenced endpoints (`/upload-csv`, `/upload-json`, `/transform-data`, `/validate-schema`) that are not implemented in the current codebase. This updated guide reflects the actual working endpoints as documented in `EXECUTION_TIPS.md` and verified in `backend/main.py`.
