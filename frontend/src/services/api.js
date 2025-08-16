import axios from 'axios';

// Create axios instance with base configuration
const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:5000',
  timeout: 30000, // 30 seconds timeout
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for logging
api.interceptors.request.use(
  (config) => {
    console.log(`API Request: ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    console.error('API Request Error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => {
    console.log(`API Response: ${response.status} ${response.config.url}`);
    return response;
  },
  (error) => {
    console.error('API Response Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

// API endpoints
export const apiEndpoints = {
  // Main analysis endpoint
  analyze: '/api/analyze',
  
  // Disaster classification
  classify: '/api/classify',
  
  // Fact checking
  factCheck: '/api/fact-check',
  
  // Authorities
  authorities: '/api/authorities',
  contactAuthority: '/api/contact-authority',
  
  // Image upload
  uploadImage: '/api/upload-image',
  
  // Batch analysis
  batchAnalyze: '/api/batch-analyze',
  
  // Statistics
  statistics: '/api/statistics',
  
  // Health check
  health: '/health',
  
  // Integrated system endpoints
  integratedProcess: '/api/integrated/process',
  integratedSummary: '/api/integrated/summary',
  integratedSubscribe: '/api/integrated/subscribe',
  integratedLoadDetector: '/api/integrated/load-detector',
  integratedProcessCrisisNLP: '/api/integrated/process-crisisnlp',
};

// API service functions
export const apiService = {
  // Analyze a single tweet
  async analyzeTweet(data) {
    try {
      const response = await api.post(apiEndpoints.analyze, data);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.error || 'Failed to analyze tweet');
    }
  },

  // Classify disaster type
  async classifyDisaster(data) {
    try {
      const response = await api.post(apiEndpoints.classify, data);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.error || 'Failed to classify disaster');
    }
  },

  // Fact check a tweet
  async factCheck(data) {
    try {
      const response = await api.post(apiEndpoints.factCheck, data);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.error || 'Failed to fact check');
    }
  },

  // Get authorities for a location
  async getAuthorities(location, disasterType = null) {
    try {
      const params = { location };
      if (disasterType) params.disaster_type = disasterType;
      
      const response = await api.get(apiEndpoints.authorities, { params });
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.error || 'Failed to get authorities');
    }
  },

  // Contact authority
  async contactAuthority(data) {
    try {
      const response = await api.post(apiEndpoints.contactAuthority, data);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.error || 'Failed to contact authority');
    }
  },

  // Upload image
  async uploadImage(formData) {
    try {
      const response = await api.post(apiEndpoints.uploadImage, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.error || 'Failed to upload image');
    }
  },

  // Batch analyze multiple tweets
  async batchAnalyze(data) {
    try {
      const response = await api.post(apiEndpoints.batchAnalyze, data);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.error || 'Failed to batch analyze');
    }
  },

  // Get system statistics
  async getStatistics() {
    try {
      const response = await api.get(apiEndpoints.statistics);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.error || 'Failed to get statistics');
    }
  },

  // Health check
  async healthCheck() {
    try {
      const response = await api.get(apiEndpoints.health);
      return response.data;
    } catch (error) {
      throw new Error('Backend service is not available');
    }
  },

  // Integrated system endpoints
  async integratedProcess(data) {
    try {
      const response = await api.post(apiEndpoints.integratedProcess, data);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.error || 'Failed to process integrated analysis');
    }
  },

  async integratedSummary() {
    try {
      const response = await api.get(apiEndpoints.integratedSummary);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.error || 'Failed to get integrated summary');
    }
  },

  async integratedSubscribe(topicId, location = null) {
    try {
      const params = { topic_id: topicId };
      if (location) params.location = location;
      
      const response = await api.get(apiEndpoints.integratedSubscribe, { params });
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.error || 'Failed to subscribe to topic');
    }
  },

  async integratedLoadDetector(data) {
    try {
      const response = await api.post(apiEndpoints.integratedLoadDetector, data);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.error || 'Failed to load detector');
    }
  },

  async integratedProcessCrisisNLP(data) {
    try {
      const response = await api.post(apiEndpoints.integratedProcessCrisisNLP, data);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.error || 'Failed to process CrisisNLP data');
    }
  },
};

export default apiService;
