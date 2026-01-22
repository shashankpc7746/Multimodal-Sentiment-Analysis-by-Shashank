import React from 'react';
import { motion } from 'motion/react';

export function AnimatedBackground() {
  return (
    <div className="fixed inset-0 overflow-hidden pointer-events-none">
      {/* Floating gradient orbs */}
      <motion.div
        animate={{
          x: [0, 100, 0],
          y: [0, -100, 0],
          scale: [1, 1.2, 1],
        }}
        transition={{
          duration: 20,
          repeat: Infinity,
          ease: 'easeInOut',
        }}
        className="absolute top-20 left-20 w-96 h-96 bg-blue-500/20 rounded-full blur-3xl"
      />
      
      <motion.div
        animate={{
          x: [0, -100, 0],
          y: [0, 100, 0],
          scale: [1, 1.3, 1],
        }}
        transition={{
          duration: 25,
          repeat: Infinity,
          ease: 'easeInOut',
        }}
        className="absolute top-1/2 right-20 w-[500px] h-[500px] bg-purple-500/20 rounded-full blur-3xl"
      />
      
      <motion.div
        animate={{
          x: [0, 50, 0],
          y: [0, -50, 0],
          scale: [1, 1.1, 1],
        }}
        transition={{
          duration: 18,
          repeat: Infinity,
          ease: 'easeInOut',
        }}
        className="absolute bottom-20 left-1/3 w-80 h-80 bg-pink-500/20 rounded-full blur-3xl"
      />

      {/* Animated particles */}
      {[...Array(20)].map((_, i) => (
        <motion.div
          key={i}
          animate={{
            y: [-20, -1000],
            opacity: [0, 1, 0],
          }}
          transition={{
            duration: Math.random() * 10 + 10,
            repeat: Infinity,
            delay: Math.random() * 5,
            ease: 'linear',
          }}
          className="absolute w-1 h-1 bg-blue-400/50 rounded-full"
          style={{
            left: `${Math.random() * 100}%`,
            bottom: 0,
          }}
        />
      ))}

      {/* Grid overlay */}
      <div className="absolute inset-0 bg-[linear-gradient(rgba(255,255,255,0.02)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,0.02)_1px,transparent_1px)] bg-[size:100px_100px] [mask-image:radial-gradient(ellipse_80%_50%_at_50%_50%,black,transparent)]" />
    </div>
  );
}
