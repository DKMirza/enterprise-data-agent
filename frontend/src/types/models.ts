// Type definitions for Enterprise Data Migration Platform API

export interface RecordPreview {
  id: number | string;
  company_name: string;
  email: string;
  domain: string;
  industry: string;
}

export interface EvidenceItem {
  type: string;
  score: number;
  details: string;
  weight?: number;
}

export interface Recommendation {
  record_1_id: number | string;
  record_2_id: number | string;
  confidence: number;
  risk_level: 'LOW' | 'MEDIUM' | 'HIGH';
  action: 'AUTO_MERGE' | 'REVIEW_REQUIRED' | 'INVESTIGATE' | 'NO_ACTION';
  evidence: EvidenceItem[];
  recommendation?: string;
  record_1_preview?: RecordPreview;
  record_2_preview?: RecordPreview;
}

export interface ResolutionSummary {
  total_matches: number;
  by_risk_level: {
    LOW: number;
    MEDIUM: number;
    HIGH: number;
  };
  by_action: Record<string, number>;
  avg_confidence: number;
  high_confidence_count?: number;
}

export interface EntityResolutionResponse {
  total_matches: number;
  summary: ResolutionSummary;
  recommendations: Recommendation[];
}

export interface QualityReport {
  total_records: number;
  duplicates_found: number;
  missing_fields: Record<string, number>;
  invalid_emails: number;
  recommendations: string[];
}

export interface EntityResolutionRequest {
  records?: any[];
  min_confidence?: number;
}

export type ApprovalStatus = 'pending' | 'approved' | 'rejected';

export interface ApprovedRecommendation extends Recommendation {
  approval_status: ApprovalStatus;
  approved_at?: Date;
  approved_by?: string;
}
