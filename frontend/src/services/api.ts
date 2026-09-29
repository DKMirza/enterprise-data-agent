import axios from 'axios';
import { 
  EntityResolutionResponse, 
  QualityReport, 
  EntityResolutionRequest,
  Recommendation 
} from '../types/models';

const API_BASE_URL = '/api';

// Create axios instance with base configuration
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request interceptor for debugging
apiClient.interceptors.request.use(
  (config) => {
    console.log('API Request:', config.method?.toUpperCase(), config.url);
    return config;
  },
  (error) => {
    console.error('Request error:', error);
    return Promise.reject(error);
  }
);

// Add response interceptor for debugging
apiClient.interceptors.response.use(
  (response) => {
    console.log('API Response:', response.status, response.config.url);
    return response;
  },
  (error) => {
    if (error.response) {
      console.error('Response error:', error.response.status, error.response.data);
    } else if (error.request) {
      console.error('No response received:', error.request);
    } else {
      console.error('Request setup error:', error.message);
    }
    return Promise.reject(error);
  }
);

/**
 * Fetch entity resolution recommendations from the backend
 */
export const fetchEntityResolution = async (
  request: EntityResolutionRequest = {}
): Promise<EntityResolutionResponse> => {
  try {
    const response = await apiClient.post('/resolve-entities', request);
    return response.data;
  } catch (error) {
    console.error('Error fetching entity resolution:', error);
    throw new Error('Failed to fetch entity resolution data');
  }
};

/**
 * Fetch quality report from the backend
 */
export const fetchQualityReport = async (): Promise<QualityReport> => {
  try {
    const response = await apiClient.get('/quality-report');
    return response.data;
  } catch (error) {
    console.error('Error fetching quality report:', error);
    throw new Error('Failed to fetch quality report');
  }
};

/**
 * Generate synthetic data for testing
 */
export const generateSyntheticData = async (numRecords: number = 100): Promise<any> => {
  try {
    const response = await apiClient.post('/generate-synthetic-data', { num_records: numRecords });
    return response.data;
  } catch (error) {
    console.error('Error generating synthetic data:', error);
    throw new Error('Failed to generate synthetic data');
  }
};

/**
 * Approve a recommendation (placeholder - implement backend endpoint first)
 */
export const approveRecommendation = async (
  record1Id: number | string, 
  record2Id: number | string
): Promise<void> => {
  // TODO: Implement backend endpoint for approval
  console.log(`Approving merge of records ${record1Id} and ${record2Id}`);
};

/**
 * Reject a recommendation (placeholder - implement backend endpoint first)
 */
export const rejectRecommendation = async (
  record1Id: number | string, 
  record2Id: number | string,
  reason?: string
): Promise<void> => {
  // TODO: Implement backend endpoint for rejection
  console.log(`Rejecting merge of records ${record1Id} and ${record2Id}`, reason ? `Reason: ${reason}` : '');
};

/**
 * Check API health status
 */
export const checkHealth = async (): Promise<any> => {
  try {
    const response = await apiClient.get('/health');
    return response.data;
  } catch (error) {
    console.error('Error checking health:', error);
    throw new Error('API is not responding');
  }
};

export default apiClient;
