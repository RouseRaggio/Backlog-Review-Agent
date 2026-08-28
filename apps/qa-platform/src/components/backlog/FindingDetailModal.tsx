import React, { useEffect } from 'react';
import { FindingDTO, FindingStatus, FindingSeverity } from '../../types/backlog';
import {
  X,
  CheckCircle2,
  AlertTriangle,
  XCircle,
  ShieldAlert,
  HelpCircle,
  Lightbulb,
  Clock,
  FileCode,
} from 'lucide-react';


interface FindingDetailModalProps {
  finding: FindingDTO | null;
  onClose: () => void;
  onGenerateTestCases?: (issueKey: string, findingMsg: string) => void;
}

export const FindingDetailModal: React.FC<FindingDetailModalProps> = ({
  finding,
  onClose,
  onGenerateTestCases,
}) => {
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose();
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [onClose]);

  if (!finding) return null;

  const renderStatusBadge = (status: FindingStatus) => {
    switch (status) {
      case 'PASS':
        return (
          <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">
            <CheckCircle2 className="w-3.5 h-3.5" /> Aprobado (PASS)
          </span>
        );
      case 'WARNING':
        return (
          <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold bg-amber-500/20 text-amber-300 border border-amber-500/30">
            <AlertTriangle className="w-3.5 h-3.5" /> Advertencia (WARNING)
          </span>
        );
      case 'FAIL':
        return (
          <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold bg-rose-500/20 text-rose-300 border border-rose-500/30">
            <XCircle className="w-3.5 h-3.5" /> Fallo (FAIL)
          </span>
        );
      case 'BLOCKED':
        return (
          <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold bg-purple-500/20 text-purple-300 border border-purple-500/30">
            <ShieldAlert className="w-3.5 h-3.5" /> Bloqueante (BLOCKED)
          </span>
        );
    }
  };

  const renderSeverityBadge = (severity?: FindingSeverity | null) => {
    if (!severity) return null;
    switch (severity) {
      case 'CRITICAL':
        return <span className="px-2.5 py-0.5 rounded-md text-xs font-bold bg-rose-950 text-rose-300 border border-rose-800">CRÍTICA</span>;
      case 'HIGH':
        return <span className="px-2.5 py-0.5 rounded-md text-xs font-bold bg-orange-950 text-orange-300 border border-orange-800">ALTA</span>;
      case 'MEDIUM':
        return <span className="px-2.5 py-0.5 rounded-md text-xs font-semibold bg-amber-950 text-amber-300 border border-amber-800">MEDIA</span>;
      case 'LOW':
        return <span className="px-2.5 py-0.5 rounded-md text-xs font-medium bg-slate-800 text-slate-300 border border-slate-700">BAJA</span>;
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/75 backdrop-blur-sm animate-fadeIn">
      <div
        className="relative w-full max-w-2xl bg-slate-900 border border-slate-700 rounded-2xl shadow-2xl overflow-hidden flex flex-col max-h-[90vh]"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Modal Header */}
        <div className="flex items-center justify-between p-5 border-b border-slate-800 bg-slate-950">
          <div className="flex items-center gap-3">
            <div className="p-2 rounded-xl bg-slate-800 border border-slate-700 text-cyan-400">
              <FileCode className="w-5 h-5" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="text-base font-mono font-bold text-cyan-300">{finding.issue_key}</span>
                <span className="px-2 py-0.5 rounded text-xs bg-slate-800 text-slate-300 font-medium">
                  {finding.issue_type}
                </span>
              </div>
              <h3 className="text-sm font-semibold text-white mt-0.5">
                Regla: <span className="font-mono text-cyan-400">{finding.rule_id}</span> - {finding.rule_name}
              </h3>
            </div>
          </div>

          <button
            onClick={onClose}
            className="p-1.5 text-slate-400 hover:text-white hover:bg-slate-800 rounded-xl transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Modal Body */}
        <div className="p-6 space-y-5 overflow-y-auto text-xs">
          {/* Status & Badges Bar */}
          <div className="flex flex-wrap items-center gap-3 p-3 rounded-xl bg-slate-950/70 border border-slate-800">
            {renderStatusBadge(finding.status)}
            {renderSeverityBadge(finding.severity)}
            <div className="flex items-center gap-1 text-slate-400 ml-auto font-mono text-[11px]">
              <Clock className="w-3.5 h-3.5" />
              <span>{new Date(finding.timestamp).toLocaleString()}</span>
            </div>
          </div>

          {/* Finding Message */}
          <div className="space-y-1.5">
            <span className="font-semibold text-slate-400 uppercase tracking-wider text-[11px] flex items-center gap-1.5">
              <HelpCircle className="w-3.5 h-3.5 text-cyan-400" />
              Diagnóstico del Hallazgo
            </span>
            <div className="p-4 rounded-xl bg-slate-800/70 border border-slate-700/60 text-slate-200 leading-relaxed font-sans">
              {finding.message}
            </div>
          </div>

          {/* Recommendation */}
          {finding.recommendation && (
            <div className="space-y-1.5">
              <span className="font-semibold text-slate-400 uppercase tracking-wider text-[11px] flex items-center gap-1.5">
                <Lightbulb className="w-3.5 h-3.5 text-amber-400" />
                Recomendación de Corrección
              </span>
              <div className="p-4 rounded-xl bg-amber-950/20 border border-amber-800/40 text-amber-200 leading-relaxed font-sans">
                {finding.recommendation}
              </div>
            </div>
          )}
        </div>

        {/* Modal Footer */}
        <div className="p-4 border-t border-slate-800 bg-slate-950 flex items-center justify-between">
          {onGenerateTestCases ? (
            <button
              onClick={() => {
                onGenerateTestCases(finding.issue_key, finding.message);
                onClose();
              }}
              className="px-4 py-2 text-xs font-semibold text-white bg-gradient-to-r from-cyan-500 to-indigo-600 hover:from-cyan-400 hover:to-indigo-500 rounded-xl shadow transition-all flex items-center gap-1.5"
            >
              <span>🧪 Generar Test Cases para {finding.issue_key}</span>
            </button>
          ) : <div />}

          <button
            onClick={onClose}
            className="px-4 py-2 text-xs font-semibold text-slate-300 hover:text-white bg-slate-800 hover:bg-slate-700 rounded-xl transition-colors"
          >
            Cerrar
          </button>
        </div>
      </div>
    </div>
  );
};
