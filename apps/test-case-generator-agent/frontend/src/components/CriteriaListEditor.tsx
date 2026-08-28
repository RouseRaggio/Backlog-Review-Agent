import React from 'react';
import { CriterionDTO } from '../types/api';
import { Plus, Trash2, CheckSquare } from 'lucide-react';

interface CriteriaListEditorProps {
  criteria: CriterionDTO[];
  setCriteria: (criteria: CriterionDTO[]) => void;
  disabled?: boolean;
}

export const CriteriaListEditor: React.FC<CriteriaListEditorProps> = ({
  criteria,
  setCriteria,
  disabled = false,
}) => {
  const handleAddCriterion = () => {
    const nextNum = criteria.length + 1;
    const nextId = `AC-${nextNum.toString().padStart(3, '0')}`;
    setCriteria([...criteria, { id: nextId, description: '' }]);
  };

  const handleUpdateCriterion = (index: number, description: string) => {
    const updated = [...criteria];
    updated[index] = { ...updated[index], description };
    setCriteria(updated);
  };

  const handleRemoveCriterion = (index: number) => {
    const updated = criteria.filter((_, i) => i !== index);
    // Renumerar IDs
    const reindexed = updated.map((c, i) => ({
      ...c,
      id: `AC-${(i + 1).toString().padStart(3, '0')}`,
    }));
    setCriteria(reindexed);
  };

  return (
    <div className="space-y-3">
      <div className="flex items-center justify-between">
        <label className="flex items-center gap-1.5 text-xs font-semibold text-slate-300 uppercase tracking-wider">
          <CheckSquare className="w-3.5 h-3.5 text-cyan-400" />
          <span>Criterios de Aceptación ({criteria.length})</span>
        </label>
        <button
          type="button"
          onClick={handleAddCriterion}
          disabled={disabled}
          className="inline-flex items-center gap-1 px-2.5 py-1 rounded-lg bg-cyan-500/10 hover:bg-cyan-500/20 text-cyan-400 border border-cyan-500/30 text-xs font-medium transition-all disabled:opacity-50"
        >
          <Plus className="w-3.5 h-3.5" />
          <span>Agregar criterio</span>
        </button>
      </div>

      {criteria.length === 0 ? (
        <div className="p-4 rounded-xl border border-dashed border-slate-800 bg-slate-900/40 text-center text-xs text-slate-500">
          No has agregado criterios de aceptación. Puedes agregarlos para obtener casos de prueba con mayor nivel de confianza y trazabilidad.
        </div>
      ) : (
        <div className="space-y-2 max-h-56 overflow-y-auto pr-1">
          {criteria.map((c, idx) => (
            <div
              key={c.id}
              className="flex items-center gap-2 p-2 rounded-xl bg-slate-900/80 border border-slate-800 focus-within:border-cyan-500/50 transition-all"
            >
              <span className="px-2 py-1 rounded-md bg-slate-800 text-cyan-300 font-mono text-[11px] font-semibold shrink-0">
                {c.id}
              </span>
              <input
                type="text"
                value={c.description}
                onChange={(e) => handleUpdateCriterion(idx, e.target.value)}
                placeholder="Descripción explícita del criterio..."
                disabled={disabled}
                className="flex-1 bg-transparent border-0 text-xs text-slate-200 placeholder-slate-500 focus:outline-none"
              />
              <button
                type="button"
                onClick={() => handleRemoveCriterion(idx)}
                disabled={disabled}
                className="p-1 text-slate-500 hover:text-rose-400 rounded-lg hover:bg-slate-800 transition-colors"
                title="Eliminar criterio"
              >
                <Trash2 className="w-3.5 h-3.5" />
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
