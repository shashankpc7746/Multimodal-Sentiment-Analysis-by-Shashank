import React, { useState } from 'react';
import { MultimodalInput } from './components/MultimodalInput';
import { ProgressStepper } from './components/ProgressStepper';
import { FeatureCards } from './components/FeatureCards';
import { SentimentResult } from './components/SentimentResult';
import { HistoryList } from './components/HistoryList';
import trisentiLogo from './assets/TriSenti logo.png';
import { AnimatedBackground } from './components/AnimatedBackground';
import { Footer } from './components/Footer';
import { HowItWorks } from './components/HowItWorks';
import { UseCases } from './components/UseCases';
import { ResultAfterTick } from './components/ResultAfterTick';
import logoImage from 'figma:asset/3f3e9a7ff4d19c90aab4fecc28a836cb0f8ea242.png';

export interface Analysis {
  id: string;
  filename: string;
  type: 'video' | 'audio' | 'text';
  timestamp: Date;
  status: 'processing' | 'completed' | 'failed';
  currentStep: number;
  sentiment?: {
    label: string;
    confidence: number;
    emotions: {
      video: { emotion: string; score: number };
      audio: { emotion: string; score: number };
      text: { emotion: string; score: number };
    };
    transcript?: string; // Add transcript for video/audio analysis
  };
}

export default function App() {
  const [currentAnalysis, setCurrentAnalysis] = useState<Analysis | null>(null);
  const [analysisHistory, setAnalysisHistory] = useState<Analysis[]>([]);

  const handleAnalyze = (data: { type: 'video' | 'audio' | 'text'; content: File | string }) => {
    const newAnalysis: Analysis = {
      id: Date.now().toString(),
      filename: data.type === 'text' 
        ? `Text Input (${(data.content as string).substring(0, 30)}...)` 
        : (data.content as File).name,
      type: data.type,
      timestamp: new Date(),
      status: 'processing',
      currentStep: 0,
    };
    
    setCurrentAnalysis(newAnalysis);
    
    // Scroll to the progress section
    setTimeout(() => {
      const progressSection = document.getElementById('analysis-progress');
      progressSection?.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }, 100);
    
    // Simulate processing steps
    simulateAnalysis(newAnalysis);
  };

  const simulateAnalysis = (analysis: Analysis) => {
    const steps = [0, 1, 2, 3]; // Steps: 0=start, 1=extraction, 2=recognition, 3=features
    let currentStepIndex = 0;

    const interval = setInterval(() => {
      currentStepIndex++;
      
      if (currentStepIndex <= steps.length) {
        setCurrentAnalysis(prev => prev ? { ...prev, currentStep: currentStepIndex } : null);
      }
      
      // Step 4 is "Sentiment Prediction" - this should take longer and show result only after completion
      if (currentStepIndex === 4) {
        // Set to step 4 (in progress) and wait longer for prediction
        setTimeout(() => {
          clearInterval(interval);
          
          // Generate mock sentiment results with more realistic variation
          const sentimentOptions = ['Positive', 'Negative', 'Neutral'];
          const emotionOptions = {
            positive: ['Happy', 'Joyful', 'Excited', 'Content'],
            negative: ['Sad', 'Angry', 'Frustrated', 'Disappointed'],
            neutral: ['Calm', 'Neutral', 'Thoughtful', 'Indifferent'],
          };
          
          // More varied sentiment selection (not just random)
          const rand = Math.random();
          const randomSentiment = rand < 0.4 ? 'Positive' : rand < 0.7 ? 'Negative' : 'Neutral';
          const emotionSet = randomSentiment === 'Positive' ? emotionOptions.positive 
            : randomSentiment === 'Negative' ? emotionOptions.negative 
            : emotionOptions.neutral;
          
          // Generate mock transcript for video/audio
          const mockTranscripts = {
            positive: "This is absolutely amazing! I'm so happy with the results. Everything turned out better than I expected. This is truly wonderful and I couldn't be more pleased.",
            negative: "I'm really disappointed with this outcome. Nothing seems to be working as intended. This is frustrating and I'm not satisfied at all.",
            neutral: "This appears to be functioning as expected. The results are within normal parameters. Everything seems to be operating according to standard procedures."
          };
          
          const completedAnalysis: Analysis = {
            ...analysis,
            status: 'completed',
            currentStep: 4, // Mark step 4 as complete
            sentiment: {
              label: randomSentiment,
              confidence: 0.82 + Math.random() * 0.15,
              emotions: {
                video: { 
                  emotion: emotionSet[Math.floor(Math.random() * emotionSet.length)], 
                  score: 0.75 + Math.random() * 0.2 
                },
                audio: { 
                  emotion: emotionSet[Math.floor(Math.random() * emotionSet.length)], 
                  score: 0.75 + Math.random() * 0.2 
                },
                text: { 
                  emotion: emotionSet[Math.floor(Math.random() * emotionSet.length)], 
                  score: 0.75 + Math.random() * 0.2 
                },
              },
              transcript: analysis.type !== 'text' 
                ? mockTranscripts[randomSentiment.toLowerCase() as keyof typeof mockTranscripts]
                : undefined
            },
          };
          
          setCurrentAnalysis(completedAnalysis);
          setAnalysisHistory(prev => [completedAnalysis, ...prev]);
        }, 2500); // Give more time for sentiment prediction step
      }
    }, 1500);
  };

  const handleViewHistory = (analysis: Analysis) => {
    setCurrentAnalysis(analysis);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-slate-800 to-gray-900 text-white relative overflow-hidden">
      <AnimatedBackground />
      
      <div className="relative z-10">
        {/* Header */}
        <header className="border-b border-white/10 backdrop-blur-sm bg-gray-900/50 sticky top-0 z-50">
          <div className="max-w-7xl mx-auto px-8 py-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-4">
                <img 
                  src={trisentiLogo} 
                  alt="TriSenti Logo" 
                  className="w-12 h-12 rounded-lg border-2 border-white/20 shadow-md object-cover" 
                />
                <div>
                  <h1 className="text-2xl sm:text-3xl font-bold bg-gradient-to-r from-blue-400 via-purple-400 to-pink-400 bg-clip-text text-transparent">
                    TriSenti AI
                  </h1>
                  <p className="text-xs sm:text-sm text-gray-400">Multimodal Sentiment Analysis Platform</p>
                </div>
              </div>
              
              <div className="hidden md:flex items-center gap-6 text-sm">
                <a href="#features" className="text-gray-400 hover:text-white transition-colors">Features</a>
                <a href="#how-it-works" className="text-gray-400 hover:text-white transition-colors">How It Works</a>
                <a href="#use-cases" className="text-gray-400 hover:text-white transition-colors">Use Cases</a>
              </div>
            </div>
          </div>
        </header>

        {/* Main Content */}
        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12 space-y-16 sm:space-y-20">
          {/* Hero Section */}
          <section className="text-center space-y-4 sm:space-y-6 py-4 sm:py-8">
            <h2 className="text-3xl sm:text-4xl md:text-5xl font-bold leading-tight px-4">
              Analyze Emotions from Video, Audio & Text
            </h2>
            <p className="text-lg sm:text-xl text-gray-400 max-w-3xl mx-auto px-4">
              Advanced deep learning models analyze multimodal inputs to detect sentiment and emotions with high accuracy
            </p>
          </section>

          {/* Input Section */}
          <section>
            <MultimodalInput onAnalyze={handleAnalyze} />
          </section>

          {/* Current Analysis */}
          {currentAnalysis && (
            <section id="analysis-progress" className="space-y-8 scroll-mt-24">
              <div className="bg-white/5 backdrop-blur-sm rounded-2xl border border-white/10 shadow-2xl p-6">
                <div className="flex items-center gap-4 mb-6">
                  <div className="w-16 h-16 bg-gradient-to-br from-blue-500 to-purple-600 rounded-xl flex items-center justify-center shadow-lg shadow-blue-500/30">
                    <span className="text-2xl">
                      {currentAnalysis.type === 'video' ? '🎥' : currentAnalysis.type === 'audio' ? '🎵' : '📝'}
                    </span>
                  </div>
                  <div>
                    <h3 className="text-xl font-semibold">{currentAnalysis.filename}</h3>
                    <p className="text-gray-400">
                      {currentAnalysis.timestamp.toLocaleString()}
                    </p>
                  </div>
                </div>
                <ProgressStepper currentStep={currentAnalysis.currentStep} />
              </div>
              {/* Only show result after last step (Sentiment Prediction) is completed with tick */}
              <ResultAfterTick currentAnalysis={currentAnalysis} />
            </section>
          )}


          {/* How It Works */}
          <section id="how-it-works">
            <HowItWorks />
          </section>

          {/* Feature Cards */}
          <section id="features">
            <div className="text-center mb-8">
              <h2 className="text-3xl font-bold mb-3">Analysis Capabilities</h2>
              <p className="text-gray-400 max-w-2xl mx-auto">
                Leverage cutting-edge AI models to extract insights from multiple data modalities
              </p>
            </div>
            <FeatureCards />
          </section>

          {/* Use Cases */}
          <section id="use-cases">
            <UseCases />
          </section>

          {/* History */}
          {analysisHistory.length > 0 && (
            <section>
              <h2 className="text-3xl font-bold mb-8">Analysis History</h2>
              <HistoryList 
                analyses={analysisHistory} 
                onViewAnalysis={handleViewHistory}
              />
            </section>
          )}
        </main>

        {/* Footer */}
        <Footer />
      </div>
    </div>
  );
}