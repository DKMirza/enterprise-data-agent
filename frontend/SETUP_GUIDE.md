# Enterprise Data Agent - Frontend Setup Guide

## Overview
Phase 4 frontend is now complete with React + Vite + TypeScript + Tailwind CSS.

## Files Created
```
frontend/
├── package.json              # Dependencies and scripts
├── vite.config.ts            # Vite configuration with API proxy
├── tsconfig.json             # TypeScript configuration
├── index.html                # HTML entry point
├── tailwind.config.js        # Tailwind CSS configuration
├── postcss.config.js         # PostCSS configuration
└── src/
    ├── main.tsx              # Application entry point
    ├── App.tsx               # Main app component with routing
    ├── index.css             # Global styles with Tailwind
    ├── types/
    │   └── models.ts         # TypeScript interfaces
    ├── services/
    │   └── api.ts            # API client functions
    ├── components/
    │   ├── Navbar.tsx        # Navigation bar
    │   ├── RiskBadge.tsx     # Risk level indicator
    │   ├── ConfidenceMeter.tsx  # Confidence score display
    │   ├── RecommendationCard.tsx  # Individual recommendation card
    │   └── RecommendationsList.tsx # List container
    └── pages/
        ├── Dashboard.tsx     # Quality metrics dashboard
        ├── Approvals.tsx     # Approval queue page
        └── NotFound.tsx      # 404 error page
```

## Quick Start

### 1. Install Dependencies
```bash
cd C:\Users\danya\Documents\enterprise-data-agent\frontend
npm install
```

### 2. Start Backend (if not running)
```bash
# From project root
docker-compose up -d
# Backend will be available at http://localhost:8000
```

### 3. Start Frontend Dev Server
```bash
cd frontend
npm run dev
# Frontend will be available at http://localhost:5173
```

## Features Implemented

### Dashboard Page (/)
- Data quality metrics (completeness, accuracy, consistency, uniqueness)
- Summary statistics (total records, duplicates found, auto-merged, pending review)
- Recent entity resolution activity
- Visual progress bars for quality scores

### Approvals Page (/approvals)
- Filterable recommendation list (All, Review Required, Investigate)
- Individual recommendation cards with:
  - Confidence score meter
  - Risk level badge
  - Evidence details
  - Approve/Reject actions
- Pagination support
- Real-time stats display

### API Integration
- Connected to backend endpoints:
  - `POST /resolve-entities` - Get duplicate recommendations
  - `GET /quality-report` - Fetch quality metrics
  - `POST /generate-synthetic-data` - Generate test data
- Proxy configured in vite.config.ts for seamless API calls

## Notes

### Backend Endpoints Needed
The following backend endpoints need to be implemented for full functionality:
- `POST /api/approve/{record1_id}/{record2_id}` - Approve a recommendation
- `POST /api/reject/{record1_id}/{record2_id}` - Reject a recommendation

These are currently placeholder functions in `frontend/src/services/api.ts`.

### CORS Configuration
If you encounter CORS errors, update the FastAPI backend with:
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Development

### Available Scripts
- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint (if configured)

### Tech Stack
- **React 18** - UI library
- **Vite** - Build tool and dev server
- **TypeScript** - Type safety
- **Tailwind CSS** - Utility-first styling
- **React Router v6** - Client-side routing
- **Axios** - HTTP client

## Next Steps
1. Install dependencies: `npm install`
2. Start backend: `docker-compose up -d`
3. Start frontend: `npm run dev`
4. Open http://localhost:5173 in your browser
5. Test the approval workflow with synthetic data
