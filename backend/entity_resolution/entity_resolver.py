"""
Entity Resolution Service for AI-powered Record Linkage

This module provides advanced entity resolution capabilities including:
- Multi-algorithm similarity scoring
- Configurable matching thresholds
- Evidence-based recommendations
- Batch processing for large datasets

Author: Enterprise Data Migration Platform Team
Version: 1.0.0
Last Updated: Phase 3 - Step 2
"""

from typing import List, Dict, Any, Tuple, Optional, Set
import re
from collections import defaultdict
from .similarity_utils import (
    levenshtein_similarity,
    jaccard_string_similarity,
    soundex_similarity,
    normalize_company_name,
    safe_string,
    extract_domain,
    normalize_phone
)


class EntityResolver:
    """
    Advanced entity resolution service for identifying duplicate or related records.
    
    This class provides AI-powered record linkage with configurable algorithms,
    confidence scoring, and evidence-based recommendations for data migration scenarios.
    """
    
    def __init__(self, 
                 high_confidence_threshold: float = 0.90,
                 medium_confidence_threshold: float = 0.75,
                 low_confidence_threshold: float = 0.60):
        """
        Initialize the EntityResolver with configurable thresholds.
        
        Args:
            high_confidence_threshold (float): Threshold for HIGH confidence matches (auto-merge)
            medium_confidence_threshold (float): Threshold for MEDIUM confidence (review required)
            low_confidence_threshold (float): Threshold for LOW confidence (investigate)
        """
        self.high_confidence_threshold = high_confidence_threshold
        self.medium_confidence_threshold = medium_confidence_threshold
        self.low_confidence_threshold = low_confidence_threshold
        
        # Algorithm weights for combined scoring
        self.algorithm_weights = {
            'name_similarity': 0.35,      # Company/name match (most important)
            'domain_match': 0.25,         # Same domain (strong signal)
            'industry_match': 0.15,       # Same industry
            'address_similarity': 0.10,   # Address similarity
            'phone_similarity': 0.10,     # Phone number match
            'email_domain_match': 0.05    # Email domain match
        }
    
    def calculate_combined_score(self, record1: Dict[str, Any], 
                                 record2: Dict[str, Any]) -> Tuple[float, List[Dict[str, Any]]]:
        """
        Calculate a combined similarity score between two records using multiple algorithms.
        
        Args:
            record1 (Dict): First record to compare
            record2 (Dict): Second record to compare
            
        Returns:
            Tuple[float, List[Dict]]: Combined confidence score and list of evidence items
        """
        evidence = []
        weighted_scores = []
        
        # 1. Company/Name Similarity (highest weight)
        name1 = normalize_company_name(record1.get('company_name', ''))
        name2 = normalize_company_name(record2.get('company_name', ''))
        
        if name1 and name2:
            # Use multiple similarity algorithms
            lev_sim = levenshtein_similarity(name1, name2)
            jac_sim = jaccard_string_similarity(name1, name2)
            soundex_sim = soundex_similarity(name1, name2)
            
            # Weighted average of name similarities
            name_score = (lev_sim * 0.4 + jac_sim * 0.4 + soundex_sim * 0.2)
            
            if name_score > 0.6:
                weighted_scores.append((self.algorithm_weights['name_similarity'], name_score))
                evidence.append({
                    'type': 'NAME_SIMILARITY',
                    'score': round(name_score, 3),
                    'details': f"Company names {name_score:.1%} similar",
                    'weight': self.algorithm_weights['name_similarity']
                })
        
        # 2. Domain Match (strong signal for same entity)
        domain1 = extract_domain(record1.get('email', '')).lower() or safe_string(record1.get('domain', '')).lower()
        domain2 = extract_domain(record2.get('email', '')).lower() or safe_string(record2.get('domain', '')).lower()
        
        if domain1 and domain2:
            if domain1 == domain2:
                weighted_scores.append((self.algorithm_weights['domain_match'], 1.0))
                evidence.append({
                    'type': 'DOMAIN_MATCH',
                    'score': 1.0,
                    'details': f"Same domain: {domain1}",
                    'weight': self.algorithm_weights['domain_match']
                })
            elif levenshtein_similarity(domain1, domain2) > 0.8:
                domain_sim = levenshtein_similarity(domain1, domain2)
                weighted_scores.append((self.algorithm_weights['domain_match'], domain_sim))
                evidence.append({
                    'type': 'DOMAIN_SIMILAR',
                    'score': round(domain_sim, 3),
                    'details': f"Similar domains: {domain1} vs {domain2}",
                    'weight': self.algorithm_weights['domain_match']
                })
        
        # 3. Industry Match (categorical)
        industry1 = safe_string(record1.get('industry', '')).lower()
        industry2 = safe_string(record2.get('industry', '')).lower()
        
        if industry1 and industry2:
            if industry1 == industry2:
                weighted_scores.append((self.algorithm_weights['industry_match'], 1.0))
                evidence.append({
                    'type': 'INDUSTRY_MATCH',
                    'score': 1.0,
                    'details': f"Same industry: {industry1}",
                    'weight': self.algorithm_weights['industry_match']
                })
            elif levenshtein_similarity(industry1, industry2) > 0.85:
                ind_sim = levenshtein_similarity(industry1, industry2)
                weighted_scores.append((self.algorithm_weights['industry_match'], ind_sim))
                evidence.append({
                    'type': 'INDUSTRY_SIMILAR',
                    'score': round(ind_sim, 3),
                    'details': f"Similar industries: {industry1} vs {industry2}",
                    'weight': self.algorithm_weights['industry_match']
                })
        
        # 4. Address Similarity (textual)
        addr1 = safe_string(record1.get('address', '')).lower()
        addr2 = safe_string(record2.get('address', '')).lower()
        
        if addr1 and addr2:
            addr_sim = levenshtein_similarity(addr1, addr2)
            if addr_sim > 0.7:
                weighted_scores.append((self.algorithm_weights['address_similarity'], addr_sim))
                evidence.append({
                    'type': 'ADDRESS_SIMILARITY',
                    'score': round(addr_sim, 3),
                    'details': f"Addresses {addr_sim:.1%} similar",
                    'weight': self.algorithm_weights['address_similarity']
                })
        
        # 5. Phone Number Match (exact or very similar)
        phone1 = normalize_phone(record1.get('phone', ''))
        phone2 = normalize_phone(record2.get('phone', ''))
        
        if phone1 and phone2:
            if phone1 == phone2:
                weighted_scores.append((self.algorithm_weights['phone_similarity'], 1.0))
                evidence.append({
                    'type': 'PHONE_MATCH',
                    'score': 1.0,
                    'details': f"Same phone number",
                    'weight': self.algorithm_weights['phone_similarity']
                })
            elif len(phone1) >= 7 and len(phone2) >= 7:
                # Check if last 7 digits match (area code may differ)
                if phone1[-7:] == phone2[-7:]:
                    weighted_scores.append((self.algorithm_weights['phone_similarity'], 0.8))
                    evidence.append({
                        'type': 'PHONE_PARTIAL_MATCH',
                        'score': 0.8,
                        'details': "Same local number (different area code)",
                        'weight': self.algorithm_weights['phone_similarity']
                    })
        
        # 6. Email Domain Match (weaker signal)
        email1 = safe_string(record1.get('email', '')).lower()
        email2 = safe_string(record2.get('email', '')).lower()
        
        if email1 and email2:
            email_domain1 = email1.split('@')[-1] if '@' in email1 else ''
            email_domain2 = email2.split('@')[-1] if '@' in email2 else ''
            
            if email_domain1 and email_domain2 and email_domain1 == email_domain2:
                weighted_scores.append((self.algorithm_weights['email_domain_match'], 0.7))
                evidence.append({
                    'type': 'EMAIL_DOMAIN_MATCH',
                    'score': 0.7,
                    'details': f"Same email domain: {email_domain1}",
                    'weight': self.algorithm_weights['email_domain_match']
                })
        
        # Calculate weighted average confidence score
        if not weighted_scores:
            return 0.0, []
        
        total_weight = sum(weight for weight, _ in weighted_scores)
        if total_weight == 0:
            return 0.0, []
        
        confidence_score = sum(weight * score for weight, score in weighted_scores) / total_weight
        
        # Cap at 1.0
        confidence_score = min(confidence_score, 1.0)
        
        return round(confidence_score, 3), evidence
    
    def classify_match(self, confidence: float) -> Tuple[str, str]:
        """
        Classify a match based on confidence score and determine action.
        
        Args:
            confidence (float): Confidence score between 0.0 and 1.0
            
        Returns:
            Tuple[str, str]: (risk_level, recommended_action)
        """
        if confidence >= self.high_confidence_threshold:
            return "LOW", "AUTO_MERGE"
        elif confidence >= self.medium_confidence_threshold:
            return "MEDIUM", "REVIEW_REQUIRED"
        elif confidence >= self.low_confidence_threshold:
            return "HIGH", "INVESTIGATE"
        else:
            return "NONE", "NO_ACTION"
    
    def resolve_entities(self, records: List[Dict[str, Any]], 
                        min_confidence: float = 0.75) -> List[Dict[str, Any]]:
        """
        Resolve entities in a list of records by finding potential duplicates.
        
        This is the main entry point for entity resolution. It compares all pairs
        of records and returns recommendations with confidence scores and evidence.
        
        Args:
            records (List[Dict]): List of records to analyze for duplicates
            min_confidence (float): Minimum confidence threshold to include in results
            
        Returns:
            List[Dict]: List of match recommendations with details
        """
        recommendations = []
        n_records = len(records)
        
        # Compare all pairs of records (O(n^2) complexity)
        for i in range(n_records):
            for j in range(i + 1, n_records):
                record1 = records[i]
                record2 = records[j]
                
                # Calculate combined similarity score
                confidence, evidence = self.calculate_combined_score(record1, record2)
                
                # Only include matches above threshold
                if confidence >= min_confidence:
                    risk_level, action = self.classify_match(confidence)
                    
                    recommendation = {
                        'record_1_id': record1.get('id', i),
                        'record_2_id': record2.get('id', j),
                        'confidence': confidence,
                        'risk_level': risk_level,
                        'action': action,
                        'evidence': evidence,
                        'recommendation': f"{'Merge' if action == 'AUTO_MERGE' else 'Review'} records {record1.get('id', i)} and {record2.get('id', j)}",
                        'record_1_preview': self._get_record_preview(record1),
                        'record_2_preview': self._get_record_preview(record2)
                    }
                    
                    recommendations.append(recommendation)
        
        # Sort by confidence (highest first)
        recommendations.sort(key=lambda x: x['confidence'], reverse=True)
        
        return recommendations
    
    def _get_record_preview(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """Get a preview of key fields from a record."""
        return {
            'id': record.get('id'),
            'company_name': safe_string(record.get('company_name', ''))[:50],
            'email': safe_string(record.get('email', '')),
            'domain': safe_string(record.get('domain', '')),
            'industry': safe_string(record.get('industry', ''))
        }
    
    def get_resolution_summary(self, recommendations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate a summary of entity resolution results.
        
        Args:
            recommendations (List[Dict]): List of match recommendations
            
        Returns:
            Dict: Summary statistics and breakdowns
        """
        summary = {
            'total_matches': len(recommendations),
            'by_risk_level': {'LOW': 0, 'MEDIUM': 0, 'HIGH': 0},
            'by_action': defaultdict(int),
            'avg_confidence': 0.0,
            'high_confidence_count': 0,
            'unique_record_pairs': set()
        }
        
        if not recommendations:
            return summary
        
        total_confidence = 0.0
        
        for rec in recommendations:
            # Count by risk level
            risk_level = rec.get('risk_level', 'NONE')
            if risk_level in summary['by_risk_level']:
                summary['by_risk_level'][risk_level] += 1
            
            # Count by action
            action = rec.get('action', 'NO_ACTION')
            summary['by_action'][action] += 1
            
            # Track confidence
            total_confidence += rec.get('confidence', 0.0)
            
            if rec.get('confidence', 0.0) >= self.high_confidence_threshold:
                summary['high_confidence_count'] += 1
            
            # Track unique pairs
            pair = tuple(sorted([rec['record_1_id'], rec['record_2_id']]))
            summary['unique_record_pairs'].add(pair)
        
        # Calculate average confidence
        summary['avg_confidence'] = round(total_confidence / len(recommendations), 3)
        summary['unique_record_pairs'] = len(summary['unique_record_pairs'])
        
        # Convert defaultdict to regular dict for JSON serialization
        summary['by_action'] = dict(summary['by_action'])
        
        return summary
    
    def find_best_match(self, target_record: Dict[str, Any], 
                       candidate_records: List[Dict[str, Any]],
                       threshold: float = 0.85) -> Optional[Dict[str, Any]]:
        """
        Find the best matching record for a target from a list of candidates.
        
        Args:
            target_record (Dict): The record to find matches for
            candidate_records (List[Dict]): List of candidate records to compare against
            threshold (float): Minimum confidence score required
            
        Returns:
            Optional[Dict]: Best match with details, or None if no match found
        """
        best_match = None
        best_score = 0.0
        
        for candidate in candidate_records:
            score, evidence = self.calculate_combined_score(target_record, candidate)
            
            if score > best_score:
                best_score = score
                risk_level, action = self.classify_match(score)
                best_match = {
                    'candidate_id': candidate.get('id'),
                    'confidence': score,
                    'evidence': evidence,
                    'risk_level': risk_level,
                    'action': action,
                    'preview': self._get_record_preview(candidate)
                }
        
        # Return match only if it exceeds threshold
        return best_match if best_score >= threshold else None
    
    def batch_resolve(self, records_batch1: List[Dict[str, Any]], 
                     records_batch2: List[Dict[str, Any]],
                     min_confidence: float = 0.75) -> List[Dict[str, Any]]:
        """
        Resolve entities between two batches of records (cross-dataset matching).
        
        This is useful for matching records from different source systems during migration.
        
        Args:
            records_batch1 (List[Dict]): First batch of records (e.g., legacy system)
            records_batch2 (List[Dict]): Second batch of records (e.g., target system)
            min_confidence (float): Minimum confidence threshold
            
        Returns:
            List[Dict]: Cross-dataset match recommendations
        """
        recommendations = []
        
        for rec1 in records_batch1:
            for rec2 in records_batch2:
                # Skip if IDs are the same (exact match already handled)
                if rec1.get('id') == rec2.get('id'):
                    continue
                
                confidence, evidence = self.calculate_combined_score(rec1, rec2)
                
                if confidence >= min_confidence:
                    risk_level, action = self.classify_match(confidence)
                    
                    recommendations.append({
                        'source_record_id': rec1.get('id'),
                        'target_record_id': rec2.get('id'),
                        'confidence': confidence,
                        'risk_level': risk_level,
                        'action': action,
                        'evidence': evidence,
                        'match_type': 'CROSS_DATASET'
                    })
        
        # Sort by confidence
        recommendations.sort(key=lambda x: x['confidence'], reverse=True)
        
        return recommendations


# Convenience function for quick entity resolution
def resolve_entities_quick(records: List[Dict[str, Any]], 
                          threshold: float = 0.75) -> List[Dict[str, Any]]:
    """
    Quick entity resolution with default settings.
    
    Args:
        records (List[Dict]): Records to analyze
        threshold (float): Minimum confidence threshold
        
    Returns:
        List[Dict]: Match recommendations
    """
    resolver = EntityResolver()
    return resolver.resolve_entities(records, min_confidence=threshold)
