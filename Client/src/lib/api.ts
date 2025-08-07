interface ImportMetaEnv {
  readonly VITE_API_URL: string
  readonly VITE_APP_NAME: string
  // add more env variables as needed
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}

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

  constructor(baseURL: string = API_BASE_URL) {
    this.baseURL = baseURL;
  }

  async analyzeFile(file: File): Promise<AnalysisResults> {
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch(`${this.baseURL}/analyze`, {
      method: 'POST',
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
    const response = await fetch(`${this.baseURL}/formats`);
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return response.json();
  }

  async healthCheck(): Promise<any> {
    const response = await fetch(`${this.baseURL.replace('/api', '')}/health`);
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return response.json();
  }
}

export const apiClient = new ApiClient();