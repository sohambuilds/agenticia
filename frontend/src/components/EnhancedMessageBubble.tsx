import React from 'react';
import { ChatResponse } from '@/lib/api';
import { Bot, User, Calculator, Zap, GraduationCap, Clock, Wrench, CheckCircle, AlertCircle } from 'lucide-react';

interface EnhancedMessageBubbleProps {
  message: string;
  isUser: boolean;
  agentUsed?: ChatResponse['agent_used'];
  metadata?: ChatResponse['metadata'];
  timestamp?: Date;
  isDarkMode: boolean;
}

const getAgentColor = (isDarkMode: boolean, agent?: ChatResponse['agent_used']) => {
  if (isDarkMode) {
    switch (agent) {
      case 'math':
        return 'bg-gradient-to-br from-blue-900/50 to-blue-800/50 border-blue-600';
      case 'physics':
        return 'bg-gradient-to-br from-green-900/50 to-green-800/50 border-green-600';
      case 'tutor':
        return 'bg-gradient-to-br from-purple-900/50 to-purple-800/50 border-purple-600';
      default:
        return 'bg-gradient-to-br from-gray-800/50 to-gray-700/50 border-gray-600';
    }
  } else {
    switch (agent) {
      case 'math':
        return 'bg-gradient-to-br from-blue-50 to-blue-100 border-blue-300';
      case 'physics':
        return 'bg-gradient-to-br from-green-50 to-green-100 border-green-300';
      case 'tutor':
        return 'bg-gradient-to-br from-purple-50 to-purple-100 border-purple-300';
      default:
        return 'bg-gradient-to-br from-gray-50 to-gray-100 border-gray-300';
    }
  }
};

const getAgentIcon = (agent?: ChatResponse['agent_used']) => {
  switch (agent) {
    case 'math':
      return <Calculator size={16} className="text-blue-600" />;
    case 'physics':
      return <Zap size={16} className="text-green-600" />;
    case 'tutor':
      return <GraduationCap size={16} className="text-purple-600" />;
    default:
      return <Bot size={16} className="text-gray-600" />;
  }
};

const getConfidenceColor = (confidence?: number) => {
  if (!confidence) return 'text-gray-500';
  if (confidence >= 0.8) return 'text-green-600';
  if (confidence >= 0.6) return 'text-yellow-600';
  return 'text-red-600';
};

const EnhancedMessageBubble: React.FC<EnhancedMessageBubbleProps> = ({
  message,
  isUser,
  agentUsed,
  metadata,
  timestamp,
  isDarkMode,
}) => {
  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-4 animate-fade-in`}>
      <div
        className={`max-w-[70%] rounded-2xl shadow-sm hover:shadow-md transition-all duration-200 ${
          isUser
            ? 'bg-gradient-to-br from-blue-600 to-blue-700 text-white p-4'
            : `border-2 ${getAgentColor(isDarkMode, agentUsed)} ${isDarkMode ? 'text-gray-100' : 'text-gray-800'} p-4`
        }`}
      >
        {/* User icon for user messages */}
        {isUser && (
          <div className="flex items-center justify-end mb-2">
            <div className="flex items-center space-x-2">
              <span className="text-xs text-blue-100">You</span>
              <User size={16} className="text-blue-100" />
            </div>
          </div>
        )}

        {/* Agent indicator for AI messages */}
        {!isUser && agentUsed && (
          <div className="flex items-center justify-between mb-3">
            <div className="flex items-center space-x-2">
              {getAgentIcon(agentUsed)}
              <span className="font-medium text-sm capitalize">{agentUsed} Agent</span>
            </div>
            {metadata?.confidence && (
              <div className={`flex items-center space-x-1 text-xs ${getConfidenceColor(metadata.confidence)}`}>
                <CheckCircle size={12} />
                <span>{Math.round(metadata.confidence * 100)}%</span>
              </div>
            )}
          </div>
        )}

        {/* Message content */}
        <div className="whitespace-pre-wrap leading-relaxed">{message}</div>

        {/* Tools used indicator */}
        {!isUser && metadata?.tools_used && metadata.tools_used.length > 0 && (
          <div className={`mt-3 pt-3 border-t ${isDarkMode ? 'border-gray-600' : 'border-gray-200'}`}>
            <div className={`flex items-center space-x-2 text-xs ${isDarkMode ? 'text-gray-400' : 'text-gray-600'}`}>
              <Wrench size={12} />
              <span className="font-medium">Tools:</span>
              <div className="flex flex-wrap gap-1">
                {metadata.tools_used.map((tool, index) => (
                  <span
                    key={index}
                    className={`px-2 py-1 rounded-full text-xs font-medium ${
                      isDarkMode ? 'bg-gray-700 text-gray-300' : 'bg-gray-100 text-gray-700'
                    }`}
                  >
                    {tool}
                  </span>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* Error indicator */}
        {!isUser && metadata?.error && (
          <div className={`mt-3 pt-3 border-t ${isDarkMode ? 'border-red-400' : 'border-red-200'}`}>
            <div className={`flex items-center space-x-2 text-xs ${isDarkMode ? 'text-red-400' : 'text-red-600'}`}>
              <AlertCircle size={12} />
              <span className="font-medium">Error:</span>
              <span>{metadata.error}</span>
            </div>
          </div>
        )}

        {/* Timestamp */}
        {timestamp && (
          <div className={`flex items-center space-x-1 text-xs mt-3 ${
            isUser ? 'text-blue-200 justify-end' : isDarkMode ? 'text-gray-500' : 'text-gray-500'
          }`}>
            <Clock size={10} />
            <span>{timestamp.toLocaleTimeString()}</span>
          </div>
        )}
      </div>
    </div>
  );
};

export default EnhancedMessageBubble; 