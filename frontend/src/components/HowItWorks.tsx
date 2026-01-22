import React from 'react';
import { motion } from 'motion/react';
import { Upload, Brain, BarChart3, CheckCircle } from 'lucide-react';

export function HowItWorks() {
  const steps = [
    {
      icon: Upload,
      title: 'Upload Input',
      description: 'Upload video, audio, or enter text for analysis',
      color: 'from-blue-500 to-blue-600',
    },
    {
      icon: Brain,
      title: 'AI Processing',
      description: 'Advanced deep learning models extract features from all modalities',
      color: 'from-purple-500 to-purple-600',
    },
    {
      icon: BarChart3,
      title: 'Multimodal Fusion',
      description: 'Combines insights from video, audio, and text for comprehensive analysis',
      color: 'from-pink-500 to-pink-600',
    },
    {
      icon: CheckCircle,
      title: 'Get Results',
      description: 'Receive detailed sentiment analysis with confidence scores',
      color: 'from-green-500 to-green-600',
    },
  ];

  return (
    <div className="space-y-6 sm:space-y-8">
      <div className="text-center px-4">
        <h2 className="text-2xl sm:text-3xl font-bold mb-2 sm:mb-3">How It Works</h2>
        <p className="text-sm sm:text-base text-gray-400 max-w-2xl mx-auto">
          Our advanced AI pipeline processes your input through multiple stages to deliver accurate sentiment analysis
        </p>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-6 px-4">
        {steps.map((step, index) => {
          const Icon = step.icon;
          return (
            <motion.div
              key={step.title}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.15 }}
              className="relative"
            >
              <div className="bg-white/5 backdrop-blur-sm border border-white/10 rounded-2xl p-4 sm:p-6 text-center h-full">
                <div className={`w-14 h-14 sm:w-16 sm:h-16 mx-auto mb-3 sm:mb-4 bg-gradient-to-br ${step.color} rounded-xl flex items-center justify-center shadow-lg`}>
                  <Icon className="w-7 h-7 sm:w-8 sm:h-8 text-white" />
                </div>
                
                <div className="mb-2">
                  <span className="text-xs font-semibold text-gray-500 uppercase tracking-wider">
                    Step {index + 1}
                  </span>
                </div>
                
                <h3 className="text-lg sm:text-xl font-bold mb-2">{step.title}</h3>
                <p className="text-xs sm:text-sm text-gray-400">{step.description}</p>
              </div>

              {/* Connector Arrow */}
              {index < steps.length - 1 && (
                <div className="hidden lg:block absolute top-1/2 -right-3 transform -translate-y-1/2 z-10">
                  <motion.div
                    animate={{ x: [0, 5, 0] }}
                    transition={{ duration: 1.5, repeat: Infinity }}
                    className="text-gray-600"
                  >
                    →
                  </motion.div>
                </div>
              )}
            </motion.div>
          );
        })}
      </div>
    </div>
  );
}