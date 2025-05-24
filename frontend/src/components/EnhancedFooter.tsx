'use client';

import React from 'react';
import { Github, Linkedin, Globe, Twitter } from 'lucide-react';

interface EnhancedFooterProps {
  isDarkMode: boolean;
}

const SocialLink = ({ href, icon: Icon, label, isDarkMode }: { 
  href: string; 
  icon: React.ComponentType<{ size?: number; className?: string }>; 
  label: string; 
  isDarkMode: boolean;
}) => (
  <a
    href={href}
    target="_blank"
    rel="noopener noreferrer"
    className={`p-2 rounded-lg transition-all duration-200 group ${
      isDarkMode 
        ? 'text-gray-400 hover:text-blue-400 hover:bg-gray-700' 
        : 'text-gray-600 hover:text-blue-600 hover:bg-blue-50'
    }`}
    title={label}
  >
    <Icon size={16} className="group-hover:scale-110 transition-transform duration-200" />
  </a>
);

const EnhancedFooter: React.FC<EnhancedFooterProps> = ({ isDarkMode }) => {
  return (
    <div className={`border-t p-3 transition-colors duration-200 ${
      isDarkMode 
        ? 'bg-gradient-to-r from-gray-900 to-gray-800 border-gray-700' 
        : 'bg-gradient-to-r from-gray-50 to-gray-100 border-gray-200'
    }`}>
      <div className="flex flex-col items-center space-y-2">
        {/* Social links */}
        <div className="flex items-center space-x-2">
          <span className={`text-sm mr-2 ${isDarkMode ? 'text-gray-400' : 'text-gray-500'}`}>
            Connect with Soham:
          </span>
          <div className="flex items-center space-x-1">
            <SocialLink 
              href="https://sohambuilds.github.io" 
              icon={Globe} 
              label="Portfolio Website" 
              isDarkMode={isDarkMode}
            />
            <SocialLink 
              href="https://github.com/sohambuilds" 
              icon={Github} 
              label="GitHub" 
              isDarkMode={isDarkMode}
            />
            <SocialLink 
              href="https://linkedin.com/in/sohamr" 
              icon={Linkedin} 
              label="LinkedIn" 
              isDarkMode={isDarkMode}
            />
            <SocialLink 
              href="https://x.com/neuralxtract" 
              icon={Twitter} 
              label="Twitter/X" 
              isDarkMode={isDarkMode}
            />
          </div>
        </div>

        {/* Copyright */}
        <div className={`text-xs ${isDarkMode ? 'text-gray-600' : 'text-gray-400'}`}>
          © 2024 Soham. Open source project for educational purposes.
        </div>
      </div>
    </div>
  );
};

export default EnhancedFooter; 