import React from 'react';
import { motion } from 'motion/react';

export function Footer() {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="relative z-10 border-t border-white/10 backdrop-blur-sm bg-gray-900/50 mt-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center text-gray-400 text-xs sm:text-sm"
        >
          <p>
            © {currentYear} <span className="text-blue-400 font-semibold">TriSenti AI</span> • 
            Developed by <span className="text-purple-400 font-semibold">Shashank</span> • 
            All Rights Reserved
          </p>
        </motion.div>
      </div>
    </footer>
  );
}