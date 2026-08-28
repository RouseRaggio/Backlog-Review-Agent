import React from 'react';
import { StatisticsDTO } from '../types/api';
import { Layers, FileText, CheckCircle2, AlertTriangle, XCircle, ShieldAlert } from 'lucide-react';

interface StatsCardsProps {
  statistics: StatisticsDTO;
}

export const StatsCards: React.FC<StatsCardsProps> = ({ statistics }) => {
  return (
    <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
      {/* Total Issues */}
      <div className="p-4 rounded-xl bg-slate-800/80 border border-slate-700/60 backdrop-blur flex flex-col justify-between hover:border-slate-600 transition-colors">
        <div className="flex items-center justify-between text-slate-400">
          <span className="text-xs font-medium">Total Issues</span>
          <Layers className="w-4 h-4 text-sky-400" />
        </div>
        <div className="mt-3">
          <span className="text-2xl font-bold text-white tracking-tight">{statistics.total_issues}</span>
          <span className="text-[11px] text-slate-400 ml-1.5 font-normal">únicas</span>
        </div>
      </div>

      {/* Total Findings */}
      <div className="p-4 rounded-xl bg-slate-800/80 border border-slate-700/60 backdrop-blur flex flex-col justify-between hover:border-slate-600 transition-colors">
        <div className="flex items-center justify-between text-slate-400">
          <span className="text-xs font-medium">Total Findings</span>
          <FileText className="w-4 h-4 text-indigo-400" />
        </div>
        <div className="mt-3">
          <span className="text-2xl font-bold text-white tracking-tight">{statistics.total_findings}</span>
          <span className="text-[11px] text-slate-400 ml-1.5 font-normal">reglas</span>
        </div>
      </div>

      {/* Passed */}
      <div className="p-4 rounded-xl bg-emerald-950/20 border border-emerald-800/40 backdrop-blur flex flex-col justify-between hover:border-emerald-700/60 transition-colors">
        <div className="flex items-center justify-between text-emerald-400">
          <span className="text-xs font-medium">Passed</span>
          <CheckCircle2 className="w-4 h-4 text-emerald-400" />
        </div>
        <div className="mt-3">
          <span className="text-2xl font-bold text-emerald-300 tracking-tight">{statistics.passed}</span>
          <span className="text-[11px] text-emerald-500/80 ml-1.5 font-normal">cumplidas</span>
        </div>
      </div>

      {/* Failed */}
      <div className="p-4 rounded-xl bg-rose-950/20 border border-rose-800/40 backdrop-blur flex flex-col justify-between hover:border-rose-700/60 transition-colors">
        <div className="flex items-center justify-between text-rose-400">
          <span className="text-xs font-medium">Failed</span>
          <XCircle className="w-4 h-4 text-rose-400" />
        </div>
        <div className="mt-3">
          <span className="text-2xl font-bold text-rose-300 tracking-tight">{statistics.failed}</span>
          <span className="text-[11px] text-rose-500/80 ml-1.5 font-normal">fallidas</span>
        </div>
      </div>

      {/* Warnings */}
      <div className="p-4 rounded-xl bg-amber-950/20 border border-amber-800/40 backdrop-blur flex flex-col justify-between hover:border-amber-700/60 transition-colors">
        <div className="flex items-center justify-between text-amber-400">
          <span className="text-xs font-medium">Warnings</span>
          <AlertTriangle className="w-4 h-4 text-amber-400" />
        </div>
        <div className="mt-3">
          <span className="text-2xl font-bold text-amber-300 tracking-tight">{statistics.warnings}</span>
          <span className="text-[11px] text-amber-500/80 ml-1.5 font-normal">alertas</span>
        </div>
      </div>

      {/* Blocked */}
      <div className="p-4 rounded-xl bg-purple-950/20 border border-purple-800/40 backdrop-blur flex flex-col justify-between hover:border-purple-700/60 transition-colors">
        <div className="flex items-center justify-between text-purple-400">
          <span className="text-xs font-medium">Blocked</span>
          <ShieldAlert className="w-4 h-4 text-purple-400" />
        </div>
        <div className="mt-3">
          <span className="text-2xl font-bold text-purple-300 tracking-tight">{statistics.blocked}</span>
          <span className="text-[11px] text-purple-500/80 ml-1.5 font-normal">bloqueadas</span>
        </div>
      </div>
    </div>
  );
};
