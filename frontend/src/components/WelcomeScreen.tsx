import React from 'react';
import { Calculator, Zap, GraduationCap, Sparkles, ArrowRight, Book, Target } from 'lucide-react';

interface WelcomeScreenProps {  onExampleClick: (example: string) => void;  isDarkMode: boolean;}

const WelcomeScreen: React.FC<WelcomeScreenProps> = ({ onExampleClick, isDarkMode }) => {  const examples = [    {      category: 'Math',      icon: <Calculator className="w-5 h-5 text-blue-600" />,      color: isDarkMode         ? 'border-blue-600 bg-blue-900/30 hover:bg-blue-800/40'         : 'border-blue-200 bg-blue-50 hover:bg-blue-100',      examples: [        "What is 15 + 27 * 3?",        "Calculate sin(45 degrees)",        "Solve for x: 2x + 5 = 15"      ]    },    {      category: 'Physics',      icon: <Zap className="w-5 h-5 text-green-600" />,      color: isDarkMode         ? 'border-green-600 bg-green-900/30 hover:bg-green-800/40'         : 'border-green-200 bg-green-50 hover:bg-green-100',      examples: [        "What is the speed of light?",        "Calculate kinetic energy with mass=5kg, velocity=10m/s",        "Explain Newton's second law"      ]    },    {      category: 'General',      icon: <GraduationCap className="w-5 h-5 text-purple-600" />,      color: isDarkMode         ? 'border-purple-600 bg-purple-900/30 hover:bg-purple-800/40'         : 'border-purple-200 bg-purple-50 hover:bg-purple-100',      examples: [        "Explain photosynthesis",        "What is machine learning?",        "How does DNA replication work?"      ]    }  ];

  const features = [
    { icon: <Target className="w-4 h-4" />, text: "Intelligent agent routing" },
    { icon: <Book className="w-4 h-4" />, text: "Step-by-step explanations" },
    { icon: <Sparkles className="w-4 h-4" />, text: "Real-time tool usage" },
  ];

  return (
    <div className="text-center py-8 px-4 max-w-4xl mx-auto">
      {/* Main heading */}
      <div className="mb-8">
        <div className="flex justify-center mb-4">
          <div className="p-4 bg-gradient-to-br from-blue-600 to-purple-600 rounded-2xl shadow-lg">
            <Sparkles className="w-8 h-8 text-white" />
          </div>
        </div>
        <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent mb-3">
          Welcome to AI Tutor!
        </h1>
                <p className={`text-lg max-w-2xl mx-auto leading-relaxed ${isDarkMode ? 'text-gray-300' : 'text-gray-600'}`}>          Your intelligent multi-agent assistant for math, physics, and general learning.           Powered by advanced AI with specialized tools and real-time problem solving.        </p>
      </div>

      {/* Features */}
            <div className="flex justify-center mb-8">        <div className={`flex items-center space-x-6 text-sm ${isDarkMode ? 'text-gray-400' : 'text-gray-600'}`}>          {features.map((feature, index) => (            <div key={index} className="flex items-center space-x-2">              {feature.icon}              <span>{feature.text}</span>            </div>          ))}        </div>      </div>

      {/* Example categories */}
      <div className="grid md:grid-cols-3 gap-6 mb-8">
        {examples.map((category, categoryIndex) => (
          <div key={categoryIndex} className={`p-6 rounded-2xl border-2 transition-all duration-200 ${category.color}`}>
            <div className="flex items-center justify-center space-x-2 mb-4">
              {category.icon}
              <h3 className="font-semibold text-lg">{category.category}</h3>
            </div>
            
            <div className="space-y-3">
              {category.examples.map((example, exampleIndex) => (
                                <button                  key={exampleIndex}                  onClick={() => onExampleClick(example)}                  className={`w-full text-left p-3 rounded-lg border transition-all duration-200 group ${                    isDarkMode                       ? 'bg-gray-800 border-gray-600 hover:border-gray-500 hover:bg-gray-700'                       : 'bg-white border-gray-200 hover:border-gray-300 hover:shadow-sm'                  }`}                >                  <div className="flex items-center justify-between">                    <span className={`text-sm ${                      isDarkMode                         ? 'text-gray-300 group-hover:text-gray-100'                         : 'text-gray-700 group-hover:text-gray-900'                    }`}>                      "{example}"                    </span>                    <ArrowRight className={`w-4 h-4 group-hover:translate-x-1 transition-all duration-200 ${                      isDarkMode                         ? 'text-gray-500 group-hover:text-gray-300'                         : 'text-gray-400 group-hover:text-gray-600'                    }`} />                  </div>                </button>
              ))}
            </div>
          </div>
        ))}
      </div>

      {/* Call to action */}
      <div className="text-center">
        <p className="text-gray-500 text-sm mb-4">
          Or type your own question in the input field below
        </p>
        <div className="inline-flex items-center space-x-2 px-4 py-2 bg-gradient-to-r from-blue-50 to-purple-50 rounded-full border border-gray-200">
          <Sparkles className="w-4 h-4 text-purple-500" />
          <span className="text-xs text-gray-600 font-medium">
            Try asking about math problems, physics concepts, or any topic you'd like help with!
          </span>
        </div>
      </div>
    </div>
  );
};

export default WelcomeScreen; 