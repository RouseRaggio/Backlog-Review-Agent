import React, { useState } from 'react';
import { Play, Loader2, Search } from 'lucide-react';

interface ReviewFormProps {
  onSubmit: (projectKey: string, maxResults: number) => void;
  isLoading: boolean;
  initialProject?: string;
  initialMaxResults?: number;
}

export const ReviewForm: React.FC<ReviewFormProps> = ({
  onSubmit,
  isLoading,
  initialProject = 'GESTADOC',
  initialMaxResults = 100,
}) => {
  const [projectKey, setProjectKey] = useState(initialProject);
  const [maxResults, setMaxResults] = useState(initialMaxResults);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!projectKey.trim()) {
      setError('Por favor ingresa la clave del proyecto');
      return;
    }
    if (maxResults < 1 || maxResults > 1000) {
      setError('El máximo de issues debe estar entre 1 y 1000');
      return;
    }
    setError(null);
    onSubmit(projectKey.trim().toUpperCase(), maxResults);
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="p-5 rounded-2xl bg-slate-800/80 border border-slate-700/60 backdrop-blur shadow-lg flex flex-col md:flex-row items-end gap-4"
    >
      <div className="flex-1 w-full">
        <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">
          Proyecto Jira
        </label>
        <div className="relative">
          <input
            type="text"
            value={projectKey}
            onChange={(e) => setProjectKey(e.target.value.toUpperCase())}
            placeholder="Ej. GESTADOC, CAP, CRA"
            disabled={isLoading}
            className="w-full px-4 py-2.5 bg-slate-900/90 border border-slate-700 rounded-xl text-white placeholder-slate-500 text-sm font-medium focus:outline-none focus:ring-2 focus:ring-sky-500 focus:border-sky-500 transition-all disabled:opacity-50"
          />
          <Search className="absolute right-3.5 top-3 w-4 h-4 text-slate-500 pointer-events-none" />
        </div>
      </div>

      <div className="w-full md:w-48">
        <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">
          Máximo de Issues
        </label>
        <input
          type="number"
          min={1}
          max={1000}
          value={maxResults}
          onChange={(e) => setMaxResults(Number(e.target.value))}
          disabled={isLoading}
          className="w-full px-4 py-2.5 bg-slate-900/90 border border-slate-700 rounded-xl text-white text-sm font-medium focus:outline-none focus:ring-2 focus:ring-sky-500 focus:border-sky-500 transition-all disabled:opacity-50"
        />
      </div>

      <div className="w-full md:w-auto">
        <button
          type="submit"
          disabled={isLoading}
          className="w-full md:w-auto px-6 py-2.5 bg-gradient-to-r from-sky-500 to-indigo-600 hover:from-sky-400 hover:to-indigo-500 text-white text-sm font-semibold rounded-xl shadow-md hover:shadow-sky-500/20 active:scale-[0.98] transition-all flex items-center justify-center gap-2 disabled:opacity-60 disabled:pointer-events-none"
        >
          {isLoading ? (
            <>
              <Loader2 className="w-4 h-4 animate-spin" />
              <span>Auditando Backlog...</span>
            </>
          ) : (
            <>
              <Play className="w-4 h-4 fill-white" />
              <span>Iniciar revisión</span>
            </>
          )}
        </button>
      </div>

      {error && (
        <div className="w-full text-xs text-rose-400 font-medium mt-1">
          {error}
        </div>
      )}
    </form>
  );
};
