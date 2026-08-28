import React from 'react';
import { Award, AlertTriangle, CheckCircle, XCircle } from 'lucide-react';

interface ScoreGaugeProps {
  score: number;
}

export const ScoreGauge: React.FC<ScoreGaugeProps> = ({ score }) => {
  const normalizedScore = Math.max(0, Math.min(100, Math.round(score)));

  let colorClass = 'text-emerald-400';
  let strokeClass = 'stroke-emerald-400';
  let label = 'Excelente';
  let Icon = CheckCircle;
  let bgGradient = 'from-emerald-500/10 to-transparent';
  let borderClass = 'border-emerald-500/20';

  if (normalizedScore < 50) {
    colorClass = 'text-rose-400';
    strokeClass = 'stroke-rose-400';
    label = 'Crítico';
    Icon = XCircle;
    bgGradient = 'from-rose-500/10 to-transparent';
    borderClass = 'border-rose-500/20';
  } else if (normalizedScore < 75) {
    colorClass = 'text-amber-400';
    strokeClass = 'stroke-amber-400';
    label = 'Mejorable';
    Icon = AlertTriangle;
    bgGradient = 'from-amber-500/10 to-transparent';
    borderClass = 'border-amber-500/20';
  }

  const radius = 58;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (normalizedScore / 100) * circumference;

  return (
    <div
      className={`p-6 rounded-2xl bg-gradient-to-b ${bgGradient} bg-slate-800/80 border ${borderClass} backdrop-blur shadow-xl flex flex-col items-center justify-center text-center relative overflow-hidden`}
    >
      <div className="flex items-center gap-1.5 text-xs font-semibold uppercase tracking-wider text-slate-400 mb-3">
        <Award className="w-4 h-4 text-cyan-400" />
        <span>Backlog Quality Score</span>
      </div>

      <div className="relative w-36 h-36 flex items-center justify-center">
        <svg className="w-full h-full transform -rotate-90" viewBox="0 0 140 140">
          <circle
            cx="70"
            cy="70"
            r={radius}
            className="stroke-slate-700/60"
            strokeWidth="10"
            fill="transparent"
          />
          <circle
            cx="70"
            cy="70"
            r={radius}
            className={`${strokeClass} transition-all duration-1000 ease-out`}
            strokeWidth="10"
            strokeDasharray={circumference}
            strokeDashoffset={strokeDashoffset}
            strokeLinecap="round"
            fill="transparent"
          />
        </svg>

        <div className="absolute flex flex-col items-center">
          <span className={`text-3xl font-black tracking-tight ${colorClass}`}>
            {normalizedScore}%
          </span>
          <span className="text-[10px] text-slate-400 font-medium uppercase mt-0.5">
            Calidad Global
          </span>
        </div>
      </div>

      <div className="mt-3 flex items-center gap-1.5 text-xs font-medium text-slate-300">
        <Icon className={`w-3.5 h-3.5 ${colorClass}`} />
        <span>Nivel: <strong className={colorClass}>{label}</strong></span>
      </div>
    </div>
  );
};
