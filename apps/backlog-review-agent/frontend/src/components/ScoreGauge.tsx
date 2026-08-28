import React from 'react';

interface ScoreGaugeProps {
  score: number;
}

export const ScoreGauge: React.FC<ScoreGaugeProps> = ({ score }) => {
  const getScoreColor = (value: number) => {
    if (value >= 80) return { stroke: '#10b981', bg: 'bg-emerald-500/10', text: 'text-emerald-400', label: 'Excelente Calidad', border: 'border-emerald-500/20' };
    if (value >= 60) return { stroke: '#f59e0b', bg: 'bg-amber-500/10', text: 'text-amber-400', label: 'Calidad Aceptable', border: 'border-amber-500/20' };
    return { stroke: '#ef4444', bg: 'bg-rose-500/10', text: 'text-rose-400', label: 'Calidad Crítica', border: 'border-rose-500/20' };
  };

  const config = getScoreColor(score);
  const radius = 60;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (score / 100) * circumference;

  return (
    <div className={`flex flex-col items-center justify-center p-6 rounded-2xl bg-slate-800/80 border ${config.border} backdrop-blur shadow-xl relative overflow-hidden`}>
      <div className="absolute top-0 right-0 w-32 h-32 bg-sky-500/5 rounded-full blur-2xl pointer-events-none" />
      
      <span className="text-xs font-semibold uppercase tracking-wider text-slate-400 mb-3">
        Backlog Quality Score
      </span>

      <div className="relative flex items-center justify-center my-2">
        <svg className="w-36 h-36 transform -rotate-90" viewBox="0 0 140 140">
          <circle
            cx="70"
            cy="70"
            r={radius}
            stroke="#1e293b"
            strokeWidth="10"
            fill="transparent"
          />
          <circle
            cx="70"
            cy="70"
            r={radius}
            stroke={config.stroke}
            strokeWidth="10"
            strokeDasharray={circumference}
            strokeDashoffset={strokeDashoffset}
            strokeLinecap="round"
            fill="transparent"
            className="transition-all duration-1000 ease-out"
          />
        </svg>

        <div className="absolute flex flex-col items-center justify-center text-center">
          <span className="text-3xl font-extrabold text-white tracking-tight">
            {score.toFixed(1)}<span className="text-lg font-bold text-slate-400">%</span>
          </span>
          <span className={`text-[11px] font-medium mt-0.5 ${config.text}`}>
            {config.label}
          </span>
        </div>
      </div>

      <div className="w-full mt-3 pt-3 border-t border-slate-700/50 flex justify-between text-xs text-slate-400">
        <span>BQS Global</span>
        <span className="font-semibold text-slate-300">Target: ≥ 80%</span>
      </div>
    </div>
  );
};
