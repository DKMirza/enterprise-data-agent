import { Filter, SortDesc } from 'lucide-react';
import RecommendationCard from './RecommendationCard';
import { Recommendation } from '../types/models';

interface RecommendationsListProps {
  recommendations: Recommendation[];
  onApprove?: (rec: Recommendation) => void;
  onReject?: (rec: Recommendation) => void;
}

type SortOption = 'confidence-desc' | 'confidence-asc' | 'risk-level';
type FilterOption = 'all' | 'LOW' | 'MEDIUM' | 'HIGH';

const RecommendationsList = ({ 
  recommendations, 
  onApprove, 
  onReject 
}: RecommendationsListProps) => {
  const [sortBy, setSortBy] = SortOption('confidence-desc');
  const [filterBy, setFilterBy] = FilterOption('all');

  // Filter and sort recommendations
  const filteredRecommendations = recommendations
    .filter((rec) => filterBy === 'all' || rec.risk_level === filterBy)
    .sort((a, b) => {
      switch (sortBy) {
        case 'confidence-desc':
          return b.confidence - a.confidence;
        case 'confidence-asc':
          return a.confidence - b.confidence;
        case 'risk-level':
          const riskOrder = { LOW: 1, MEDIUM: 2, HIGH: 3 };
          return riskOrder[a.risk_level] - riskOrder[b.risk_level];
        default:
          return 0;
      }
    });

  if (recommendations.length === 0) {
    return (
      <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-12 text-center">
        <p className="text-slate-500 text-lg">No recommendations found</p>
        <p className="text-slate-400 text-sm mt-2">Run entity resolution to find duplicates</p>
      </div>
    );
  }

  return (
    <div>
      {/* Filters and Sort */}
      <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-4 mb-6">
        <div className="flex items-center justify-between flex-wrap gap-4">
          <div className="flex items-center gap-2">
            <Filter className="w-4 h-4 text-slate-500" />
            <span className="text-sm font-medium text-slate-700">Filter by Risk:</span>
            <select
              value={filterBy}
              onChange={(e) => setFilterBy(e.target.value as FilterOption)}
              className="text-sm border-slate-300 rounded-lg focus:ring-primary-500 focus:border-primary-500"
            >
              <option value="all">All</option>
              <option value="LOW">Low (Auto-Merge)</option>
              <option value="MEDIUM">Medium (Review)</option>
              <option value="HIGH">High (Investigate)</option>
            </select>
          </div>

          <div className="flex items-center gap-2">
            <SortDesc className="w-4 h-4 text-slate-500" />
            <span className="text-sm font-medium text-slate-700">Sort by:</span>
            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value as SortOption)}
              className="text-sm border-slate-300 rounded-lg focus:ring-primary-500 focus:border-primary-500"
            >
              <option value="confidence-desc">Confidence (High to Low)</option>
              <option value="confidence-asc">Confidence (Low to High)</option>
              <option value="risk-level">Risk Level</option>
            </select>
          </div>

          <span className="text-sm text-slate-500">
            Showing {filteredRecommendations.length} of {recommendations.length} recommendations
          </span>
        </div>
      </div>

      {/* Recommendations Grid */}
      <div className="space-y-4">
        {filteredRecommendations.map((rec, index) => (
          <RecommendationCard
            key={`${rec.record_1_id}-${rec.record_2_id}-${index}`}
            recommendation={rec}
            onApprove={onApprove}
            onReject={onReject}
          />
        ))}
      </div>
    </div>
  );
};

export default RecommendationsList;
