'use client';

import React from 'react';
import { MessageCircle, Sparkles, Moon, Sun } from 'lucide-react';
import StatusIndicator from './StatusIndicator';

interface EnhancedHeaderProps {
  onClearChat: () => void;
  isDarkMode: boolean;
  onToggleDarkMode: () => void;
}

const EnhancedHeader: React.FC<EnhancedHeaderProps> = ({ onClearChat, isDarkMode, onToggleDarkMode }) => {
  return (
    <div className={`border-b shadow-sm transition-colors duration-200 ${
      isDarkMode 
        ? 'bg-gradient-to-r from-gray-900 to-gray-800 border-gray-700' 
        : 'bg-gradient-to-r from-blue-50 to-purple-50 border-gray-200'
    }`}>
      <div className="p-3">
        <div className="flex justify-between items-center">
          {/* Left side - Logo and capabilities */}
          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-2">
              <div className="p-1.5 bg-gradient-to-br from-blue-600 to-purple-600 rounded-lg shadow-md">
                <Sparkles className="w-4 h-4 text-white" />
              </div>
              <div>
                <h1 className="text-lg font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                  AI Tutor Assistant
                </h1>
              </div>
            </div>
            
            {/* Capabilities indicators */}
            <div className="hidden sm:flex items-center space-x-3">
              <div className="flex items-center space-x-1">
                <div className="w-1.5 h-1.5 bg-blue-500 rounded-full"></div>
                <span className={`text-xs font-medium ${isDarkMode ? 'text-gray-300' : 'text-gray-700'}`}>Math</span>
              </div>
              <div className="flex items-center space-x-1">
                <div className="w-1.5 h-1.5 bg-green-500 rounded-full"></div>
                <span className={`text-xs font-medium ${isDarkMode ? 'text-gray-300' : 'text-gray-700'}`}>Physics</span>
              </div>
              <div className="flex items-center space-x-1">
                <div className="w-1.5 h-1.5 bg-purple-500 rounded-full"></div>
                <span className={`text-xs font-medium ${isDarkMode ? 'text-gray-300' : 'text-gray-700'}`}>General</span>
              </div>
            </div>
          </div>

          {/* Right side - Status and controls */}
          <div className="flex items-center space-x-3">
            <StatusIndicator />
            
            {/* Dark mode toggle */}
            <button
              onClick={onToggleDarkMode}
              className={`p-2 rounded-lg transition-all duration-200 ${
                isDarkMode 
                  ? 'bg-gray-700 hover:bg-gray-600 text-yellow-400' 
                  : 'bg-white hover:bg-gray-50 text-gray-600 border border-gray-300'
              }`}
              title={isDarkMode ? 'Switch to light mode' : 'Switch to dark mode'}
            >
              {isDarkMode ? <Sun size={16} /> : <Moon size={16} />}
            </button>

            {/* New chat button */}
            <button
              onClick={onClearChat}
              className={`flex items-center space-x-2 px-3 py-2 rounded-lg transition-all duration-200 shadow-sm hover:shadow ${
                isDarkMode 
                  ? 'bg-gray-700 hover:bg-gray-600 text-gray-200 border border-gray-600' 
                  : 'bg-white hover:bg-gray-50 text-gray-700 border border-gray-300'
              }`}
            >
              <MessageCircle size={14} />
              <span className="text-sm font-medium hidden sm:inline">New Chat</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default EnhancedHeader; 