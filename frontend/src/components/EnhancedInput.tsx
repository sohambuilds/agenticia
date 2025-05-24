import React, { forwardRef } from 'react';
import { Send, Mic, Paperclip } from 'lucide-react';

interface EnhancedInputProps {
  value: string;
  onChange: (value: string) => void;
  onSend: () => void;
  onKeyPress: (e: React.KeyboardEvent) => void;
  isLoading: boolean;
  placeholder?: string;
  isDarkMode: boolean;
}

const EnhancedInput = forwardRef<HTMLInputElement, EnhancedInputProps>(({
  value,
  onChange,
  onSend,
  onKeyPress,
  isLoading,
  placeholder = "Ask me anything...",
  isDarkMode
}, ref) => {
  return (
    <div className="relative">
      <div className={`flex items-center space-x-3 p-4 border-2 rounded-2xl shadow-lg hover:shadow-xl transition-all duration-200 ${
        isDarkMode 
          ? 'bg-gray-800 border-gray-600 focus-within:border-blue-500 focus-within:ring-4 focus-within:ring-blue-900/50' 
          : 'bg-white border-gray-200 focus-within:border-blue-400 focus-within:ring-4 focus-within:ring-blue-100'
      }`}>
        {/* Input field */}
        <div className="flex-1 relative">
          <input
            ref={ref}
            type="text"
            value={value}
            onChange={(e) => onChange(e.target.value)}
            onKeyPress={onKeyPress}
            placeholder={placeholder}
            disabled={isLoading}
            className={`w-full p-3 bg-transparent border-none outline-none resize-none ${
              isDarkMode 
                ? 'text-gray-100 placeholder-gray-400' 
                : 'text-gray-800 placeholder-gray-500'
            }`}
          />
        </div>

        {/* Action buttons */}
        <div className="flex items-center space-x-2">
          {/* Attachment button (future feature) */}
          <button
            type="button"
            className={`p-2 rounded-lg transition-all duration-200 ${
              isDarkMode 
                ? 'text-gray-500 hover:text-gray-300 hover:bg-gray-700' 
                : 'text-gray-400 hover:text-gray-600 hover:bg-gray-100'
            }`}
            title="Attach file (coming soon)"
            disabled
          >
            <Paperclip size={18} />
          </button>
          
          {/* Voice input button (future feature) */}
          <button
            type="button"
            className={`p-2 rounded-lg transition-all duration-200 ${
              isDarkMode 
                ? 'text-gray-500 hover:text-gray-300 hover:bg-gray-700' 
                : 'text-gray-400 hover:text-gray-600 hover:bg-gray-100'
            }`}
            title="Voice input (coming soon)"
            disabled
          >
            <Mic size={18} />
          </button>

          {/* Send button */}
          <button
            onClick={onSend}
            disabled={!value.trim() || isLoading}
            className="p-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-xl hover:from-blue-700 hover:to-purple-700 focus:outline-none focus:ring-4 focus:ring-blue-200 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 shadow-md hover:shadow-lg group"
          >
            <Send size={18} className="group-hover:translate-x-0.5 transition-transform duration-200" />
          </button>
        </div>
      </div>

      {/* Keyboard hint */}
      <div className="flex justify-between items-center mt-2 px-2">
        <div className={`text-xs ${isDarkMode ? 'text-gray-400' : 'text-gray-500'}`}>
          Press <kbd className={`px-1 py-0.5 text-xs rounded border ${
            isDarkMode 
              ? 'bg-gray-700 border-gray-600 text-gray-300' 
              : 'bg-gray-100 border-gray-300 text-gray-700'
          }`}>Enter</kbd> to send • <kbd className={`px-1 py-0.5 text-xs rounded border ${
            isDarkMode 
              ? 'bg-gray-700 border-gray-600 text-gray-300' 
              : 'bg-gray-100 border-gray-300 text-gray-700'
          }`}>Shift+Enter</kbd> for new line
        </div>
        <div className={`text-xs ${isDarkMode ? 'text-gray-500' : 'text-gray-400'}`}>
          {value.length > 0 && `${value.length} characters`}
        </div>
      </div>
    </div>
  );
});

EnhancedInput.displayName = 'EnhancedInput';

export default EnhancedInput; 