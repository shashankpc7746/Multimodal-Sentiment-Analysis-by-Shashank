import React from 'react';
import styles from './InputPreview.module.css';

interface InputPreviewProps {
  type: 'video' | 'audio' | 'text';
  file?: File | null;
  text?: string;
}

export function InputPreview({ type, file, text }: InputPreviewProps) {
  if (type === 'video' && file) {
    return (
      <div className="bg-white/5 border border-white/10 rounded-2xl p-4 flex flex-col items-center shadow-lg animate-fade-in">
        <h4 className="font-semibold text-lg mb-2 text-blue-400">Video Preview</h4>
        <video
          controls
          className={`rounded-lg shadow-md max-w-full h-48 sm:h-64 mx-auto ${styles['input-preview-video-bg']}`}
          src={URL.createObjectURL(file)}
        >
          Your browser does not support the video tag.
        </video>
      </div>
    );
  }

  if (type === 'audio' && file) {
    return (
      <div className="bg-gradient-to-br from-purple-900/30 to-indigo-900/30 border border-purple-500/30 rounded-2xl p-6 flex flex-col items-center shadow-xl animate-fade-in backdrop-blur-sm">
        <div className="flex items-center gap-3 mb-4">
          <div className="w-12 h-12 rounded-full bg-purple-500/20 flex items-center justify-center">
            <svg className="w-6 h-6 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19V6l12-3v13M9 19c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zm12-3c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zM9 10l12-3" />
            </svg>
          </div>
          <div>
            <h4 className="font-semibold text-lg text-purple-300">Audio Preview</h4>
            <p className="text-sm text-gray-400 truncate max-w-[200px]">{file.name}</p>
          </div>
        </div>
        
        {/* Waveform visualization placeholder */}
        <div className="w-full max-w-md mb-4 h-16 bg-black/30 rounded-lg flex items-center justify-center px-4 overflow-hidden">
          <div className="flex items-end gap-1 h-12">
            {[...Array(32)].map((_, i) => (
              <div
                key={i}
                className="w-1.5 bg-gradient-to-t from-purple-500 to-pink-500 rounded-full animate-pulse"
                style={{
                  height: `${Math.random() * 100}%`,
                  animationDelay: `${i * 0.05}s`,
                  animationDuration: '1s'
                }}
              />
            ))}
          </div>
        </div>
        
        {/* Audio player */}
        <div className="w-full max-w-md bg-black/40 rounded-xl p-3 border border-purple-500/20">
          <audio
            src={URL.createObjectURL(file)}
            controls
            className="w-full h-10"
            style={{ 
              filter: 'invert(1) hue-rotate(180deg)',
              opacity: 0.9
            }}
          >
            Your browser does not support the audio tag.
          </audio>
        </div>
        
        {/* File info */}
        <div className="mt-3 text-xs text-gray-500 flex items-center gap-2">
          <span className="px-2 py-1 bg-purple-500/10 rounded-full text-purple-400">
            {(file.size / (1024 * 1024)).toFixed(2)} MB
          </span>
          <span className="px-2 py-1 bg-purple-500/10 rounded-full text-purple-400">
            {file.type || 'audio/*'}
          </span>
        </div>
      </div>
    );
  }

  if (type === 'text' && text) {
    return (
      <div className="bg-white/5 border border-white/10 rounded-2xl p-4 flex flex-col items-center shadow-lg animate-fade-in">
        <h4 className="font-semibold text-lg mb-2 text-pink-400">Text Preview</h4>
        <div className="w-full max-w-xl whitespace-pre-wrap text-white text-base bg-black/20 rounded-lg p-3 border border-white/10">
          {text}
        </div>
      </div>
    );
  }

  return null;
}
