from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import os
import pandas as pd
from agents.duplicate_detector import DuplicateDetector
from entity_resolution import EntityResolver

app = FastAPI(
    title="Enterprise Data Migration Platform",
    description="AI-powered CRM modernization and data quality platform"
)


class QualityReport(BaseModel):
    total_records: int
    duplicates_found: int
    missing_fields: dict
    invalid_emails: int
    recommendations: list[str]


class DuplicateRecommendation(BaseModel):
    record_1_id: int
    record_2_id: int
    confidence: float
    risk_level: str
    action: str
    evidence: list[str]
    recommendation: str


# Phase 3 Step 3: Entity Resolution Request/Response Models
class EntityResolutionRequest(BaseModel):
    """Request model for batch entity resolution."""
    records: Optional[List[Dict[str, Any]]] = None  # If None, uses synthetic data
    min_confidence: float = 0.75
    
    class Config:
        json_schema_extra = {
            "example": {
                "min_confidence": 0.80
            }
        }


class EntityResolutionResponse(BaseModel):
    """Response model for batch entity resolution."""
    total_matches: int
    summary: Dict[str, Any]
    recommendations: List[Dict[str, Any]]


class BestMatchRequest(BaseModel):
    """Request model for finding best match for a single record."""
    target_record: Dict[str, Any]
    candidate_records: List[Dict[str, Any]]
    threshold: float = 0.85
    
    class Config:
        json_schema_extra = {
            "example": {
                "target_record": {"company_name": "Acme Corp", "email": "contact@acme.com"},
                "candidate_records": [
                    {"id": 1, "company_name": "Acme Corporation", "email": "info@acme.com"},
                    {"id": 2, "company_name": "Different Company", "email": "contact@other.com"}
                ],
                "threshold": 0.85
            }
        }


class BestMatchResponse(BaseModel):
    """Response model for best match lookup."""
    match_found: bool
    best_match: Optional[Dict[str, Any]]
    message: str


@app.get("/")
def root():
    return {"message": "Enterprise Data Migration Platform API", "version": "1.0.0"}


@app.get("/health")
def health_check():
    return {"status": "healthy", "database": "connected"}


@app.post("/generate-synthetic-data")
def generate_data(num_records: int = 5000):
    """Generate synthetic dirty CRM data for testing"""
    from data_quality.generate_synthetic_data import (
        generate_dirty_crm_records, 
        save_to_csv
    )
    
    records = generate_dirty_crm_records(num_records)
    save_to_csv(records)
    
    return {
        "message": f"Generated {len(records)} synthetic records",
        "file": "data/synthetic/legacy_crm_data.csv"
    }


@app.get("/quality-report")
def get_quality_report():
    """Analyze data quality and return report"""
    try:
        filepath = "data/synthetic/legacy_crm_data.csv"
        if not os.path.exists(filepath):
            raise HTTPException(status_code=404, detail="No synthetic data found. Run /generate-synthetic-data first.")
        
        df = pd.read_csv(filepath)
        
        total = len(df)
        duplicates = df['company_name'].duplicated().sum()
        missing_industry = df['industry'].isna().sum() + (df['industry'] == "").sum()
        invalid_email = df['email'].apply(lambda x: '@' not in str(x) if pd.notna(x) else True).sum()
        
        return QualityReport(
            total_records=total,
            duplicates_found=int(duplicates),
            missing_fields={"industry": int(missing_industry)},
            invalid_emails=int(invalid_email),
            recommendations=[
                "Run duplicate detection on company names",
                "Impute missing industry values using AI inference",
                "Validate and correct email formats"
            ]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/detect-duplicates")
def detect_duplicates():
    """AI-powered duplicate detection with confidence scoring"""
    try:
        filepath = "data/synthetic/legacy_crm_data.csv"
        if not os.path.exists(filepath):
            raise HTTPException(status_code=404, detail="No synthetic data found. Run /generate-synthetic-data first.")
        
        df = pd.read_csv(filepath)
        records = df.to_dict('records')
        
        detector = DuplicateDetector()
        recommendations = detector.detect_duplicates(records)
        summary = detector.get_summary(recommendations)
        
        return {
            "total_recommendations": len(recommendations),
            "summary": summary,
            "recommendations": recommendations[:10]  # Return top 10 for now
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Phase 3 Step 3: Entity Resolution Endpoints
@app.post("/resolve-entities", response_model=EntityResolutionResponse)
def resolve_entities_endpoint(request: EntityResolutionRequest):
    """
    Batch entity resolution - find all potential duplicate pairs in a dataset.
    
    This endpoint uses AI-powered record linkage to identify records that likely
    represent the same real-world entity. It compares multiple fields (name, domain,
    industry, address, phone) using weighted similarity algorithms.
    
    Args:
        request (EntityResolutionRequest): Contains optional custom records or uses synthetic data,
                                          and minimum confidence threshold for matches
        
    Returns:
        EntityResolutionResponse: Total match count, summary statistics, and top 20 recommendations
        
    Use Cases:
        - Pre-migration data cleanup to identify duplicates
        - Merging customer databases from multiple sources
        - Finding related records across different systems
        
    Example Request:
        POST /resolve-entities
        {
            "min_confidence": 0.80
        }
        
    Example Response:
        {
            "total_matches": 156,
            "summary": {"by_risk_level": {"LOW": 45, "MEDIUM": 78, "HIGH": 33}, ...},
            "recommendations": [...]
        }
    """
    try:
        # Load records - either from request or synthetic data
        if request.records:
            records = request.records
        else:
            filepath = "data/synthetic/legacy_crm_data.csv"
            if not os.path.exists(filepath):
                raise HTTPException(
                    status_code=404, 
                    detail="No synthetic data found. Run /generate-synthetic-data first or provide records in request."
                )
            df = pd.read_csv(filepath)
            records = df.to_dict('records')
        
        # Initialize entity resolver with default thresholds
        resolver = EntityResolver()
        
        # Perform batch entity resolution
        recommendations = resolver.resolve_entities(records, min_confidence=request.min_confidence)
        
        # Generate summary statistics
        summary = resolver.get_resolution_summary(recommendations)
        
        return EntityResolutionResponse(
            total_matches=len(recommendations),
            summary=summary,
            recommendations=recommendations[:20]  # Return top 20 matches
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Entity resolution failed: {str(e)}")


@app.post("/find-best-match", response_model=BestMatchResponse)
def find_best_match_endpoint(request: BestMatchRequest):
    """
    Find the best matching record for a single target from candidate records.
    
    This endpoint is useful when you have one record and want to find if it already
    exists in your database (or another dataset). It returns the highest-confidence
    match above the threshold, or indicates no suitable match was found.
    
    Args:
        request (BestMatchRequest): Contains target record to match, list of candidate records,
                                   and minimum confidence threshold
        
    Returns:
        BestMatchResponse: Whether a match was found, details of best match if available,
                          and descriptive message
        
    Use Cases:
        - Real-time duplicate checking during data entry
        - Matching new customer records against existing database
        - Finding canonical entity for a given record
        
    Example Request:
        POST /find-best-match
        {
            "target_record": {
                "company_name": "Acme Corp",
                "email": "contact@acme.com",
                "industry": "Technology"
            },
            "candidate_records": [
                {"id": 1, "company_name": "Acme Corporation", "email": "info@acme.com"},
                {"id": 2, "company_name": "Different Company", "email": "contact@other.com"}
            ],
            "threshold": 0.85
        }
        
    Example Response:
        {
            "match_found": true,
            "best_match": {
                "candidate_record": {...},
                "confidence": 0.92,
                "risk_level": "LOW",
                "action": "AUTO_MERGE",
                "evidence": [...]
            },
            "message": "High confidence match found with candidate ID 1 (92% similarity)"
        }
    """
    try:
        # Validate input
        if not request.target_record:
            raise HTTPException(status_code=400, detail="target_record is required")
        
        if not request.candidate_records or len(request.candidate_records) == 0:
            raise HTTPException(status_code=400, detail="candidate_records list cannot be empty")
        
        # Initialize entity resolver
        resolver = EntityResolver()
        
        # Find best match
        best_match_result = resolver.find_best_match(
            target_record=request.target_record,
            candidate_records=request.candidate_records,
            threshold=request.threshold
        )
        
        if best_match_result:
            return BestMatchResponse(
                match_found=True,
                best_match=best_match_result,
                message=f"Match found with {best_match_result['confidence']*100:.1f}% confidence. "
                       f"Recommended action: {best_match_result['action']}"
            )
        else:
            return BestMatchResponse(
                match_found=False,
                best_match=None,
                message=f"No match found above {request.threshold*100:.0f}% confidence threshold"
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Best match lookup failed: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
