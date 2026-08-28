import React from 'react';
import { SummaryMetricsDTO } from '../types/api';
import {
  Layers,
  CheckCircle2,
  XCircle,
  AlertTriangle,
  GitBranch,
  AlertCircle,
  Maximize2,
} from 'lucide-react';


interface GenerationSummaryCardsProps {
  summary: SummaryMetricsDTO;
  warnings: string[];
}

export const GenerationSummaryCards: React.FC<GenerationSummaryCardsProps> = ({
  summary,
  warnings,
}) => {
  const getConfidenceBadge = (confidence: string) => {
    switch (confidence.toUpperCase()) {
      case 'HIGH':
        return { text: 'Alta', color: 'text-emerald-400', bg: 'bg-emerald-500/10', border: 'border-emerald-500/30' };
      case 'MEDIUM':
        return { text: 'Media', color: 'text-amber-400', bg: 'bg-amber-500/10', border: 'border-amber-500/30' };
      default:
        return { text: 'Baja (Revisión requerida)', color: 'text-rose-400', bg: 'bg-rose-500/10', border: 'border-rose-500/30' };
    }
  };

  const conf = getConfidenceBadge(summary.overall_confidence);

  return (
    <div className="space-y-4">
      {/* Metric Cards Grid */}
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
        {/* Total Cases */}
        <div className="p-4 rounded-xl bg-slate-900/80 border border-slate-800 backdrop-blur flex flex-col justify-between">
          <div className="flex items-center justify-between text-slate-400">
            <span className="text-xs font-medium">Total Casos</span>
            <Layers className="w-4 h-4 text-cyan-400" />
          </div>
          <div className="mt-2">
            <span className="text-2xl font-bold text-white tracking-tight">{summary.total_cases}</span>
          </div>
        </div>

        {/* Positivos */}
        <div className="p-4 rounded-xl bg-emerald-950/20 border border-emerald-800/40 backdrop-blur flex flex-col justify-between">
          <div className="flex items-center justify-between text-emerald-400">
            <span className="text-xs font-medium">Positivos</span>
            <CheckCircle2 className="w-4 h-4 text-emerald-400" />
          </div>
          <div className="mt-2">
            <span className="text-2xl font-bold text-emerald-300 tracking-tight">{summary.positive_count}</span>
          </div>
        </div>

        {/* Negativos */}
        <div className="p-4 rounded-xl bg-rose-950/20 border border-rose-800/40 backdrop-blur flex flex-col justify-between">
          <div className="flex items-center justify-between text-rose-400">
            <span className="text-xs font-medium">Negativos</span>
            <XCircle className="w-4 h-4 text-rose-400" />
          </div>
          <div className="mt-2">
            <span className="text-2xl font-bold text-rose-300 tracking-tight">{summary.negative_count}</span>
          </div>
        </div>

        {/* Validación */}
        <div className="p-4 rounded-xl bg-amber-950/20 border border-amber-800/40 backdrop-blur flex flex-col justify-between">
          <div className="flex items-center justify-between text-amber-400">
            <span className="text-xs font-medium">Validación</span>
            <AlertTriangle className="w-4 h-4 text-amber-400" />
          </div>
          <div className="mt-2">
            <span className="text-2xl font-bold text-amber-300 tracking-tight">{summary.validation_count}</span>
          </div>
        </div>

        {/* Límites */}
        <div className="p-4 rounded-xl bg-purple-950/20 border border-purple-800/40 backdrop-blur flex flex-col justify-between">
          <div className="flex items-center justify-between text-purple-400">
            <span className="text-xs font-medium">Límites (Boundary)</span>
            <Maximize2 className="w-4 h-4 text-purple-400" />
          </div>
          <div className="mt-2">
            <span className="text-2xl font-bold text-purple-300 tracking-tight">{summary.boundary_count}</span>
          </div>
        </div>

        {/* Trazabilidad & Confianza */}
        <div className="p-4 rounded-xl bg-slate-900/80 border border-slate-800 backdrop-blur flex flex-col justify-between">
          <div className="flex items-center justify-between text-slate-400">
            <span className="text-xs font-medium">Trazabilidad</span>
            <GitBranch className="w-4 h-4 text-cyan-400" />
          </div>
          <div className="mt-2 flex items-baseline justify-between">
            <span className="text-xl font-bold text-cyan-300 tracking-tight">{summary.traceability_rate}%</span>
            <span className={`text-[10px] px-1.5 py-0.5 rounded font-semibold ${conf.bg} ${conf.color} border ${conf.border}`}>
              {conf.text}
            </span>
          </div>
        </div>
      </div>

      {/* Warnings Banner */}
      {warnings.length > 0 && (
        <div className="p-4 rounded-xl bg-amber-950/30 border border-amber-800/50 space-y-2">
          <div className="flex items-center gap-2 text-amber-400 text-xs font-semibold uppercase tracking-wider">
            <AlertCircle className="w-4 h-4 shrink-0" />
            <span>Advertencias de Suficiencia / No Invención</span>
          </div>
          <ul className="space-y-1 text-xs text-amber-200/90 list-disc list-inside">
            {warnings.map((w, idx) => (
              <li key={idx}>{w}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};
