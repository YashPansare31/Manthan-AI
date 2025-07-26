import { useState } from 'react';
import { Plus, Download, Share2, FileText, X } from 'lucide-react';
import { Button } from '@/components/ui/button';

interface FloatingActionButtonProps {
  onNewUpload: () => void;
  onExport?: () => void;
  onShare?: () => void;
  hasResults?: boolean;
}

export const FloatingActionButton = ({ 
  onNewUpload, 
  onExport, 
  onShare, 
  hasResults = false 
}: FloatingActionButtonProps) => {
  const [isOpen, setIsOpen] = useState(false);

  const toggleMenu = () => setIsOpen(!isOpen);

  const actions = [
    ...(hasResults ? [
      { icon: Download, label: 'Export', onClick: onExport },
      { icon: Share2, label: 'Share', onClick: onShare },
      { icon: FileText, label: 'New Upload', onClick: onNewUpload },
    ] : [
      { icon: FileText, label: 'Upload File', onClick: onNewUpload },
    ])
  ];

  return (
    <div className="fixed bottom-8 right-8 z-50">
      {/* Action Menu */}
      {isOpen && (
        <div className="absolute bottom-16 right-0 space-y-3 animate-slide-up">
          {actions.map((action, index) => (
            <div
              key={index}
              className="flex items-center space-x-3 animate-fade-in"
              style={{ animationDelay: `${index * 100}ms` }}
            >
              <span className="text-sm text-muted-foreground bg-black/60 backdrop-blur-sm px-3 py-1 rounded-lg">
                {action.label}
              </span>
              <Button
                size="icon"
                variant="glass"
                className="w-12 h-12 rounded-full shadow-glow hover:scale-110"
                onClick={() => {
                  action.onClick?.();
                  setIsOpen(false);
                }}
              >
                <action.icon className="w-5 h-5" />
              </Button>
            </div>
          ))}
        </div>
      )}

      {/* Main FAB */}
      <Button
        size="icon"
        variant="gradient"
        className="w-14 h-14 rounded-full shadow-glow hover:shadow-xl hover:scale-110 transition-all duration-300"
        onClick={toggleMenu}
      >
        {isOpen ? (
          <X className="w-6 h-6 transition-transform duration-300 rotate-90" />
        ) : (
          <Plus className="w-6 h-6 transition-transform duration-300" />
        )}
      </Button>
    </div>
  );
};