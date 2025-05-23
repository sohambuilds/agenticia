import React from 'react';
import { ChatResponse } from '@/lib/api';

interface MessageBubbleProps {
  message: string;
  isUser: boolean;
  agentUsed?: ChatResponse['agent_used'];
  metadata?: ChatResponse['metadata'];
  timestamp?: Date;
}

const getAgentColor = (agent?: ChatResponse['agent_used']) => {
  switch (agent) {
    case 'math':
      return 'bg-blue-100 border-blue-200';
    case 'physics':
      return 'bg-green-100 border-green-200';
    case 'tutor':
      return 'bg-purple-100 border-purple-200';
    default:
      return 'bg-gray-100 border-gray-200';
  }
};

const getAgentIcon = (agent?: ChatResponse['agent_used']) => {
  switch (agent) {
    case 'math':
      return '🧮';
    case 'physics':
      return '⚡';
    case 'tutor':
      return '🎓';
    default:
      return '🤖';
  }
};

const MessageBubble: React.FC<MessageBubbleProps> = ({
  message,
  isUser,
  agentUsed,
  metadata,
  timestamp,
}) => {
  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-4`}>
      <div
        className={`max-w-[70%] rounded-lg p-3 ${
          isUser
            ? 'bg-blue-600 text-white'
            : `border-2 ${getAgentColor(agentUsed)} text-gray-800`
        }`}
      >
        {/* Agent indicator for AI messages */}
        {!isUser && agentUsed && (
          <div className="flex items-center mb-2 text-xs text-gray-600">
            <span className="mr-1">{getAgentIcon(agentUsed)}</span>
            <span className="font-medium capitalize">{agentUsed} Agent</span>
            {metadata?.confidence && (
              <span className="ml-2 text-gray-500">
                ({Math.round(metadata.confidence * 100)}% confident)
              </span>
            )}
          </div>
        )}

        {/* Message content */}
        <div className="whitespace-pre-wrap">{message}</div>

        {/* Tools used indicator */}
        {!isUser && metadata?.tools_used && metadata.tools_used.length > 0 && (
          <div className="mt-2 pt-2 border-t border-gray-300">
            <div className="text-xs text-gray-600">
              <span className="font-medium">Tools used:</span>{' '}
              {metadata.tools_used.join(', ')}
            </div>
          </div>
        )}

        {/* Error indicator */}
        {!isUser && metadata?.error && (
          <div className="mt-2 pt-2 border-t border-red-300">
            <div className="text-xs text-red-600">
              <span className="font-medium">Error:</span> {metadata.error}
            </div>
          </div>
        )}

        {/* Timestamp */}
        {timestamp && (
          <div className={`text-xs mt-2 ${isUser ? 'text-blue-200' : 'text-gray-500'}`}>
            {timestamp.toLocaleTimeString()}
          </div>
        )}
      </div>
    </div>
  );
};

export default MessageBubble; 