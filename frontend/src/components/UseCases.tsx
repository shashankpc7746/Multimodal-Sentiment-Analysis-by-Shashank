import React from 'react';
import { motion } from 'motion/react';
import { GraduationCap, Briefcase, Heart, Video } from 'lucide-react';

export function UseCases() {
  const useCases = [
    {
      icon: GraduationCap,
      title: 'Research & Education',
      description: 'Study emotional patterns, conduct behavioral research, and teach sentiment analysis concepts',
      gradient: 'from-blue-500/20 to-blue-600/20',
      borderColor: 'border-blue-500/30',
    },
    {
      icon: Briefcase,
      title: 'Business Analytics',
      description: 'Analyze customer feedback, monitor brand sentiment, and improve user experience',
      gradient: 'from-purple-500/20 to-purple-600/20',
      borderColor: 'border-purple-500/30',
    },
    {
      icon: Heart,
      title: 'Mental Health',
      description: 'Track emotional well-being, monitor therapy progress, and detect mood changes',
      gradient: 'from-pink-500/20 to-pink-600/20',
      borderColor: 'border-pink-500/30',
    },
    {
      icon: Video,
      title: 'Content Creation',
      description: 'Optimize video content, gauge audience reactions, and improve engagement',
      gradient: 'from-green-500/20 to-green-600/20',
      borderColor: 'border-green-500/30',
    },
  ];

  return (
    <div className="space-y-6 sm:space-y-8">
      <div className="text-center px-4">
        <h2 className="text-2xl sm:text-3xl font-bold mb-2 sm:mb-3">Use Cases</h2>
        <p className="text-sm sm:text-base text-gray-400 max-w-2xl mx-auto">
          Discover how TriSenti AI can be applied across various industries and domains
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 sm:gap-6 px-4">
        {useCases.map((useCase, index) => {
          const Icon = useCase.icon;
          return (
            <motion.div
              key={useCase.title}
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: index * 0.1 }}
              whileHover={{ scale: 1.02, y: -5 }}
              className={`bg-gradient-to-br ${useCase.gradient} backdrop-blur-sm border ${useCase.borderColor} rounded-2xl p-4 sm:p-6`}
            >
              <div className="flex items-start gap-3 sm:gap-4">
                <div className="w-12 h-12 sm:w-14 sm:h-14 bg-white/10 rounded-xl flex items-center justify-center flex-shrink-0">
                  <Icon className="w-6 h-6 sm:w-7 sm:h-7 text-white" />
                </div>
                
                <div>
                  <h3 className="text-lg sm:text-xl font-bold mb-2">{useCase.title}</h3>
                  <p className="text-gray-300 text-xs sm:text-sm">{useCase.description}</p>
                </div>
              </div>
            </motion.div>
          );
        })}
      </div>
    </div>
  );
}