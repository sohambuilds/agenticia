'use client';

import React, { useState, useRef, useEffect } from 'react';
import { chatAPI, ChatResponse } from '@/lib/api';
import MessageBubble from './MessageBubble';
import LoadingSpinner from './LoadingSpinner';
import StatusIndicator from './StatusIndicator';

interface Message {
  id: string;
  content: string;
  isUser: boolean;
  timestamp: Date;
  agentUsed?: ChatResponse['agent_used'];
  metadata?: ChatResponse['metadata'];
}

const ChatInterface: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [conversationId, setConversationId] = useState<string | undefined>();
  const [error, setError] = useState<string | null>(null);
  
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    inputRef.current?.focus();
  }, []);

  const handleSendMessage = async () => {
    if (!inputValue.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      content: inputValue,
      isUser: true,
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);
    setError(null);

    try {
      const response = await chatAPI.sendMessage(inputValue, conversationId);
      
      if (!conversationId) {
        setConversationId(response.conversation_id);
      }

      const aiMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: response.response,
        isUser: false,
        timestamp: new Date(),
        agentUsed: response.agent_used,
        metadata: response.metadata,
      };

      setMessages(prev => [...prev, aiMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      setError('Failed to send message. Please try again.');
      
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: 'Sorry, I encountered an error. Please try again.',
        isUser: false,
        timestamp: new Date(),
        metadata: { error: 'Connection failed' },
      };
      
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const handleClearChat = () => {
    setMessages([]);
    setConversationId(undefined);
    setError(null);
    inputRef.current?.focus();
  };

  return (
    <div className="flex flex-col h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-200 p-4 shadow-sm">
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-xl font-bold text-gray-800">AI Tutor Assistant</h1>
            <div className="flex items-center space-x-4">
              <p className="text-sm text-gray-600">Math • Physics • General Tutoring</p>
              <StatusIndicator />
            </div>
          </div>
          <button
            onClick={handleClearChat}
            className="px-3 py-1 text-sm bg-gray-100 hover:bg-gray-200 rounded-md transition-colors"
          >
            Clear Chat
          </button>
        </div>
      </div>

      {/* Chat Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.length === 0 && (
          <div className="text-center text-gray-500 mt-8">
            <div className="text-4xl mb-4">🎓</div>
            <h2 className="text-lg font-medium mb-2">Welcome to AI Tutor!</h2>
            <p className="text-sm">
              Ask me anything about math, physics, or any topic you&apos;d like help with.
            </p>
            <div className="mt-4 text-xs text-gray-400">
              <p>Try: &quot;What is 2 + 3 * 4?&quot; or &quot;What is the speed of light?&quot;</p>
            </div>
          </div>
        )}

        {messages.map((message) => (
          <MessageBubble
            key={message.id}
            message={message.content}
            isUser={message.isUser}
            agentUsed={message.agentUsed}
            metadata={message.metadata}
            timestamp={message.timestamp}
          />
        ))}

        {isLoading && <LoadingSpinner />}
        
        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="bg-white border-t border-gray-200 p-4">
        {error && (
          <div className="mb-3 p-2 bg-red-100 border border-red-300 text-red-700 rounded-md text-sm">
            {error}
          </div>
        )}
        
        <div className="flex space-x-2">
          <input
            ref={inputRef}
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Ask me anything..."
            disabled={isLoading}
            className="flex-1 p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent disabled:opacity-50"
          />
          <button
            onClick={handleSendMessage}
            disabled={!inputValue.trim() || isLoading}
            className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            Send
          </button>
        </div>
        
        <div className="mt-2 text-xs text-gray-500 text-center">
          Press Enter to send • Shift+Enter for new line
        </div>
      </div>
    </div>
  );
};

export default ChatInterface; 