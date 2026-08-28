import React from 'react';
import { GenerationOptionsDTO } from '../types/api';
import { SlidersHorizontal } from 'lucide-react';

interface GenerationOptionsFormProps {
  options: GenerationOptionsDTO;
  setOptions: (opts: GenerationOptionsDTO) => void;
  disabled?: boolean;
}

export const GenerationOptionsForm: React.FC<GenerationOptionsFormProps> = ({
  options,
  setOptions,
  disabled = false,
}) => {
  return (
    <div className="space-y-3 pt-2 border-t border-slate-800/80">
      <div className="flex items-center gap-1.5 text-xs font-semibold text-slate-300 uppercase tracking-wider">
        <SlidersHorizontal className="w-3.5 h-3.5 text-cyan-400" />
        <span>Opciones de Generación</span>
      </div>

      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
        <label className="flex items-center gap-2 text-xs text-slate-300 cursor-pointer select-none">
          <input
            type="checkbox"
            checked={options.include_positive}
            onChange={(e) => setOptions({ ...options, include_positive: e.target.checked })}
            disabled={disabled}
            className="rounded border-slate-700 bg-slate-900 text-cyan-500 focus:ring-cyan-500 focus:ring-offset-slate-900"
          />
          <span>Positivos</span>
        </label>

        <label className="flex items-center gap-2 text-xs text-slate-300 cursor-pointer select-none">
          <input
            type="checkbox"
            checked={options.include_negative}
            onChange={(e) => setOptions({ ...options, include_negative: e.target.checked })}
            disabled={disabled}
            className="rounded border-slate-700 bg-slate-900 text-cyan-500 focus:ring-cyan-500 focus:ring-offset-slate-900"
          />
          <span>Negativos</span>
        </label>

        <label className="flex items-center gap-2 text-xs text-slate-300 cursor-pointer select-none">
          <input
            type="checkbox"
            checked={options.include_validation}
            onChange={(e) => setOptions({ ...options, include_validation: e.target.checked })}
            disabled={disabled}
            className="rounded border-slate-700 bg-slate-900 text-cyan-500 focus:ring-cyan-500 focus:ring-offset-slate-900"
          />
          <span>Validación</span>
        </label>

        <label className="flex items-center gap-2 text-xs text-slate-300 cursor-pointer select-none">
          <input
            type="checkbox"
            checked={options.include_boundary}
            onChange={(e) => setOptions({ ...options, include_boundary: e.target.checked })}
            disabled={disabled}
            className="rounded border-slate-700 bg-slate-900 text-cyan-500 focus:ring-cyan-500 focus:ring-offset-slate-900"
          />
          <span>Límites (Boundary)</span>
        </label>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-2">
        <div>
          <label className="block text-[11px] text-slate-400 mb-1">Nivel de detalle</label>
          <select
            value={options.detail_level}
            onChange={(e) => setOptions({ ...options, detail_level: e.target.value })}
            disabled={disabled}
            className="w-full px-2.5 py-1.5 bg-slate-900/90 border border-slate-700 rounded-lg text-xs text-slate-200 focus:outline-none focus:ring-1 focus:ring-cyan-500"
          >
            <option value="basic">Básico</option>
            <option value="standard">Estándar</option>
            <option value="detailed">Detallado</option>
          </select>
        </div>

        <div>
          <label className="block text-[11px] text-slate-400 mb-1">Prioridad mínima</label>
          <select
            value={options.min_priority}
            onChange={(e) => setOptions({ ...options, min_priority: e.target.value })}
            disabled={disabled}
            className="w-full px-2.5 py-1.5 bg-slate-900/90 border border-slate-700 rounded-lg text-xs text-slate-200 focus:outline-none focus:ring-1 focus:ring-cyan-500"
          >
            <option value="LOW">Baja (Todos los casos)</option>
            <option value="MEDIUM">Media o superior</option>
            <option value="HIGH">Alta o superior</option>
            <option value="CRITICAL">Crítica solamente</option>
          </select>
        </div>
      </div>
    </div>
  );
};
