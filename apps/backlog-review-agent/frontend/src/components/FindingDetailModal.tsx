import React, { useEffect } from 'react';
import { FindingDTO } from '../types/api';
import { X, CheckCircle2, XCircle, AlertTriangle, ShieldAlert, BookOpen, Lightbulb, Tag, FileText } from 'lucide-react';

interface FindingDetailModalProps {
  finding: FindingDTO | null;
  onClose: () => void;
}

export const FindingDetailModal: React.FC<FindingDetailModalProps> = ({
  finding,
  onClose,
}) => {
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        onClose();
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [onClose]);

  if (!finding) return null;

  const renderStatusBadge = (status: string) => {
    switch (status) {
      case 'PASS':
        return (
          <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">
            <CheckCircle2 className="w-3.5 h-3.5" /> PASS
          </span>
        );
      case 'FAIL':
        return (
          <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold bg-rose-500/20 text-rose-300 border border-rose-500/30">
            <XCircle className="w-3.5 h-3.5" /> FAIL
          </span>
        );
      case 'WARNING':
        return (
          <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold bg-amber-500/20 text-amber-300 border border-amber-500/30">
            <AlertTriangle className="w-3.5 h-3.5" /> WARNING
          </span>
        );
      case 'BLOCKED':
        return (
          <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold bg-purple-500/20 text-purple-300 border border-purple-500/30">
            <ShieldAlert className="w-3.5 h-3.5" /> BLOCKED
          </span>
        );
      default:
        return (
          <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold bg-slate-800 text-slate-300 border border-slate-700">
            {status}
          </span>
        );
    }
  };

  const renderSeverityBadge = (severity?: string | null) => {
    if (!severity) return null;
    switch (severity.toUpperCase()) {
      case 'CRITICAL':
        return (
          <span className="px-2.5 py-1 rounded-md text-xs font-bold bg-rose-950 text-rose-300 border border-rose-700 uppercase tracking-wide">
            Severidad: CRITICAL
          </span>
        );
      case 'HIGH':
        return (
          <span className="px-2.5 py-1 rounded-md text-xs font-bold bg-orange-950 text-orange-300 border border-orange-700 uppercase tracking-wide">
            Severidad: HIGH
          </span>
        );
      case 'MEDIUM':
        return (
          <span className="px-2.5 py-1 rounded-md text-xs font-semibold bg-amber-950 text-amber-300 border border-amber-700 uppercase tracking-wide">
            Severidad: MEDIUM
          </span>
        );
      case 'LOW':
        return (
          <span className="px-2.5 py-1 rounded-md text-xs font-medium bg-slate-800 text-slate-300 border border-slate-700 uppercase tracking-wide">
            Severidad: LOW
          </span>
        );
      default:
        return <span className="text-xs text-slate-300">{severity}</span>;
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm animate-fadeIn">
      <div
        className="relative w-full max-w-2xl bg-slate-900 border border-slate-700 rounded-2xl shadow-2xl overflow-hidden flex flex-col max-h-[90vh]"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="flex items-center justify-between p-5 border-b border-slate-800 bg-slate-850">
          <div className="flex items-center gap-3">
            <div className="p-2 rounded-xl bg-sky-500/10 text-sky-400 border border-sky-500/20">
              <FileText className="w-5 h-5" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="text-lg font-mono font-bold text-sky-300">{finding.issue_key}</span>
                <span className="px-2 py-0.5 rounded text-xs bg-slate-800 text-slate-300 font-medium border border-slate-700">
                  {finding.issue_type}
                </span>
              </div>
              <p className="text-xs text-slate-400 mt-0.5">Detalle del hallazgo de auditoría</p>
            </div>
          </div>

          <button
            onClick={onClose}
            className="p-2 text-slate-400 hover:text-white hover:bg-slate-800 rounded-xl transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Body */}
        <div className="p-6 space-y-6 overflow-y-auto">
          {/* Status & Severity Bar */}
          <div className="flex flex-wrap items-center gap-3 p-3.5 rounded-xl bg-slate-800/60 border border-slate-700/60">
            {renderStatusBadge(finding.status)}
            {renderSeverityBadge(finding.severity)}
          </div>

          {/* Rule Info */}
          <div className="space-y-2">
            <div className="flex items-center gap-2 text-xs font-semibold text-slate-400 uppercase tracking-wider">
              <BookOpen className="w-4 h-4 text-indigo-400" />
              <span>Regla de Calidad</span>
            </div>
            <div className="p-4 rounded-xl bg-slate-800/80 border border-slate-700/70">
              <div className="flex items-center gap-2">
                <span className="px-2 py-0.5 rounded bg-indigo-950 text-indigo-300 border border-indigo-700/60 text-xs font-mono font-bold">
                  {finding.rule_id}
                </span>
                <span className="text-sm font-semibold text-white">
                  {finding.rule_name}
                </span>
              </div>
            </div>
          </div>

          {/* Message */}
          <div className="space-y-2">
            <div className="flex items-center gap-2 text-xs font-semibold text-slate-400 uppercase tracking-wider">
              <Tag className="w-4 h-4 text-sky-400" />
              <span>Mensaje del Análisis</span>
            </div>
            <div className="p-4 rounded-xl bg-slate-800/80 border border-slate-700/70 text-sm text-slate-200 leading-relaxed">
              {finding.message || 'Sin mensaje adicional.'}
            </div>
          </div>

          {/* Recommendation */}
          <div className="space-y-2">
            <div className="flex items-center gap-2 text-xs font-semibold text-slate-400 uppercase tracking-wider">
              <Lightbulb className="w-4 h-4 text-amber-400" />
              <span>Recomendación de Mejora</span>
            </div>
            <div className="p-4 rounded-xl bg-amber-950/20 border border-amber-800/40 text-sm text-amber-200/90 leading-relaxed">
              {finding.recommendation ? (
                finding.recommendation
              ) : (
                <span className="text-slate-500 italic">No hay recomendaciones específicas para este hallazgo.</span>
              )}
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="p-4 border-t border-slate-800 bg-slate-900 flex justify-end">
          <button
            onClick={onClose}
            className="px-5 py-2 text-xs font-semibold text-slate-300 hover:text-white bg-slate-800 hover:bg-slate-700 rounded-xl transition-colors"
          >
            Cerrar
          </button>
        </div>
      </div>
    </div>
  );
};
