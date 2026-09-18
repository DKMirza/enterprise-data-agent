from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import pandas as pd
from agents.duplicate_detector import DuplicateDetector

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
