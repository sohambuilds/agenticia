import React from 'react';
import { Brain, Sparkles } from 'lucide-react';

interface EnhancedLoadingSpinnerProps {
  message?: string;
}

const EnhancedLoadingSpinner: React.FC<EnhancedLoadingSpinnerProps> = ({ 
  message = "AI is thinking..." 
}) => {
  return (
    <div className="flex justify-start mb-4">
      <div className="max-w-[70%] bg-gradient-to-br from-gray-50 to-gray-100 border-2 border-gray-300 rounded-2xl p-4 shadow-sm">
        <div className="flex items-center space-x-3">
          {/* Animated brain icon */}
          <div className="relative">
            <Brain className="w-5 h-5 text-blue-600 animate-pulse" />
            <Sparkles className="w-3 h-3 text-purple-500 absolute -top-1 -right-1 animate-ping" />
          </div>
          
          {/* Typing animation */}
          <div className="flex items-center space-x-1">
            <div className="flex space-x-1">
              <div className="w-2 h-2 bg-blue-600 rounded-full animate-bounce"></div>
              <div className="w-2 h-2 bg-purple-600 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
              <div className="w-2 h-2 bg-green-600 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
            </div>
            <span className="text-sm text-gray-600 ml-2 animate-pulse">{message}</span>
          </div>
        </div>
        
        {/* Progress bar */}
        <div className="mt-3 w-full bg-gray-200 rounded-full h-1 overflow-hidden">
          <div className="h-full bg-gradient-to-r from-blue-500 to-purple-500 rounded-full animate-pulse" style={{
            width: '60%',
            animation: 'loading-bar 2s ease-in-out infinite'
          }}></div>
        </div>
      </div>
    </div>
  );
};

export default EnhancedLoadingSpinner; 