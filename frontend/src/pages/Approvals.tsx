import { useState, useEffect } from 'react';
import { fetchEntityResolution, approveRecommendation, rejectRecommendation } from '../services/api';
import type { EntityResolutionResponse, Recommendation } from '../types/models';
import RecommendationCard from '../components/RecommendationCard';

export default function Approvals() {
  const [data, setData] = useState<EntityResolutionResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filter, setFilter] = useState<'all' | 'review_required' | 'investigate'>('all');

  useEffect(() => {
    loadRecommendations();
  }, []);

  const loadRecommendations = async () => {
    try {
      setLoading(true);
      setError(null);
      const result = await fetchEntityResolution();
      setData(result);
    } catch (err) {
      setError('Failed to load recommendations. Make sure the backend is running.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleApprove = async (record1Id: number | string, record2Id: number | string) => {
    try {
      await approveRecommendation(record1Id, record2Id);
      // Refresh the list
      loadRecommendations();
    } catch (err) {
      console.error('Failed to approve recommendation:', err);
      alert('Failed to approve recommendation. Please try again.');
    }
  };

  const handleReject = async (record1Id: number | string, record2Id: number | string) => {
    try {
      await rejectRecommendation(record1Id, record2Id);
      // Refresh the list
      loadRecommendations();
    } catch (err) {
      console.error('Failed to reject recommendation:', err);
      alert('Failed to reject recommendation. Please try again.');
    }
  };

  const filteredRecommendations = data?.recommendations.filter(rec => {
    if (filter === 'all') return true;
    if (filter === 'review_required') return rec.action === 'REVIEW_REQUIRED';
    if (filter === 'investigate') return rec.action === 'INVESTIGATE';
    return true;
  }) || [];

  const stats = {
    total: filteredRecommendations.length,
    reviewRequired: filteredRecommendations.filter(r => r.action === 'REVIEW_REQUIRED').length,
    investigate: filteredRecommendations.filter(r => r.action === 'INVESTIGATE').length,
    autoMerge: filteredRecommendations.filter(r => r.action === 'AUTO_MERGE').length,
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="animate-pulse space-y-8">
            <div className="h-8 bg-gray-200 rounded w-1/3"></div>
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              {[...Array(4)].map((_, i) => (
                <div key={i} className="h-16 bg-gray-200 rounded-lg"></div>
              ))}
            </div>
            <div className="space-y-4">
              {[...Array(3)].map((_, i) => (
                <div key={i} className="h-48 bg-gray-200 rounded-lg"></div>
              ))}
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="bg-red-50 border border-red-200 rounded-lg p-6">
            <p className="text-red-800">{error}</p>
            <button
              onClick={loadRecommendations}
              className="mt-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
            >
              Retry
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Approval Queue</h1>
          <button
            onClick={loadRecommendations}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
          >
            Refresh
          </button>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
          <div className="bg-white rounded-lg shadow p-4">
            <p className="text-sm font-medium text-gray-500">Total Items</p>
            <p className="text-2xl font-bold text-gray-900 mt-1">{stats.total}</p>
          </div>
          <div className="bg-white rounded-lg shadow p-4">
            <p className="text-sm font-medium text-gray-500">Review Required</p>
            <p className="text-2xl font-bold text-orange-600 mt-1">{stats.reviewRequired}</p>
          </div>
          <div className="bg-white rounded-lg shadow p-4">
            <p className="text-sm font-medium text-gray-500">Investigate</p>
            <p className="text-2xl font-bold text-red-600 mt-1">{stats.investigate}</p>
          </div>
          <div className="bg-white rounded-lg shadow p-4">
            <p className="text-sm font-medium text-gray-500">Auto-Merge</p>
            <p className="text-2xl font-bold text-green-600 mt-1">{stats.autoMerge}</p>
          </div>
        </div>

        {/* Filters */}
        <div className="mb-6 flex space-x-4">
          <button
            onClick={() => setFilter('all')}
            className={`px-4 py-2 rounded-lg ${
              filter === 'all'
                ? 'bg-blue-600 text-white'
                : 'bg-white text-gray-700 hover:bg-gray-50'
            }`}
          >
            All ({data?.total_matches || 0})
          </button>
          <button
            onClick={() => setFilter('review_required')}
            className={`px-4 py-2 rounded-lg ${
              filter === 'review_required'
                ? 'bg-orange-600 text-white'
                : 'bg-white text-gray-700 hover:bg-gray-50'
            }`}
          >
            Review Required ({stats.reviewRequired})
          </button>
          <button
            onClick={() => setFilter('investigate')}
            className={`px-4 py-2 rounded-lg ${
              filter === 'investigate'
                ? 'bg-red-600 text-white'
                : 'bg-white text-gray-700 hover:bg-gray-50'
            }`}
          >
            Investigate ({stats.investigate})
          </button>
        </div>

        {/* Recommendations List */}
        {filteredRecommendations.length === 0 ? (
          <div className="bg-white rounded-lg shadow p-12 text-center">
            <p className="text-gray-500 text-lg">No recommendations to display</p>
          </div>
        ) : (
          <div className="space-y-4">
            {filteredRecommendations.map((rec, index) => (
              <RecommendationCard
                key={`${rec.record_1_id}-${rec.record_2_id}-${index}`}
                recommendation={rec}
                onApprove={() => handleApprove(rec.record_1_id, rec.record_2_id)}
                onReject={() => handleReject(rec.record_1_id, rec.record_2_id)}
              />
            ))}
          </div>
        )}

        {/* Pagination placeholder */}
        {filteredRecommendations.length > 0 && (
          <div className="mt-8 flex justify-center">
            <nav className="flex space-x-2">
              <button className="px-4 py-2 bg-white rounded-lg border hover:bg-gray-50 disabled:opacity-50" disabled>
                Previous
              </button>
              <button className="px-4 py-2 bg-blue-600 text-white rounded-lg">1</button>
              <button className="px-4 py-2 bg-white rounded-lg border hover:bg-gray-50">2</button>
              <button className="px-4 py-2 bg-white rounded-lg border hover:bg-gray-50">3</button>
              <button className="px-4 py-2 bg-white rounded-lg border hover:bg-gray-50">
                Next
              </button>
            </nav>
          </div>
        )}
      </div>
    </div>
  );
}
