import React from 'react';
import { SentimentResult } from './SentimentResult';

export function ResultAfterTick({ currentAnalysis }) {
  const [showResult, setShowResult] = React.useState(false);
  React.useEffect(() => {
    if (currentAnalysis.currentStep === 6 && currentAnalysis.sentiment) {
      // Wait for tick animation (e.g., 700ms)
      const timeout = setTimeout(() => setShowResult(true), 700);
      return () => clearTimeout(timeout);
    } else {
      setShowResult(false);
    }
  }, [currentAnalysis.currentStep, currentAnalysis.sentiment]);
  if (!showResult) return null;
  return <SentimentResult sentiment={currentAnalysis.sentiment} />;
}
