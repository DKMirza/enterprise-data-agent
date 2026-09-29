import { ArrowRight, FileText } from 'lucide-react';
import ConfidenceMeter from './ConfidenceMeter';
import RiskBadge from './RiskBadge';
import { Recommendation } from '../types/models';

interface RecommendationCardProps {
  recommendation: Recommendation;
  onApprove?: (rec: Recommendation) => void;
  onReject?: (rec: Recommendation) => void;
}

const RecommendationCard = ({ 
  recommendation, 
  onApprove, 
  onReject 
}: RecommendationCardProps) => {
  const {
    record_1_id,
    record_2_id,
    confidence,
    risk_level,
    action,
    evidence,
    record_1_preview,
    record_2_preview,
  } = recommendation;

  return (
    <div className="bg-white rounded-xl shadow-sm border border-slate-200 card-hover overflow-hidden">
      {/* Header */}
      <div className="px-6 py-4 bg-slate-50 border-b border-slate-200 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <span className="text-sm font-mono text-slate-500">
            #{record_1_id} ↔ #{record_2_id}
          </span>
          <RiskBadge riskLevel={risk_level} />
        </div>
        <span className={`px-3 py-1 rounded-full text-xs font-semibold ${
          action === 'AUTO_MERGE' 
            ? 'bg-blue-100 text-blue-700' 
            : action === 'REVIEW_REQUIRED'
            ? 'bg-purple-100 text-purple-700'
            : 'bg-orange-100 text-orange-700'
        }`}>
          {action.replace('_', ' ')}
        </span>
      </div>

      {/* Body */}
      <div className="p-6">
        {/* Record Comparison */}
        <div className="grid grid-cols-2 gap-4 mb-6">
          {/* Record 1 */}
          <div className="bg-slate-50 rounded-lg p-4 border border-slate-200">
            <h4 className="text-sm font-semibold text-slate-700 mb-3 flex items-center gap-2">
              <FileText className="w-4 h-4" />
              Record {record_1_id}
            </h4>
            <div className="space-y-2 text-sm">
              <div>
                <span className="text-slate-500">Company:</span>
                <p className="font-medium text-slate-900">{record_1_preview?.company_name || 'N/A'}</p>
              </div>
              <div>
                <span className="text-slate-500">Email:</span>
                <p className="text-slate-700">{record_1_preview?.email || 'N/A'}</p>
              </div>
              <div>
                <span className="text-slate-500">Domain:</span>
                <p className="text-slate-700">{record_1_preview?.domain || 'N/A'}</p>
              </div>
              {record_1_preview?.industry && (
                <div>
                  <span className="text-slate-500">Industry:</span>
                  <p className="text-slate-700">{record_1_preview.industry}</p>
                </div>
              )}
            </div>
          </div>

          {/* Record 2 */}
          <div className="bg-slate-50 rounded-lg p-4 border border-slate-200">
            <h4 className="text-sm font-semibold text-slate-700 mb-3 flex items-center gap-2">
              <FileText className="w-4 h-4" />
              Record {record_2_id}
            </h4>
            <div className="space-y-2 text-sm">
              <div>
                <span className="text-slate-500">Company:</span>
                <p className="font-medium text-slate-900">{record_2_preview?.company_name || 'N/A'}</p>
              </div>
              <div>
                <span className="text-slate-500">Email:</span>
                <p className="text-slate-700">{record_2_preview?.email || 'N/A'}</p>
              </div>
              <div>
                <span className="text-slate-500">Domain:</span>
                <p className="text-slate-700">{record_2_preview?.domain || 'N/A'}</p>
              </div>
              {record_2_preview?.industry && (
                <div>
                  <span className="text-slate-500">Industry:</span>
                  <p className="text-slate-700">{record_2_preview.industry}</p>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Confidence Meter */}
        <div className="mb-6">
          <ConfidenceMeter confidence={confidence} />
        </div>

        {/* Evidence */}
        {evidence && evidence.length > 0 && (
          <div className="mb-6">
            <h4 className="text-sm font-semibold text-slate-700 mb-3">Matching Evidence</h4>
            <div className="space-y-2">
              {evidence.map((item, index) => (
                <div 
                  key={index}
                  className="flex items-start gap-2 p-2 bg-green-50 rounded-lg border border-green-100"
                >
                  <span className="text-green-600 text-xs font-semibold mt-0.5">✓</span>
                  <div className="flex-1">
                    <p className="text-sm text-slate-800">{item.details}</p>
                    <p className="text-xs text-slate-500">
                      {item.type.replace('_', ' ')} • Score: {(item.score * 100).toFixed(0)}%
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Actions */}
        <div className="flex items-center justify-end gap-3 pt-4 border-t border-slate-200">
          <button
            onClick={() => onReject?.(recommendation)}
            className="px-4 py-2 text-sm font-medium text-red-700 bg-red-50 hover:bg-red-100 rounded-lg transition-colors"
          >
            Reject
          </button>
          <button
            onClick={() => onApprove?.(recommendation)}
            className="px-4 py-2 text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 rounded-lg transition-colors flex items-center gap-2"
          >
            Approve Merge
            <ArrowRight className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  );
};

export default RecommendationCard;
