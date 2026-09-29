import { useState, useEffect } from 'react';
import { fetchQualityReport } from '../services/api';
import type { QualityReport } from '../types/models';

export default function Dashboard() {
  const [qualityData, setQualityData] = useState<QualityReport | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadQualityReport();
  }, []);

  const loadQualityReport = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await fetchQualityReport();
      setQualityData(data);
    } catch (err) {
      setError('Failed to load quality report. Make sure the backend is running.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="animate-pulse space-y-8">
            <div className="h-8 bg-gray-200 rounded w-1/3"></div>
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
              {[...Array(4)].map((_, i) => (
                <div key={i} className="h-32 bg-gray-200 rounded-lg"></div>
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
              onClick={loadQualityReport}
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
        <h1 className="text-3xl font-bold text-gray-900 mb-8">Data Quality Dashboard</h1>

        {/* Summary Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow p-6">
            <p className="text-sm font-medium text-gray-500">Total Records</p>
            <p className="text-3xl font-bold text-gray-900 mt-2">
              {qualityData?.total_records?.toLocaleString() || 'N/A'}
            </p>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <p className="text-sm font-medium text-gray-500">Duplicates Found</p>
            <p className="text-3xl font-bold text-orange-600 mt-2">
              {qualityData?.duplicates_found?.toLocaleString() || 'N/A'}
            </p>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <p className="text-sm font-medium text-gray-500">Auto-Merged</p>
            <p className="text-3xl font-bold text-green-600 mt-2">
              {qualityData?.auto_merged?.toLocaleString() || 'N/A'}
            </p>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <p className="text-sm font-medium text-gray-500">Pending Review</p>
            <p className="text-3xl font-bold text-blue-600 mt-2">
              {qualityData?.pending_review?.toLocaleString() || 'N/A'}
            </p>
          </div>
        </div>

        {/* Quality Metrics */}
        <div className="bg-white rounded-lg shadow mb-8">
          <div className="px-6 py-4 border-b border-gray-200">
            <h2 className="text-xl font-semibold text-gray-900">Quality Metrics</h2>
          </div>
          <div className="p-6 space-y-4">
            {qualityData?.metrics && (
              <>
                <div>
                  <div className="flex justify-between mb-1">
                    <span className="text-sm font-medium text-gray-700">Completeness</span>
                    <span className="text-sm font-medium text-gray-700">{qualityData.metrics.completeness}%</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2.5">
                    <div
                      className="bg-green-600 h-2.5 rounded-full transition-all duration-500"
                      style={{ width: `${qualityData.metrics.completeness}%` }}
                    ></div>
                  </div>
                </div>

                <div>
                  <div className="flex justify-between mb-1">
                    <span className="text-sm font-medium text-gray-700">Accuracy</span>
                    <span className="text-sm font-medium text-gray-700">{qualityData.metrics.accuracy}%</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2.5">
                    <div
                      className="bg-blue-600 h-2.5 rounded-full transition-all duration-500"
                      style={{ width: `${qualityData.metrics.accuracy}%` }}
                    ></div>
                  </div>
                </div>

                <div>
                  <div className="flex justify-between mb-1">
                    <span className="text-sm font-medium text-gray-700">Consistency</span>
                    <span className="text-sm font-medium text-gray-700">{qualityData.metrics.consistency}%</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2.5">
                    <div
                      className="bg-purple-600 h-2.5 rounded-full transition-all duration-500"
                      style={{ width: `${qualityData.metrics.consistency}%` }}
                    ></div>
                  </div>
                </div>

                <div>
                  <div className="flex justify-between mb-1">
                    <span className="text-sm font-medium text-gray-700">Uniqueness</span>
                    <span className="text-sm font-medium text-gray-700">{qualityData.metrics.uniqueness}%</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2.5">
                    <div
                      className="bg-orange-600 h-2.5 rounded-full transition-all duration-500"
                      style={{ width: `${qualityData.metrics.uniqueness}%` }}
                    ></div>
                  </div>
                </div>
              </>
            )}
          </div>
        </div>

        {/* Recent Activity */}
        <div className="bg-white rounded-lg shadow">
          <div className="px-6 py-4 border-b border-gray-200">
            <h2 className="text-xl font-semibold text-gray-900">Recent Entity Resolution</h2>
          </div>
          <div className="p-6">
            <p className="text-gray-500 text-sm">
              Last run: {qualityData?.last_run || 'Never'}
            </p>
            {qualityData?.summary && (
              <div className="mt-4 grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="text-center p-4 bg-gray-50 rounded-lg">
                  <p className="text-sm text-gray-600">High Confidence</p>
                  <p className="text-2xl font-bold text-green-600 mt-1">
                    {qualityData.summary.high_confidence || 0}
                  </p>
                </div>
                <div className="text-center p-4 bg-gray-50 rounded-lg">
                  <p className="text-sm text-gray-600">Medium Confidence</p>
                  <p className="text-2xl font-bold text-orange-600 mt-1">
                    {qualityData.summary.medium_confidence || 0}
                  </p>
                </div>
                <div className="text-center p-4 bg-gray-50 rounded-lg">
                  <p className="text-sm text-gray-600">Low Confidence</p>
                  <p className="text-2xl font-bold text-red-600 mt-1">
                    {qualityData.summary.low_confidence || 0}
                  </p>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
