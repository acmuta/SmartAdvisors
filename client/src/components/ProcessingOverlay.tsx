import { useState, useEffect } from 'react';
import { FileText, GraduationCap, Sparkles } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

interface ProcessingOverlayProps {
  isVisible: boolean;
  title: string;
  subtitle?: string;
  steps?: string[];
  icon?: 'transcript' | 'plan' | 'recommend';
}

const ICONS = {
  transcript: FileText,
  plan: GraduationCap,
  recommend: Sparkles,
};

export default function ProcessingOverlay({ isVisible, title, subtitle, steps, icon = 'recommend' }: ProcessingOverlayProps) {
  const [stepIndex, setStepIndex] = useState(0);
  const Icon = ICONS[icon];

  // Cycle through step messages every 2.5s
  useEffect(() => {
    if (!steps?.length) return;
    setStepIndex(0);
    const interval = setInterval(() => {
      setStepIndex(prev => (prev + 1) % steps.length);
    }, 2500);
    return () => clearInterval(interval);
  }, [steps]);

  const displayMessage = steps?.length ? steps[stepIndex] : subtitle;

  return (
    <AnimatePresence>
      {isVisible && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          transition={{ duration: 0.3 }}
          className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm"
        >
          <motion.div
            initial={{ opacity: 0, scale: 0.9, y: 20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.9, y: 20 }}
            transition={{ duration: 0.35, ease: 'easeOut' }}
            className="bg-white/10 backdrop-blur-xl border border-white/10 rounded-3xl px-12 py-10 text-center max-w-sm mx-4 shadow-2xl"
          >
            {/* Animated icon with spinner ring */}
            <div className="relative w-24 h-24 mx-auto mb-6">
              {/* Outer spinning ring */}
              <div className="absolute inset-0 rounded-full border-[3px] border-transparent border-t-[#FF8040] border-r-[#0046FF] animate-spin" />
              {/* Inner pulsing icon */}
              <motion.div
                animate={{ scale: [1, 1.1, 1] }}
                transition={{ duration: 2, repeat: Infinity, ease: 'easeInOut' }}
                className="absolute inset-0 flex items-center justify-center"
              >
                <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-[#FF8040]/20 to-[#0046FF]/20 border border-white/10 flex items-center justify-center">
                  <Icon className="w-8 h-8 text-[#FF8040]" />
                </div>
              </motion.div>
            </div>

            {/* Title */}
            <h3 className="text-xl font-bold text-white mb-2">{title}</h3>

            {/* Cycling step message */}
            <div className="h-6 relative overflow-hidden">
              <AnimatePresence mode="wait">
                {displayMessage && (
                  <motion.p
                    key={displayMessage}
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -10 }}
                    transition={{ duration: 0.3 }}
                    className="text-white/50 text-sm absolute inset-x-0"
                  >
                    {displayMessage}
                  </motion.p>
                )}
              </AnimatePresence>
            </div>

            {/* Pulsing dots */}
            <div className="flex items-center justify-center gap-1.5 mt-5">
              {[0, 1, 2].map(i => (
                <motion.div
                  key={i}
                  animate={{ opacity: [0.3, 1, 0.3], scale: [0.8, 1, 0.8] }}
                  transition={{ duration: 1.2, repeat: Infinity, delay: i * 0.2 }}
                  className="w-2 h-2 rounded-full bg-[#FF8040]"
                />
              ))}
            </div>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
