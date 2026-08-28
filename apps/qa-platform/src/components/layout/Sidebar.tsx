import React from 'react';
import { ModuleId } from '../../types/navigation';
import {
  LayoutDashboard,
  FileSpreadsheet,
  FileCheck2,
  Database,
  PlayCircle,
  BarChart3,
  Bug,
  Settings,
  Sparkles,
} from 'lucide-react';

interface SidebarProps {
  currentModule: ModuleId;
  onNavigate: (module: ModuleId) => void;
}

export const Sidebar: React.FC<SidebarProps> = ({ currentModule, onNavigate }) => {
  const menuItems: { id: ModuleId; label: string; icon: React.ElementType; status: string; active: boolean }[] = [
    { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard, status: 'Activo', active: true },
    { id: 'backlog', label: 'Backlog Review', icon: FileSpreadsheet, status: 'Activo', active: true },
    { id: 'test-cases', label: 'Test Cases', icon: FileCheck2, status: 'Activo', active: true },
    { id: 'test-data', label: 'Test Data', icon: Database, status: 'Próximamente', active: false },
    { id: 'execution', label: 'Ejecución', icon: PlayCircle, status: 'Próximamente', active: false },
    { id: 'results', label: 'Resultados', icon: BarChart3, status: 'Próximamente', active: false },
    { id: 'bugs', label: 'Bugs', icon: Bug, status: 'Próximamente', active: false },
    { id: 'configuration', label: 'Configuración', icon: Settings, status: 'Próximamente', active: false },
  ];

  return (
    <aside className="w-64 bg-slate-900/95 border-r border-slate-800/80 flex flex-col justify-between p-4 shrink-0 min-h-screen">
      <div>
        {/* Brand */}
        <div
          onClick={() => onNavigate('dashboard')}
          className="flex items-center gap-3 px-2 py-3 mb-6 cursor-pointer group"
        >
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-cyan-500 to-indigo-600 flex items-center justify-center shadow-lg shadow-cyan-500/20 group-hover:scale-105 transition-transform">
            <Sparkles className="w-5 h-5 text-white" />
          </div>
          <div>
            <h1 className="font-bold text-sm tracking-tight text-white flex items-center gap-1.5">
              AI-QA Agents
            </h1>
            <span className="text-[10px] font-semibold tracking-wider text-cyan-400 uppercase">
              Automation Platform
            </span>
          </div>
        </div>

        {/* Navigation Menu */}
        <nav className="space-y-1">
          {menuItems.map((item) => {
            const Icon = item.icon;
            const isSelected = currentModule === item.id;
            return (
              <button
                key={item.id}
                onClick={() => onNavigate(item.id)}
                className={`w-full flex items-center justify-between px-3 py-2.5 rounded-xl text-xs font-medium transition-all text-left ${
                  isSelected
                    ? 'bg-cyan-500/10 text-cyan-300 border border-cyan-500/30 shadow-sm'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50'
                }`}
              >
                <div className="flex items-center gap-2.5">
                  <Icon className={`w-4 h-4 ${isSelected ? 'text-cyan-400' : 'text-slate-400'}`} />
                  <span>{item.label}</span>
                </div>
                {!item.active && (
                  <span className="text-[9px] px-1.5 py-0.5 rounded bg-slate-800 text-slate-400 font-mono">
                    Próx.
                  </span>
                )}
                {isSelected && (
                  <span className="w-1.5 h-1.5 rounded-full bg-cyan-400 shadow-sm shadow-cyan-400" />
                )}
              </button>
            );
          })}
        </nav>
      </div>

      {/* Footer Info */}
      <div className="p-3.5 rounded-xl bg-slate-800/40 border border-slate-800 text-[11px] text-slate-400 space-y-1.5">
        <div className="flex items-center justify-between">
          <span className="font-semibold text-slate-300">AI-QA Platform</span>
          <span className="text-[10px] font-mono text-cyan-400 bg-cyan-950/60 px-1.5 py-0.5 rounded border border-cyan-800/50">v1.0</span>
        </div>
        <p className="text-[10px] text-slate-400 leading-relaxed">
          Plataforma unificada para agentes autónomos de QA.
        </p>
      </div>
    </aside>
  );
};
