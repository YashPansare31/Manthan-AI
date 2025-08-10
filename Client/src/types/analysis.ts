// This file doesn't exist yet - CREATE IT
export interface AnalysisResults {
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

export interface FileUploadProps {
  onFileAnalyzed: (results: AnalysisResults) => void;
  isProcessing: boolean;
  setIsProcessing: (processing: boolean) => void;
}