from typing import List, Dict, Any
import re
from difflib import SequenceMatcher

class DuplicateDetector:
    """AI-powered duplicate detection with confidence scoring"""
    
    def __init__(self):
        self.high_confidence_threshold = 0.95
        self.medium_confidence_threshold = 0.75
    
    def safe_string(self, value) -> str:
        """Safely convert any value to string for comparison"""
        if value is None or (isinstance(value, float) and str(value) == 'nan'):
            return ""
        return str(value).strip()
    
    def calculate_string_similarity(self, s1: str, s2: str) -> float:
        """Calculate similarity between two strings"""
        if not self.safe_string(s1) or not self.safe_string(s2):
            return 0.0
        return SequenceMatcher(None, self.safe_string(s1).lower(), self.safe_string(s2).lower()).ratio()
    
    def normalize_company_name(self, name: str) -> str:
        """Normalize company names for comparison"""
        safe_name = self.safe_string(name)
        if not safe_name:
            return ""
        # Remove common suffixes
        patterns = [r'\b(Corp|Corporation|Inc|Incorporated|LLC|Ltd)\b', r'\s+', r'^\s+|\s+$']
        normalized = safe_name.lower()
        for pattern in patterns:
            normalized = re.sub(pattern, '', normalized)
        return normalized.strip()
    
    def detect_duplicates(self, records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Detect potential duplicates with confidence scores and evidence"""
        recommendations = []
        
        # Group by domain first (strong signal)
        domain_groups = {}
        for record in records:
            domain = self.safe_string(record.get('domain', '')).lower()
            if domain:
                if domain not in domain_groups:
                    domain_groups[domain] = []
                domain_groups[domain].append(record)
        
        # Check duplicates within each domain group
        for domain, group_records in domain_groups.items():
            if len(group_records) < 2:
                continue
            
            for i in range(len(group_records)):
                for j in range(i + 1, len(group_records)):
                    rec1 = group_records[i]
                    rec2 = group_records[j]
                    
                    # Calculate confidence score
                    evidence = []
                    scores = []
                    
                    # Company name similarity
                    name_sim = self.calculate_string_similarity(
                        self.normalize_company_name(rec1.get('company_name', '')),
                        self.normalize_company_name(rec2.get('company_name', ''))
                    )
                    if name_sim > 0.7:
                        evidence.append(f"Similar company name ({name_sim:.0%} match)")
                        scores.append(name_sim * 0.4)
                    
                    # Same domain (strong signal)
                    dom1 = self.safe_string(rec1.get('domain', '')).lower()
                    dom2 = self.safe_string(rec2.get('domain', '')).lower()
                    if dom1 and dom2 and dom1 == dom2:
                        evidence.append("Same website domain")
                        scores.append(0.35)
                    
                    # Industry match
                    ind1 = self.safe_string(rec1.get('industry', ''))
                    ind2 = self.safe_string(rec2.get('industry', ''))
                    if ind1 and ind2 and ind1.lower() == ind2.lower():
                        evidence.append("Same industry")
                        scores.append(0.15)
                    
                    # Address similarity (weak signal)
                    addr_sim = self.calculate_string_similarity(
                        rec1.get('address', ''),
                        rec2.get('address', '')
                    )
                    if addr_sim > 0.6:
                        evidence.append(f"Similar address ({addr_sim:.0%} match)")
                        scores.append(addr_sim * 0.1)
                    
                    # Calculate overall confidence
                    if scores:
                        confidence = min(sum(scores), 1.0)
                        
                        # Determine risk level
                        if confidence >= self.high_confidence_threshold:
                            risk_level = "LOW"
                            action = "AUTO_MERGE"
                        elif confidence >= self.medium_confidence_threshold:
                            risk_level = "MEDIUM"
                            action = "REVIEW_REQUIRED"
                        else:
                            risk_level = "HIGH"
                            action = "INVESTIGATE"
                        
                        recommendations.append({
                            "record_1_id": rec1.get('id'),
                            "record_2_id": rec2.get('id'),
                            "confidence": round(confidence, 2),
                            "risk_level": risk_level,
                            "action": action,
                            "evidence": evidence,
                            "recommendation": f"MERGE records {rec1.get('id')} and {rec2.get('id')}"
                        })
        
        return recommendations
    
    def get_summary(self, recommendations: List[Dict[str, Any]]) -> Dict[str, int]:
        """Get summary statistics of recommendations"""
        summary = {"LOW": 0, "MEDIUM": 0, "HIGH": 0}
        for rec in recommendations:
            summary[rec["risk_level"]] += 1
        return summary
