interface ImportMetaEnv {
  readonly VITE_API_URL: string
  readonly VITE_APP_NAME: string
  readonly VITE_AUTH0_DOMAIN: string
  readonly VITE_AUTH0_CLIENT_ID: string
  readonly VITE_AUTH0_AUDIENCE: string
  // add more env variables as needed
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}

// Add Auth0 import for the hook
import { useAuth0 } from '@auth0/auth0-react'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

// Frontend interface (what components expect)
export interface AnalysisResults {
  transcription: string;
  summary: string;
  action_items: string[];
  decision_points: string[];
  processing_time: number;
}

// Backend interface (what API returns)
interface BackendAnalysisResponse {
  transcript: Array<{
    id: string;
    speaker: string;
    text: string;
    start_time: number;
    end_time: number;
    confidence: number;
  }>;
  summary: string;
  action_items: Array<{
    id: string;
    text: string;
    assignee?: string;
    deadline?: string;
    priority: string;
    confidence: number;
  }>;
  key_decisions: Array<{
    id: string;
    decision: string;
    rationale?: string;
    impact: string;
    confidence: number;
  }>;
  processing_time: number;
}

// Transform backend response to frontend format
function transformBackendResponse(backendData: BackendAnalysisResponse): AnalysisResults {
  return {
    transcription: backendData.transcript?.map(segment => segment.text).join(' ') || '',
    summary: backendData.summary || '',
    action_items: backendData.action_items?.map(item => item.text) || [],
    decision_points: backendData.key_decisions?.map(decision => decision.decision) || [],
    processing_time: backendData.processing_time || 0
  };
}

export class ApiClient {
  private baseURL: string;
  private getAccessToken?: () => Promise<string>;

  constructor(baseURL: string = API_BASE_URL, getAccessToken?: () => Promise<string>) {
    this.baseURL = baseURL;
    this.getAccessToken = getAccessToken;
  }

  private async getAuthHeaders(): Promise<HeadersInit> {
    const headers: HeadersInit = {};

    if (this.getAccessToken) {
      try {
        const token = await this.getAccessToken();
        headers['Authorization'] = `Bearer ${token}`;
      } catch (error) {
        console.warn('Failed to get access token:', error);
      }
    }

    return headers;
  }

  async analyzeFile(file: File): Promise<AnalysisResults> {
    const formData = new FormData();
    formData.append('file', file);

    const authHeaders = await this.getAuthHeaders();

    const response = await fetch(`${this.baseURL}/analyze`, {
      method: 'POST',
      headers: authHeaders,
      body: formData,
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
    }

    const backendData: BackendAnalysisResponse = await response.json();
    return transformBackendResponse(backendData);
  }

  async getSupportedFormats(): Promise<any> {
    const authHeaders = await this.getAuthHeaders();

    const response = await fetch(`${this.baseURL}/formats`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        ...authHeaders,
      },
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return response.json();
  }

  async healthCheck(): Promise<any> {
    const authHeaders = await this.getAuthHeaders();

    const response = await fetch(`${this.baseURL.replace('/api', '')}/health`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        ...authHeaders,
      },
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return response.json();
  }
}

// Create authenticated API client hook
export const useAuthenticatedApiClient = () => {
  const { getAccessTokenSilently, isAuthenticated } = useAuth0();
  
  return new ApiClient(
    API_BASE_URL, 
    isAuthenticated ? getAccessTokenSilently : undefined
  );
};

// Keep the default client for backwards compatibility (non-authenticated)
export const apiClient = new ApiClient();