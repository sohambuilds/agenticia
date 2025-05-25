'use client';

import React, { useState, useEffect } from 'react';
import { chatAPI } from '@/lib/api';

const StatusIndicator: React.FC = () => {
  const [status, setStatus] = useState<'checking' | 'online' | 'offline'>('checking');
  const [errorDetails, setErrorDetails] = useState<string>('');

  useEffect(() => {
    const checkStatus = async () => {
      try {
        console.log('API Base URL:', process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000');
        await chatAPI.checkHealth();
        setStatus('online');
        setErrorDetails('');
      } catch (error: any) {
        console.error('Backend health check failed:', error);
        console.error('Error details:', {
          message: error.message,
          code: error.code,
          response: error.response?.data,
          status: error.response?.status
        });
        setStatus('offline');
        setErrorDetails(error.message || 'Connection failed');
      }
    };

    checkStatus();
    // Check status every 30 seconds
    const interval = setInterval(checkStatus, 30000);

    return () => clearInterval(interval);
  }, []);

  const getStatusColor = () => {
    switch (status) {
      case 'online':
        return 'bg-green-500';
      case 'offline':
        return 'bg-red-500';
      default:
        return 'bg-yellow-500';
    }
  };

  const getStatusText = () => {
    switch (status) {
      case 'online':
        return 'Online';
      case 'offline':
        return 'Offline';
      default:
        return 'Checking...';
    }
  };

  return (
    <div className="flex items-center space-x-2 text-xs">
      <div className={`w-2 h-2 rounded-full ${getStatusColor()}`}></div>
      <span className="text-gray-600">{getStatusText()}</span>
      {status === 'offline' && errorDetails && (
        <span className="text-red-500 text-xs ml-1" title={errorDetails}>
          ⚠️
        </span>
      )}
    </div>
  );
};

export default StatusIndicator; 