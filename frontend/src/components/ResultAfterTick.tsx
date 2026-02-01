import React from 'react';
import { SentimentResult } from './SentimentResult';
import { Analysis } from '../App';

interface ResultAfterTickProps {
  currentAnalysis: Analysis;
}

export function ResultAfterTick({ currentAnalysis }: ResultAfterTickProps) {
  const [showResult, setShowResult] = React.useState(false);
  
  React.useEffect(() => {
    // Only show result after step 4 (Sentiment Prediction) is completed AND sentiment data exists
    if (currentAnalysis.currentStep === 4 && currentAnalysis.sentiment && currentAnalysis.status === 'completed') {
      // Wait for tick animation to complete (1200ms for animation + delay)
      const timeout = setTimeout(() => setShowResult(true), 1200);
      return () => clearTimeout(timeout);
    } else {
      setShowResult(false);
    }
  }, [currentAnalysis.currentStep, currentAnalysis.sentiment, currentAnalysis.status]);
  
  if (!showResult || !currentAnalysis.sentiment) return null;
  
  return <SentimentResult sentiment={currentAnalysis.sentiment} />;
}
