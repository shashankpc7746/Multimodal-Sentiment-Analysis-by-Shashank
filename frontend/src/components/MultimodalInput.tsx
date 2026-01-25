import React, { useState, useRef } from 'react';
import { Upload, Film, Music, Type, CheckCircle, X } from 'lucide-react';
import { motion, AnimatePresence } from 'motion/react';
import { InputPreview } from './InputPreview';

interface MultimodalInputProps {
  onAnalyze: (data: { type: 'video' | 'audio' | 'text'; content: File | string }) => void;
}

type InputMode = 'video' | 'audio' | 'text';

export function MultimodalInput({ onAnalyze }: MultimodalInputProps) {
  const [activeMode, setActiveMode] = useState<InputMode>('video');
  const [isDragging, setIsDragging] = useState(false);
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);
  const [textInput, setTextInput] = useState('');
  const fileInputRef = useRef<HTMLInputElement>(null);

  const modes = [
    { id: 'video' as InputMode, label: 'Video', icon: Film, color: 'from-blue-500 to-blue-600', formats: 'MP4, MOV, AVI, MKV' },
    { id: 'audio' as InputMode, label: 'Audio', icon: Music, color: 'from-purple-500 to-purple-600', formats: 'MP3, WAV, M4A, OGG' },
    { id: 'text' as InputMode, label: 'Text', icon: Type, color: 'from-pink-500 to-pink-600', formats: 'Direct input' },
  ];

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
      {/* Input Area */}
      <motion.div
        key={activeMode}
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.3 }}
        className="px-4"
      >
        {activeMode !== 'text' ? (
          <div
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
            onClick={() => !uploadedFile && fileInputRef.current?.click()}
            className={`relative border-2 border-dashed rounded-2xl p-6 sm:p-12 transition-all cursor-pointer backdrop-blur-sm ${
              isDragging
                ? 'border-blue-500 bg-blue-500/10 scale-105'
                : uploadedFile
                ? 'border-green-500 bg-green-500/10'
                : 'border-white/20 bg-white/5 hover:border-blue-400 hover:bg-blue-400/10'
            }`}
          >
            <input
              ref={fileInputRef}
              type="file"
              accept={acceptedTypes}
              onChange={handleFileSelect}
              className="hidden"
              aria-label="Upload file"
              placeholder="Choose a file to upload"
            />
            <AnimatePresence mode="wait">
              {!uploadedFile ? (
                <motion.div
                  key="upload-prompt"
                  initial={{ opacity: 0, scale: 0.9 }}
                  animate={{ opacity: 1, scale: 1 }}
                  exit={{ opacity: 0, scale: 0.9 }}
                  className="text-center space-y-4"
                >
                  <motion.div
                    animate={{
                      y: isDragging ? -10 : [0, -10, 0],
                    }}
                    transition={{
                      y: {
                        duration: 2,
                        repeat: isDragging ? 0 : Infinity,
                        ease: 'easeInOut',
                      },
                    }}
                    className="inline-block"
                  >
                    <div className={`w-20 h-20 sm:w-24 sm:h-24 mx-auto bg-gradient-to-br ${modes.find(m => m.id === activeMode)?.color} rounded-2xl flex items-center justify-center shadow-lg`}>
                      <Upload className="w-10 h-10 sm:w-12 sm:h-12 text-white" />
                    </div>
                  </motion.div>
                  <div>
                    <h3 className="text-xl sm:text-2xl font-bold mb-2">
                      {isDragging ? `Drop your ${activeMode} here` : `Upload a ${activeMode} file`}
                    </h3>
                    <p className="text-gray-400 text-sm sm:text-base">
                      Drag and drop or click to browse
                    </p>
                    <p className="text-xs sm:text-sm text-gray-500 mt-2">
                      Supported formats: {modes.find(m => m.id === activeMode)?.formats}
                    </p>
                  </div>
                </motion.div>
              ) : (
                <motion.div
                  key="upload-success"
                  initial={{ opacity: 0, scale: 0.9 }}
                  animate={{ opacity: 1, scale: 1 }}
                  exit={{ opacity: 0, scale: 0.9 }}
                  className="flex flex-col sm:flex-row items-center gap-4"
                >
                  <motion.div
                    initial={{ scale: 0 }}
                    animate={{ scale: 1 }}
                    transition={{ type: 'spring', stiffness: 200, damping: 15 }}
                    className="w-14 h-14 sm:w-16 sm:h-16 bg-green-500 rounded-xl flex items-center justify-center shadow-lg shadow-green-500/50"
                  >
                    <CheckCircle className="w-7 h-7 sm:w-8 sm:h-8 text-white" />
                  </motion.div>
                  <div className="flex-1 text-left w-full sm:w-auto">
                    <div className="flex items-center gap-2 mb-1 justify-center sm:justify-start">
                      {activeMode === 'video' ? (
                        <Film className="w-5 h-5 text-gray-400" />
                      ) : (
                        <Music className="w-5 h-5 text-gray-400" />
                      )}
                      <h4 className="font-semibold text-base sm:text-lg truncate max-w-[200px] sm:max-w-none">{uploadedFile.name}</h4>
                    </div>
                    <p className="text-gray-400 text-sm text-center sm:text-left">
                      {(uploadedFile.size / (1024 * 1024)).toFixed(2)} MB
                    </p>
                  </div>
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      setUploadedFile(null);
                    }}
                    className="p-2 text-gray-400 hover:text-white hover:bg-white/10 rounded-lg transition-colors"
                    title="Remove uploaded file"
                  >
                    <X className="w-5 h-5" />
                  </button>
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        ) : (
          <div className="bg-white/5 backdrop-blur-sm border border-white/20 rounded-2xl p-4 sm:p-6 space-y-4">
            <div className="flex items-center gap-3 mb-2">
              <div className="w-10 h-10 sm:w-12 sm:h-12 bg-gradient-to-br from-pink-500 to-pink-600 rounded-xl flex items-center justify-center shadow-lg">
                <Type className="w-5 h-5 sm:w-6 sm:h-6 text-white" />
              </div>
              <div>
                <h3 className="text-lg sm:text-xl font-bold">Enter Text for Analysis</h3>
                <p className="text-xs sm:text-sm text-gray-400">Type or paste your text below</p>
              </div>
            </div>
            <textarea
              value={textInput}
              onChange={(e) => setTextInput(e.target.value)}
              placeholder="Enter your text here... (e.g., 'I'm so happy today! This is the best day ever!' or 'I'm feeling really disappointed about the results.')"
              className="w-full h-40 sm:h-48 px-3 sm:px-4 py-2 sm:py-3 bg-white/5 border border-white/20 rounded-xl text-white placeholder-gray-500 focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none text-sm sm:text-base"
            />
            <div className="flex items-center justify-between text-sm">
              <span className="text-gray-400">
                {textInput.length} characters
              </span>
              <span className="text-gray-500">
                Minimum 10 characters recommended
              </span>
            </div>
          </div>
        )}
      </motion.div>

      {/* Preview Section (below input area) */}
      {(uploadedFile && (activeMode === 'video' || activeMode === 'audio')) || (activeMode === 'text' && textInput.trim()) ? (
        <div className="mt-6 flex justify-center">
          <InputPreview
            type={activeMode}
            file={activeMode !== 'text' ? uploadedFile : undefined}
            text={activeMode === 'text' ? textInput : undefined}
          />
        </div>
      ) : null}
                    }}
                    className="inline-block"
                  >
                    <div className={`w-20 h-20 sm:w-24 sm:h-24 mx-auto bg-gradient-to-br ${modes.find(m => m.id === activeMode)?.color} rounded-2xl flex items-center justify-center shadow-lg`}>
                      <Upload className="w-10 h-10 sm:w-12 sm:h-12 text-white" />
                    </div>
                  </motion.div>
                  
                  <div>
                    <h3 className="text-xl sm:text-2xl font-bold mb-2">
                      {isDragging ? `Drop your ${activeMode} here` : `Upload a ${activeMode} file`}
                    </h3>
                    <p className="text-gray-400 text-sm sm:text-base">
                      Drag and drop or click to browse
                    </p>
                    <p className="text-xs sm:text-sm text-gray-500 mt-2">
                      Supported formats: {modes.find(m => m.id === activeMode)?.formats}
                    </p>
                  </div>
                </motion.div>
              ) : (
                <motion.div
                  key="upload-success"
                  initial={{ opacity: 0, scale: 0.9 }}
                  animate={{ opacity: 1, scale: 1 }}
                  exit={{ opacity: 0, scale: 0.9 }}
                  className="flex flex-col sm:flex-row items-center gap-4"
                >
                  <motion.div
                    initial={{ scale: 0 }}
                    animate={{ scale: 1 }}
                    transition={{ type: 'spring', stiffness: 200, damping: 15 }}
                    className="w-14 h-14 sm:w-16 sm:h-16 bg-green-500 rounded-xl flex items-center justify-center shadow-lg shadow-green-500/50"
                  >
                    <CheckCircle className="w-7 h-7 sm:w-8 sm:h-8 text-white" />
                  </motion.div>

                  <div className="flex-1 text-left w-full sm:w-auto">
                    <div className="flex items-center gap-2 mb-1 justify-center sm:justify-start">
                      {activeMode === 'video' ? (
                        <Film className="w-5 h-5 text-gray-400" />
                      ) : (
                        <Music className="w-5 h-5 text-gray-400" />
                      )}
                      <h4 className="font-semibold text-base sm:text-lg truncate max-w-[200px] sm:max-w-none">{uploadedFile.name}</h4>
                    </div>
                    <p className="text-gray-400 text-sm text-center sm:text-left">
                      {(uploadedFile.size / (1024 * 1024)).toFixed(2)} MB
                    </p>

                    {/* Video preview for uploaded video */}
                    {activeMode === 'video' && uploadedFile && (
                      <div className="mt-3 flex justify-center">
                        <video
                          src={URL.createObjectURL(uploadedFile)}
                          controls
                          width={320}
                          height={180}
                          className="rounded-lg border border-white/10 shadow-md bg-black"
                          style={{ maxWidth: 320, maxHeight: 180 }}
                        >
                          Your browser does not support the video tag.
                        </video>
                      </div>
                    )}
                  </div>

                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      setUploadedFile(null);
                    }}
                    className="p-2 text-gray-400 hover:text-white hover:bg-white/10 rounded-lg transition-colors"
                    title="Remove uploaded file"
                  >
                    <X className="w-5 h-5" />
                  </button>
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        ) : (
          <div className="bg-white/5 backdrop-blur-sm border border-white/20 rounded-2xl p-4 sm:p-6 space-y-4">
            <div className="flex items-center gap-3 mb-2">
              <div className="w-10 h-10 sm:w-12 sm:h-12 bg-gradient-to-br from-pink-500 to-pink-600 rounded-xl flex items-center justify-center shadow-lg">
                <Type className="w-5 h-5 sm:w-6 sm:h-6 text-white" />
              </div>
              <div>
                <h3 className="text-lg sm:text-xl font-bold">Enter Text for Analysis</h3>
                <p className="text-xs sm:text-sm text-gray-400">Type or paste your text below</p>
              </div>
            </div>
            
            <textarea
              value={textInput}
              onChange={(e) => setTextInput(e.target.value)}
              placeholder="Enter your text here... (e.g., 'I'm so happy today! This is the best day ever!' or 'I'm feeling really disappointed about the results.')"
              className="w-full h-40 sm:h-48 px-3 sm:px-4 py-2 sm:py-3 bg-white/5 border border-white/20 rounded-xl text-white placeholder-gray-500 focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none text-sm sm:text-base"
            />
            
            <div className="flex items-center justify-between text-sm">
              <span className="text-gray-400">
                {textInput.length} characters
              </span>
              <span className="text-gray-500">
                Minimum 10 characters recommended
              </span>
            </div>
          </div>
        )}
      </motion.div>

      {/* Analyze Button */}
      <motion.button
        whileHover={{ scale: canAnalyze ? 1.02 : 1 }}
        whileTap={{ scale: canAnalyze ? 0.98 : 1 }}
        onClick={handleAnalyze}
        disabled={!canAnalyze}
        className={`w-full py-3 sm:py-4 rounded-xl font-semibold text-base sm:text-lg transition-all mx-4 sm:mx-0 ${
          canAnalyze
            ? 'bg-gradient-to-r from-blue-600 to-purple-600 text-white shadow-lg shadow-blue-500/50 hover:shadow-blue-500/70 cursor-pointer'
            : 'bg-white/5 text-gray-500 cursor-not-allowed border border-white/10'
        }`}
      >
        {canAnalyze ? '🚀 Analyze Sentiment' : '⚠️ Please provide input to analyze'}
      </motion.button>
    </div>
  );
}