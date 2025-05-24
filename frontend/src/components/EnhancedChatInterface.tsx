'use client';

import React, { useState, useRef, useEffect } from 'react';
import { chatAPI, ChatResponse } from '@/lib/api';
import EnhancedMessageBubble from './EnhancedMessageBubble';
import EnhancedLoadingSpinner from './EnhancedLoadingSpinner';
import EnhancedHeader from './EnhancedHeader';
import EnhancedFooter from './EnhancedFooter';
import EnhancedInput from './EnhancedInput';
import WelcomeScreen from './WelcomeScreen';

interface Message {
  id: string;
  content: string;
  isUser: boolean;
  timestamp: Date;
  agentUsed?: ChatResponse['agent_used'];
  metadata?: ChatResponse['metadata'];
}

const EnhancedChatInterface: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [conversationId, setConversationId] = useState<string | undefined>();
  const [error, setError] = useState<string | null>(null);
  const [isDarkMode, setIsDarkMode] = useState(true);
  
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
    // Load dark mode preference from localStorage, default to dark mode
    const savedDarkMode = localStorage.getItem('darkMode');
    if (savedDarkMode !== null) {
      setIsDarkMode(JSON.parse(savedDarkMode));
    } else {
      // Default to dark mode and save it
      setIsDarkMode(true);
      localStorage.setItem('darkMode', JSON.stringify(true));
    }
  }, []);

  const toggleDarkMode = () => {
    const newDarkMode = !isDarkMode;
    setIsDarkMode(newDarkMode);
    localStorage.setItem('darkMode', JSON.stringify(newDarkMode));
  };

  const handleSendMessage = async (messageContent?: string) => {
    const content = messageContent || inputValue;
    if (!content.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      content: content,
      isUser: true,
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);
    setError(null);

    try {
      const response = await chatAPI.sendMessage(content, conversationId);
      
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

  const handleExampleClick = (example: string) => {
    setInputValue(example);
    setTimeout(() => {
      handleSendMessage(example);
    }, 100);
  };

  return (
    <div className={`flex flex-col h-screen transition-colors duration-200 ${
      isDarkMode 
        ? 'bg-gradient-to-br from-gray-900 to-gray-800' 
        : 'bg-gradient-to-br from-gray-50 to-gray-100'
    }`}>
      <EnhancedHeader 
        onClearChat={handleClearChat} 
        isDarkMode={isDarkMode} 
        onToggleDarkMode={toggleDarkMode} 
      />

      <div className="flex-1 overflow-y-auto p-6 space-y-4">
        {messages.length === 0 ? (
          <WelcomeScreen onExampleClick={handleExampleClick} isDarkMode={isDarkMode} />
        ) : (
          <>
            {messages.map((message) => (
              <EnhancedMessageBubble
                key={message.id}
                message={message.content}
                isUser={message.isUser}
                agentUsed={message.agentUsed}
                metadata={message.metadata}
                timestamp={message.timestamp}
                isDarkMode={isDarkMode}
              />
            ))}
          </>
        )}

        {isLoading && <EnhancedLoadingSpinner />}
        <div ref={messagesEndRef} />
      </div>

      <div className={`p-6 border-t transition-colors duration-200 ${
        isDarkMode 
          ? 'bg-gray-800 border-gray-700' 
          : 'bg-white border-gray-200'
      }`}>
        {error && (
          <div className={`mb-4 p-4 border rounded-xl text-sm animate-fade-in ${
            isDarkMode 
              ? 'bg-red-900/50 border-red-700 text-red-400' 
              : 'bg-red-50 border-red-200 text-red-700'
          }`}>
            <div className="flex items-center space-x-2">
              <div className="w-2 h-2 bg-red-500 rounded-full"></div>
              <span className="font-medium">Error:</span>
              <span>{error}</span>
            </div>
          </div>
        )}
        
        <EnhancedInput
          ref={inputRef}
          value={inputValue}
          onChange={setInputValue}
          onSend={() => handleSendMessage()}
          onKeyPress={handleKeyPress}
          isLoading={isLoading}
          isDarkMode={isDarkMode}
        />
      </div>

      <EnhancedFooter isDarkMode={isDarkMode} />
    </div>
  );
};

export default EnhancedChatInterface; 