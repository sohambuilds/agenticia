import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000, // 30 second timeout
});

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
    agent_metadata?: any;
    error?: string;
  };
}

export interface AgentInfo {
  available_agents: string[];
  agent_descriptions: Record<string, string>;
  routing_info: any;
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