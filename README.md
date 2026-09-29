# Enterprise Data Migration Platform 🚀

An enterprise-grade AI platform that automates legacy CRM modernization with human-in-the-loop oversight. This system addresses the critical challenge of migrating dirty, inconsistent data from legacy systems to modern platforms while maintaining auditability and control.

---

## 📋 Table of Contents

- [Quick Start](#quick-start)
- [Prerequisites](#prerequisites)
- [Installation & Setup](#installation--setup)
- [Running the Backend (Phases 1-3)](#running-the-backend-phases-1-3)
- [Running the Frontend (Phase 4)](#running-the-frontend-phase-4)
- [Testing the Application](#testing-the-application)
- [API Documentation](#api-documentation)
- [Troubleshooting](#troubleshooting)

---

## 🚀 Quick Start

For a **complete setup from scratch**, follow these steps:

```bash
# 1. Clone the repository
git clone https://github.com/DKMirza/enterprise-data-agent.git
cd enterprise-data-agent

# 2. Start the backend services (Phases 1-3)
docker-compose up -d --build

# 3. Install frontend dependencies (Phase 4)
cd frontend
npm install

# 4. Start the frontend dev server
npm run dev

# 5. Open your browser
# Backend API: http://localhost:8000/docs
# Frontend UI: http://localhost:5173
```

---

## 📋 Prerequisites

Before you begin, ensure you have the following installed on your system:

### Required Software

| Software | Version | Download Link | Purpose |
|----------|---------|---------------|---------|
| **Git** | 2.x or later | [git-scm.com](https://git-scm.com/downloads) | Clone repository |
| **Docker Desktop** | 4.x or later | [docker.com](https://www.docker.com/products/docker-desktop/) | Run backend & database |
| **Node.js** | 18.x LTS or later | [nodejs.org](https://nodejs.org/) | Run frontend (includes npm) |

### Verify Installation

Open your terminal/command prompt and run:

```bash
# Check Git installation
git --version

# Check Docker installation
docker --version
docker-compose --version

# Check Node.js installation
node --version
npm --version
```

**Expected Output Example:**
```
git version 2.43.0
Docker version 27.0.0, build ...
docker compose version 2.26.0
v18.19.0
10.2.3
```

---

## 🛠️ Installation & Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/DKMirza/enterprise-data-agent.git
cd enterprise-data-agent
```

**Project Structure:**
```
enterprise-data-agent/
├── backend/              # FastAPI backend (Phases 1-3)
│   ├── main.py          # Main application entry point
│   └── requirements.txt # Python dependencies
├── frontend/            # React frontend (Phase 4)
│   ├── src/             # Source files
│   │   ├── components/  # Reusable UI components
│   │   ├── pages/       # Page components
│   │   ├── services/    # API integration
│   │   └── types/       # TypeScript definitions
│   ├── package.json     # Node.js dependencies
│   └── vite.config.ts   # Vite configuration
├── data/               # Generated synthetic data
├── docker-compose.yml  # Docker services configuration
├── README.md          # This file
└── EXECUTION_TIPS.md  # Detailed API examples
```

---

## 🔄 Running the Backend (Phases 1-3)

The backend includes Phases 1-3: Data Generation, AI Duplicate Detection, and Entity Resolution.

### Step 2: Start Docker Services

From the **project root directory**, run:

```bash
docker-compose up -d --build
```

**What this does:**
- Builds the FastAPI backend container
- Starts PostgreSQL database container
- Runs both services in detached mode (`-d`)

**Expected Output:**
```
 [+] Building 123.4s (xx/xx) FINISHED
 [+] Running 2/2
 ⠿ Container enterprise-data-agent-db-1       Started
 ⠿ Container enterprise-data-agent-backend-1  Started
```

### Step 3: Verify Backend is Running

Check container status:
```bash
docker ps
```

View backend logs:
```bash
docker logs enterprise-data-agent-backend-1 --tail 20
```

**Expected Output:**
```
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

### Step 4: Test Backend API

Open your browser and visit: **http://localhost:8000/docs**

This is the auto-generated Swagger UI with interactive API documentation.

Or test via terminal:

```bash
# Health check
curl http://localhost:8000/health

# Generate synthetic data (100 records)
curl -X POST "http://localhost:8000/generate-synthetic-data" \
  -H "Content-Type: application/json" \
  -d '{"num_records": 100}'

# Get quality report
curl http://localhost:8000/quality-report
```

**Windows PowerShell Alternative:**
```powershell
Invoke-WebRequest -Uri "http://localhost:8000/generate-synthetic-data" `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"num_records": 100}'
```

---

## 🎨 Running the Frontend (Phase 4)

The frontend is a React + TypeScript application with Tailwind CSS for the Human Approval UI.

### Step 5: Install Frontend Dependencies

Navigate to the frontend directory and install dependencies:

```bash
cd frontend
npm install
```

**Expected Output:**
```
added 180 packages in 45s
```

> **Note:** If you encounter a PowerShell execution policy error (`running scripts is disabled`), run this first:
> ```powershell
> Set-ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
> ```

### Step 6: Start Frontend Development Server

From the `frontend` directory, run:

```bash
npm run dev
```

**Expected Output:**
```
VITE v5.x.x ready in xxx ms

➜  Local:   http://localhost:5173/
➜  Network: use --host to expose
```

### Step 7: Open the Application

Open your browser and visit: **http://localhost:5173**

You should see the Enterprise Data Agent dashboard with:
- Quality metrics overview
- Approval queue for duplicate recommendations
- Navigation between Dashboard and Approvals pages

---

## ✅ Testing the Application

### Backend API Tests (Phases 1-3)

#### Test 1: Generate Synthetic Data
```bash
curl -X POST "http://localhost:8000/generate-synthetic-data" \
  -H "Content-Type: application/json" \
  -d '{"num_records": 50}'
```

**Expected Response:**
```json
{
  "message": "Synthetic data generated successfully",
  "records_created": 50,
  "file_path": "data/synthetic/legacy_crm_data.csv"
}
```

#### Test 2: Get Quality Report
```bash
curl http://localhost:8000/quality-report
```

**Expected Response:**
```json
{
  "total_records": 50,
  "issues_found": {
    "duplicates": 8,
    "missing_fields": 12,
    "invalid_formats": 3
  },
  "quality_score": 0.75
}
```

#### Test 3: Entity Resolution (Phase 3)
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

**Expected Response:**
```json
{
  "total_matches": 1,
  "recommendations": [
    {
      "record_1_id": "R1",
      "record_2_id": "R2",
      "confidence": 0.94,
      "risk_level": "LOW",
      "action": "AUTO_MERGE",
      "evidence": [
        {"type": "DOMAIN_MATCH", "score": 1.0}
      ]
    }
  ]
}
```

### Frontend Tests (Phase 4)

1. **Dashboard Page** (`http://localhost:5173`)
   - Should display quality metrics with progress bars
   - Shows total records, duplicates found, pending review counts

2. **Approvals Page** (`http://localhost:5173/approvals`)
   - Lists duplicate recommendations from backend
   - Filter by risk level (All, Review Required, Investigate)
   - Each card shows confidence score and evidence

---

## 📚 API Documentation

### Backend Endpoints

| Endpoint | Method | Description | Phase |
|----------|--------|-------------|-------|
| `/health` | GET | Health check | All |
| `/generate-synthetic-data` | POST | Generate test data | 1 |
| `/quality-report` | GET | Get quality metrics | 1 |
| `/detect-duplicates` | POST | AI duplicate detection | 2 |
| `/resolve-entities` | POST | Batch entity resolution | 3 |
| `/find-best-match` | POST | Single record lookup | 3 |

**Interactive API Docs:** http://localhost:8000/docs (when backend is running)

### Frontend Pages

| Route | Component | Description |
|-------|-----------|-------------|
| `/` | Dashboard | Quality metrics overview |
| `/approvals` | Approvals | Human approval queue |
| `*` | NotFound | 404 error page |

---

## 🔧 Troubleshooting

### Issue: Docker containers won't start

**Solution:**
```bash
# Check logs for errors
docker logs enterprise-data-agent-backend-1

# Restart services
docker-compose down
docker-compose up -d --build
```

### Issue: Port 8000 or 5432 already in use

**Solution (Windows):**
```powershell
# Find process using port 8000
netstat -ano | findstr :8000

# Kill the process (replace PID with actual number)
taskkill /PID <PID> /F
```

**Solution (Linux/Mac):**
```bash
lsof -i :8000
kill -9 <PID>
```

### Issue: npm command not recognized

**Solution:** Ensure Node.js is installed and in PATH:
```powershell
# Check installation
node --version
npm --version

# If not found, reinstall from https://nodejs.org/
# Make sure to check "Add to PATH" during installation
```

### Issue: PowerShell execution policy error

**Error:** `running scripts is disabled on this system`

**Solution:**
```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
```

### Issue: Frontend can't connect to backend

**Solution:** The frontend uses a Vite proxy configured in `vite.config.ts`. Ensure:
1. Backend is running on http://localhost:8000
2. Docker containers are healthy (`docker ps`)
3. No CORS errors in browser console

### Issue: Database connection errors

**Solution:**
```bash
# Restart database container
docker-compose restart db

# Check database logs
docker logs enterprise-data-agent-db-1
```

---

## 🛑 Stopping the Application

### Stop Frontend
Press `Ctrl + C` in the terminal running `npm run dev`

### Stop Backend (Docker)
```bash
# Stop containers (keep data)
docker-compose down

# Stop and remove volumes (clears database)
docker-compose down -v

# Remove images as well
docker-compose down --rmi all
```

---

## 📊 Confidence Thresholds Reference

| Confidence Range | Risk Level | Action | Description |
|-----------------|------------|--------|-------------|
| ≥ 0.90 | LOW | AUTO_MERGE | Highly likely duplicates, safe to merge |
| 0.75 - 0.89 | MEDIUM | REVIEW_REQUIRED | Manual review recommended |
| 0.60 - 0.74 | HIGH | INVESTIGATE | Low confidence, investigate further |

---

## 🎯 Project Status

| Phase | Description | Status |
|-------|-------------|--------|
| **1** | Data Engine & Synthetic Generation | ✅ Complete |
| **2** | AI Duplicate Detection | ✅ Complete |
| **3** | Entity Resolution (Fuzzy Matching) | ✅ Complete |
| **4** | Human Approval UI (React Frontend) | ✅ Complete |
| **5** | Migration Simulator & Sandbox | 🔜 Pending |
| **6** | Production Engineering (CI/CD, Tests) | 🔜 Pending |

---

## 📖 Additional Resources

- **Detailed API Examples:** [EXECUTION_TIPS.md](EXECUTION_TIPS.md)
- **Frontend Setup Guide:** [frontend/SETUP_GUIDE.md](frontend/SETUP_GUIDE.md)
- **Testing Instructions:** [TESTING_INSTRUCTIONS_UPDATED.md](TESTING_INSTRUCTIONS_UPDATED.md)

---

## 🤝 Contributing

This project is under active development. Feel free to explore the codebase, report issues, or submit pull requests!

---

## 📄 License

MIT License - See [LICENSE](LICENSE) file for details.

---

**Built with ❤️ using FastAPI, PostgreSQL, React, TypeScript, and Docker**
