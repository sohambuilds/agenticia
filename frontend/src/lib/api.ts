import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Add detailed logging for debugging
console.log('🔧 API Configuration:', {
  NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL,
  API_BASE_URL: API_BASE_URL,
  NODE_ENV: process.env.NODE_ENV,
  timestamp: new Date().toISOString()
});

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000, // 30 second timeout
});

// Add request interceptor for logging
apiClient.interceptors.request.use(
  (config) => {
    console.log('📤 API Request:', {
      method: config.method?.toUpperCase(),
      url: config.url,
      baseURL: config.baseURL,
      fullURL: `${config.baseURL}${config.url}`,
      headers: config.headers,
      data: config.data,
      timestamp: new Date().toISOString()
    });
    return config;
  },
  (error) => {
    console.error('📤 Request Error:', error);
    return Promise.reject(error);
  }
);

// Add response interceptor for logging
apiClient.interceptors.response.use(
  (response) => {
    console.log('📥 API Response Success:', {
      status: response.status,
      statusText: response.statusText,
      url: response.config.url,
      data: response.data,
      timestamp: new Date().toISOString()
    });
    return response;
  },
  (error) => {
    console.error('📥 API Response Error:', {
      message: error.message,
      code: error.code,
      status: error.response?.status,
      statusText: error.response?.statusText,
      url: error.config?.url,
      responseData: error.response?.data,
      timestamp: new Date().toISOString()
    });
    return Promise.reject(error);
  }
);

// Types for our API
export interface ChatMessage {
  message: string;
  conversation_id?: string;
}

export interface ChatResponse {
  response: string;
  agent_used: 'tutor' | 'math' | 'physics';
  conversation_id: string;
  metadata?: {
    tools_used?: string[];
    confidence?: number;
    agent_metadata?: Record<string, unknown>;
    error?: string;
  };
}

export interface AgentInfo {
  available_agents: string[];
  agent_descriptions: Record<string, string>;
  routing_info: Record<string, unknown>;
  status: string;
}

export interface HealthResponse {
  status: string;
  service: string;
  agents_available: string[];
}

// API functions
export const chatAPI = {
  sendMessage: async (message: string, conversationId?: string): Promise<ChatResponse> => {
    try {
      const response = await apiClient.post<ChatResponse>('/api/chat', {
        message,
        conversation_id: conversationId,
      });
      return response.data;
    } catch (error) {
      console.error('Chat API error:', error);
      throw new Error('Failed to send message');
    }
  },

  getAgentInfo: async (): Promise<AgentInfo> => {
    try {
      const response = await apiClient.get<AgentInfo>('/api/agents');
      return response.data;
    } catch (error) {
      console.error('Agent info API error:', error);
      throw new Error('Failed to get agent information');
    }
  },

  checkHealth: async (): Promise<HealthResponse> => {
    try {
      const response = await apiClient.get<HealthResponse>('/api/health');
      return response.data;
    } catch (error) {
      console.error('Health check API error:', error);
      throw new Error('Failed to check system health');
    }
  },
};

export default apiClient; 