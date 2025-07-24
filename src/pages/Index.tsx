import { useState } from 'react';
import { Header } from '@/components/Header';
import { FileUpload } from '@/components/FileUpload';
import { ResultsSection } from '@/components/ResultsSection';
import { FloatingActionButton } from '@/components/FloatingActionButton';
import { useToast } from '@/hooks/use-toast';
import heroBackground from '@/assets/hero-background.jpg';

interface AnalysisResults {
  transcription: string;
  summary: string;
  action_items: string[];
  decision_points: string[];
  processing_time: number;
}

const Index = () => {
  const [results, setResults] = useState<AnalysisResults | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const { toast } = useToast();

  const handleFileAnalyzed = (analysisResults: AnalysisResults) => {
    setResults(analysisResults);
  };

  const handleNewUpload = () => {
    setResults(null);
  };

  const handleExport = () => {
    if (!results) return;
    
    const exportData = {
      transcription: results.transcription,
      summary: results.summary,
      action_items: results.action_items,
      decision_points: results.decision_points,
      exported_at: new Date().toISOString(),
    };
    
    const blob = new Blob([JSON.stringify(exportData, null, 2)], { 
      type: 'application/json' 
    });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `meeting-analysis-${Date.now()}.json`;
    a.click();
    URL.revokeObjectURL(url);
    
    toast({
      title: "Export successful",
      description: "Meeting analysis exported as JSON",
    });
  };

  const handleShare = () => {
    if (!results) return;
    
    const shareText = `Meeting Analysis Summary:\n\n${results.summary}\n\nAction Items:\n${results.action_items.map(item => `• ${item}`).join('\n')}`;
    
    if (navigator.share) {
      navigator.share({
        title: 'Meeting Analysis',
        text: shareText,
      });
    } else {
      navigator.clipboard.writeText(shareText);
      toast({
        title: "Copied to clipboard",
        description: "Meeting summary copied for sharing",
      });
    }
  };

  return (
    <div className="min-h-screen">
      <Header 
        processingTime={results?.processing_time} 
        isProcessing={isProcessing}
      />
      
      <main className="container mx-auto px-6 py-8">
        {!results ? (
          <div className="max-w-4xl mx-auto">
            {/* Hero Section */}
            <div className="text-center mb-12 animate-fade-in">
              <div 
                className="relative overflow-hidden rounded-3xl mb-8 h-64 flex items-center justify-center"
                style={{
                  backgroundImage: `url(${heroBackground})`,
                  backgroundSize: 'cover',
                  backgroundPosition: 'center'
                }}
              >
                <div className="absolute inset-0 bg-black/50 backdrop-blur-sm" />
                <div className="relative z-10 text-center">
                  <h1 className="text-5xl font-bold mb-4 bg-gradient-to-r from-white via-white to-white/80 bg-clip-text text-transparent">
                    Transform Your Meetings
                  </h1>
                  <p className="text-xl text-white/90 mb-2">
                    Upload your meeting recordings and get instant AI-powered analysis
                  </p>
                  <p className="text-sm text-white/70">
                    Transcription • Summary • Action Items • Key Decisions
                  </p>
                </div>
              </div>
            </div>
            
            <div className="max-w-2xl mx-auto">
              <FileUpload
                onFileAnalyzed={handleFileAnalyzed}
                isProcessing={isProcessing}
                setIsProcessing={setIsProcessing}
              />
            </div>
          </div>
        ) : (
          <div className="space-y-6">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-2xl font-bold mb-2">Analysis Complete</h2>
                <p className="text-muted-foreground">
                  Your meeting has been processed and analyzed
                </p>
              </div>
              <button
                onClick={handleNewUpload}
                className="px-6 py-2 glass-strong rounded-lg border border-primary/30 hover:bg-primary/10 transition-all duration-300 text-sm"
              >
                New Upload
              </button>
            </div>
            
            <ResultsSection results={results} />
          </div>
        )}
      </main>

      {/* Floating Action Button */}
      <FloatingActionButton
        onNewUpload={handleNewUpload}
        onExport={handleExport}
        onShare={handleShare}
        hasResults={!!results}
      />

      {/* Background decorative elements */}
      <div className="fixed inset-0 -z-10 overflow-hidden">
        <div className="absolute -top-40 -right-40 w-80 h-80 rounded-full bg-primary/10 blur-3xl animate-float" />
        <div className="absolute -bottom-40 -left-40 w-80 h-80 rounded-full bg-primary-glow/10 blur-3xl animate-float" style={{ animationDelay: '2s' }} />
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-96 h-96 rounded-full bg-primary/5 blur-3xl animate-float" style={{ animationDelay: '4s' }} />
      </div>
    </div>
  );
};

export default Index;