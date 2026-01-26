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
          src={URL.createObjectURL(file)}
          controls
          width={320}
          height={180}
          className="rounded-lg border border-white/10 shadow-md bg-black"
          style={{ maxWidth: 320, maxHeight: 180 }}
        >
          Your browser does not support the video tag.
        <video
          controls
          className={`rounded-lg shadow-md max-w-full h-48 sm:h-64 mx-auto ${styles['input-preview-video-bg']}`}
          src={URL.createObjectURL(file)}
        />
      <div className="bg-white/5 border border-white/10 rounded-2xl p-4 flex flex-col items-center shadow-lg animate-fade-in">
        <h4 className="font-semibold text-lg mb-2 text-purple-400">Audio Preview</h4>
        <audio
          src={URL.createObjectURL(file)}
          controls
          className="w-full max-w-xs rounded-lg border border-white/10 shadow-md bg-black"
        >
          Your browser does not support the audio tag.
        </audio>
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
