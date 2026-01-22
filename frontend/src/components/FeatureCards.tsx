import React, { useState } from 'react';
import { Video, Mic, FileText, ChevronDown } from 'lucide-react';
import { motion, AnimatePresence } from 'motion/react';

export function FeatureCards() {
  const [expandedCard, setExpandedCard] = useState<number | null>(null);

  const features = [
    {
      id: 1,
      title: 'Video Analysis',
      icon: Video,
      color: 'from-blue-500 to-blue-600',
      emoji: '🎥',
      description: 'Analyzes facial expressions, body language, and visual cues to detect emotions',
      details: [
        'Facial emotion recognition using deep CNNs',
        'Micro-expression detection',
        'Action unit analysis',
        'Temporal emotion tracking',
      ],
    },
    {
      id: 2,
      title: 'Audio Analysis',
      icon: Mic,
      color: 'from-purple-500 to-purple-600',
      emoji: '🎵',
      description: 'Extracts voice tone, pitch, and acoustic features to identify emotional states',
      details: [
        'Prosodic feature extraction',
        'Voice quality analysis',
        'Emotion detection from speech patterns',
        'Background noise filtering',
      ],
    },
    {
      id: 3,
      title: 'Text Analysis',
      icon: FileText,
      color: 'from-pink-500 to-pink-600',
      emoji: '📝',
      description: 'Uses NLP and transformers to understand sentiment from spoken words',
      details: [
        'BERT-based sentiment classification',
        'Contextual emotion understanding',
        'Multi-language support',
        'Sarcasm and irony detection',
      ],
    },
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6 px-4">
      {features.map((feature, index) => {
        const Icon = feature.icon;
        const isExpanded = expandedCard === feature.id;

        return (
          <motion.div
            key={feature.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
            whileHover={{ y: -8 }}
            className="relative"
          >
            <div
              onClick={() => setExpandedCard(isExpanded ? null : feature.id)}
              className="bg-white/5 backdrop-blur-sm border border-white/10 rounded-2xl shadow-lg hover:shadow-2xl transition-shadow cursor-pointer overflow-hidden"
            >
              {/* Header */}
              <div className={`bg-gradient-to-r ${feature.color} p-4 sm:p-6 text-white`}>
                <motion.div
                  animate={{
                    scale: isExpanded ? 1.1 : 1,
                    rotate: isExpanded ? 360 : 0,
                  }}
                  transition={{ type: 'spring', stiffness: 200, damping: 15 }}
                  className="w-14 h-14 sm:w-16 sm:h-16 bg-white/20 rounded-xl flex items-center justify-center mb-3 sm:mb-4 backdrop-blur-sm shadow-lg"
                >
                  <span className="text-3xl sm:text-4xl">{feature.emoji}</span>
                </motion.div>
                
                <h3 className="text-xl sm:text-2xl font-bold mb-2">{feature.title}</h3>
                <p className="text-white/90 text-xs sm:text-sm">{feature.description}</p>
              </div>

              {/* Content */}
              <div className="p-4 sm:p-6">
                <div className="flex items-center justify-between mb-4">
                  <div className="flex items-center gap-2">
                    <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
                    <span className="text-sm text-gray-400">Ready</span>
                  </div>
                  
                  <motion.div
                    animate={{ rotate: isExpanded ? 180 : 0 }}
                    transition={{ duration: 0.3 }}
                  >
                    <ChevronDown className="w-5 h-5 text-gray-400" />
                  </motion.div>
                </div>

                <AnimatePresence>
                  {isExpanded && (
                    <motion.div
                      initial={{ opacity: 0, height: 0 }}
                      animate={{ opacity: 1, height: 'auto' }}
                      exit={{ opacity: 0, height: 0 }}
                      transition={{ duration: 0.3 }}
                      className="space-y-2 border-t border-white/10 pt-4"
                    >
                      <h4 className="font-semibold text-gray-300 mb-3">Technical Details:</h4>
                      {feature.details.map((detail, idx) => (
                        <motion.div
                          key={idx}
                          initial={{ opacity: 0, x: -10 }}
                          animate={{ opacity: 1, x: 0 }}
                          transition={{ delay: idx * 0.1 }}
                          className="flex items-start gap-2"
                        >
                          <div className="w-1.5 h-1.5 bg-blue-500 rounded-full mt-2" />
                          <p className="text-sm text-gray-400">{detail}</p>
                        </motion.div>
                      ))}
                    </motion.div>
                  )}
                </AnimatePresence>
              </div>
            </div>
          </motion.div>
        );
      })}
    </div>
  );
}