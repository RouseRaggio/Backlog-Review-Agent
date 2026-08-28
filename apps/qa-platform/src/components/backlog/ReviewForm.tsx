import React, { useState } from 'react';
import { Search, Sparkles, Loader2, FolderGit2, Hash } from 'lucide-react';

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

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!projectKey.trim() || isLoading) return;
    onSubmit(projectKey.trim().toUpperCase(), maxResults);
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="p-5 rounded-2xl bg-slate-900/80 border border-slate-800 backdrop-blur shadow-xl space-y-4"
    >
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <FolderGit2 className="w-4 h-4 text-sky-400" />
          <h3 className="text-sm font-semibold text-white uppercase tracking-wider">
            Auditar Proyecto Jira
          </h3>
        </div>
        <span className="text-[10px] font-mono text-slate-400 bg-slate-800 px-2 py-0.5 rounded border border-slate-700">
          Clean Architecture
        </span>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 items-end">
        <div className="sm:col-span-2">
          <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">
            Clave del Proyecto Jira
          </label>
          <div className="relative">
            <Search className="absolute left-3.5 top-2.5 w-4 h-4 text-slate-400" />
            <input
              type="text"
              value={projectKey}
              onChange={(e) => setProjectKey(e.target.value.toUpperCase())}
              placeholder="Ej: GESTADOC, GES, CAP"
              disabled={isLoading}
              className="w-full pl-10 pr-4 py-2 bg-slate-950 border border-slate-700/80 rounded-xl text-white placeholder-slate-500 text-xs font-mono font-medium focus:outline-none focus:ring-1 focus:ring-sky-500 focus:border-sky-500 transition-all disabled:opacity-50"
            />
          </div>
        </div>

        <div>
          <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2 flex items-center gap-1">
            <Hash className="w-3.5 h-3.5 text-sky-400" /> Máximo de Issues
          </label>
          <input
            type="number"
            min={1}
            max={500}
            value={maxResults}
            onChange={(e) => setMaxResults(Math.max(1, parseInt(e.target.value) || 1))}
            disabled={isLoading}
            className="w-full px-3.5 py-2 bg-slate-950 border border-slate-700/80 rounded-xl text-white placeholder-slate-500 text-xs font-mono font-medium focus:outline-none focus:ring-1 focus:ring-sky-500 focus:border-sky-500 transition-all disabled:opacity-50"
          />
        </div>
      </div>

      <div className="flex justify-end pt-1">
        <button
          type="submit"
          disabled={isLoading || !projectKey.trim()}
          className="px-6 py-2.5 bg-gradient-to-r from-sky-500 to-indigo-600 hover:from-sky-400 hover:to-indigo-500 text-white text-xs font-semibold rounded-xl shadow-lg shadow-sky-500/20 active:scale-[0.98] transition-all flex items-center justify-center gap-2 disabled:opacity-60 disabled:pointer-events-none"
        >
          {isLoading ? (
            <>
              <Loader2 className="w-4 h-4 animate-spin" />
              <span>Auditando Backlog...</span>
            </>
          ) : (
            <>
              <Sparkles className="w-4 h-4 fill-white" />
              <span>Iniciar Auditoría</span>
            </>
          )}
        </button>
      </div>
    </form>
  );
};
