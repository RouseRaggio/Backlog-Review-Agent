import React, { useEffect, useState } from 'react';
import { TestCaseDTO } from '../../types/testCase';
import {
  X,
  Copy,
  Check,
  CheckCircle2,
  XCircle,
  AlertTriangle,
  Maximize2,
  Shield,
  Layers,
  ListOrdered,
  FileCheck,
  FileText,
} from 'lucide-react';

interface TestCaseDetailModalProps {
  testCase: TestCaseDTO | null;
  onClose: () => void;
}

export const TestCaseDetailModal: React.FC<TestCaseDetailModalProps> = ({
  testCase,
  onClose,
}) => {
  const [copied, setCopied] = useState(false);

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose();
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [onClose]);

  if (!testCase) return null;

  const handleCopy = () => {
    const formatted = `=== ${testCase.id}: ${testCase.title} ===
Tipo: ${testCase.type} | Prioridad: ${testCase.priority} | Categoría: ${testCase.category}
Criterio: ${testCase.acceptance_criteria_reference || 'USER_STORY'} (Requisito: ${testCase.requirement_reference})
Confianza: ${testCase.confidence}

Precondiciones:
${testCase.preconditions.map((p) => `- ${p}`).join('\n')}

Datos requeridos:
${Object.entries(testCase.required_data).map(([k, v]) => `- ${k}: ${v}`).join('\n')}

Pasos:
${testCase.steps.join('\n')}

Resultado Esperado:
${testCase.expected_result}`;

    navigator.clipboard.writeText(formatted);
    setCopied(true);
    setTimeout(() => setCopied(false), 2500);
  };

  const renderTypeBadge = (type: string) => {
    switch (type) {
      case 'POSITIVE':
        return (
          <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">
            <CheckCircle2 className="w-3.5 h-3.5" /> POSITIVO
          </span>
        );
      case 'NEGATIVE':
        return (
          <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold bg-rose-500/20 text-rose-300 border border-rose-500/30">
            <XCircle className="w-3.5 h-3.5" /> NEGATIVO
          </span>
        );
      case 'VALIDATION':
        return (
          <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold bg-amber-500/20 text-amber-300 border border-amber-500/30">
            <AlertTriangle className="w-3.5 h-3.5" /> VALIDACIÓN
          </span>
        );
      case 'BOUNDARY':
        return (
          <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold bg-purple-500/20 text-purple-300 border border-purple-500/30">
            <Maximize2 className="w-3.5 h-3.5" /> LÍMITE (BOUNDARY)
          </span>
        );
      default:
        return <span className="text-xs text-slate-300">{type}</span>;
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/75 backdrop-blur-sm animate-fadeIn">
      <div
        className="relative w-full max-w-3xl bg-slate-900 border border-slate-700 rounded-2xl shadow-2xl overflow-hidden flex flex-col max-h-[90vh]"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="flex items-center justify-between p-5 border-b border-slate-800 bg-slate-950">
          <div className="flex items-center gap-3">
            <div className="p-2 rounded-xl bg-cyan-500/10 text-cyan-400 border border-cyan-500/20">
              <FileCheck className="w-5 h-5" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="text-base font-mono font-bold text-cyan-300">{testCase.id}</span>
                <span className="px-2 py-0.5 rounded text-[11px] bg-slate-800 text-slate-300 font-medium border border-slate-700">
                  {testCase.category}
                </span>
                <span className="px-2 py-0.5 rounded text-[11px] bg-slate-800 text-slate-300 font-mono">
                  {testCase.priority}
                </span>
              </div>
              <h3 className="text-sm font-semibold text-white mt-1">{testCase.title}</h3>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={handleCopy}
              className="inline-flex items-center gap-1.5 px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-medium rounded-xl border border-slate-700 transition-colors"
            >
              {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
              <span>{copied ? 'Copiado' : 'Copiar'}</span>
            </button>
            <button
              onClick={onClose}
              className="p-1.5 text-slate-400 hover:text-white hover:bg-slate-800 rounded-xl transition-colors"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* Body Content */}
        <div className="p-6 space-y-5 overflow-y-auto text-xs">
          {/* Status & Badges Bar */}
          <div className="flex flex-wrap items-center gap-3 p-3 rounded-xl bg-slate-950/70 border border-slate-800">
            {renderTypeBadge(testCase.type)}
            <span className="px-2.5 py-1 rounded-md text-xs font-semibold bg-slate-800 text-slate-300">
              Confianza: {testCase.confidence}
            </span>
            <span className="px-2.5 py-1 rounded-md text-xs font-mono text-cyan-400 bg-cyan-950/40 border border-cyan-800/40 ml-auto">
              Criterio: {testCase.acceptance_criteria_reference || 'USER_STORY'} (Requisito: {testCase.requirement_reference})
            </span>
          </div>

          {/* Description */}
          <div className="space-y-1.5">
            <span className="font-semibold text-slate-400 uppercase tracking-wider text-[11px]">
              Descripción
            </span>
            <p className="p-3.5 rounded-xl bg-slate-800/60 border border-slate-800 text-slate-200 leading-relaxed">
              {testCase.description}
            </p>
          </div>

          {/* Preconditions & Required Data */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-1.5">
              <span className="font-semibold text-slate-400 uppercase tracking-wider text-[11px] flex items-center gap-1">
                <Shield className="w-3.5 h-3.5 text-cyan-400" /> Precondiciones
              </span>
              <div className="p-3 rounded-xl bg-slate-800/60 border border-slate-800 space-y-1 text-slate-300">
                {testCase.preconditions.length === 0 ? (
                  <span className="text-slate-500 italic">Sin precondiciones adicionales.</span>
                ) : (
                  testCase.preconditions.map((p, idx) => (
                    <div key={idx} className="flex items-start gap-1.5">
                      <span className="text-cyan-400 font-bold">•</span>
                      <span>{p}</span>
                    </div>
                  ))
                )}
              </div>
            </div>

            <div className="space-y-1.5">
              <span className="font-semibold text-slate-400 uppercase tracking-wider text-[11px] flex items-center gap-1">
                <Layers className="w-3.5 h-3.5 text-indigo-400" /> Datos Requeridos
              </span>
              <div className="p-3 rounded-xl bg-slate-800/60 border border-slate-800 space-y-1 text-slate-300 font-mono text-[11px]">
                {Object.keys(testCase.required_data).length === 0 ? (
                  <span className="text-slate-500 italic">No requiere datos específicos.</span>
                ) : (
                  Object.entries(testCase.required_data).map(([k, v]) => (
                    <div key={k} className="flex items-center justify-between">
                      <span className="text-slate-400">{k}:</span>
                      <span className="text-cyan-300 font-semibold">{v}</span>
                    </div>
                  ))
                )}
              </div>
            </div>
          </div>

          {/* Steps */}
          <div className="space-y-1.5">
            <span className="font-semibold text-slate-400 uppercase tracking-wider text-[11px] flex items-center gap-1">
              <ListOrdered className="w-3.5 h-3.5 text-cyan-400" /> Pasos de Ejecución
            </span>
            <div className="p-3.5 rounded-xl bg-slate-800/60 border border-slate-800 space-y-2 text-slate-200">
              {testCase.steps.map((step, idx) => (
                <div key={idx} className="flex items-start gap-2">
                  <span className="text-slate-400">{step}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Expected Result */}
          <div className="space-y-1.5">
            <span className="font-semibold text-slate-400 uppercase tracking-wider text-[11px] flex items-center gap-1">
              <FileText className="w-3.5 h-3.5 text-emerald-400" /> Resultado Esperado
            </span>
            <div className="p-3.5 rounded-xl bg-emerald-950/20 border border-emerald-800/40 text-emerald-200 leading-relaxed font-medium">
              {testCase.expected_result}
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="p-4 border-t border-slate-800 bg-slate-950 flex justify-end">
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
