import React from 'react';
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

export const Sidebar: React.FC = () => {
  const menuItems = [
    { label: 'Dashboard', icon: LayoutDashboard, status: 'Próximamente', active: false },
    { label: 'Backlog', icon: FileSpreadsheet, status: 'Próximamente', active: false },
    { label: 'Test Cases', icon: FileCheck2, status: 'Activo', active: true },
    { label: 'Test Data', icon: Database, status: 'Próximamente', active: false },
    { label: 'Ejecución', icon: PlayCircle, status: 'Próximamente', active: false },
    { label: 'Resultados', icon: BarChart3, status: 'Próximamente', active: false },
    { label: 'Bugs', icon: Bug, status: 'Próximamente', active: false },
    { label: 'Configuración', icon: Settings, status: 'Próximamente', active: false },
  ];

  return (
    <aside className="w-64 bg-slate-900/90 border-r border-slate-800/80 flex flex-col justify-between p-4 shrink-0 min-h-screen">
      <div>
        {/* Brand */}
        <div className="flex items-center gap-3 px-2 py-3 mb-6">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-cyan-500 to-indigo-600 flex items-center justify-center shadow-lg shadow-cyan-500/20">
            <Sparkles className="w-5 h-5 text-white" />
          </div>
          <div>
            <h1 className="font-bold text-sm tracking-tight text-white flex items-center gap-1.5">
              AI-QA Agents
            </h1>
            <span className="text-[10px] font-semibold tracking-wider text-cyan-400 uppercase">
              Test Case Generator
            </span>
          </div>
        </div>

        {/* Navigation Menu */}
        <nav className="space-y-1">
          {menuItems.map((item) => {
            const Icon = item.icon;
            return (
              <div
                key={item.label}
                className={`flex items-center justify-between px-3 py-2.5 rounded-xl text-xs font-medium transition-all ${
                  item.active
                    ? 'bg-cyan-500/10 text-cyan-300 border border-cyan-500/30 shadow-sm'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50 cursor-pointer'
                }`}
              >
                <div className="flex items-center gap-2.5">
                  <Icon className={`w-4 h-4 ${item.active ? 'text-cyan-400' : 'text-slate-400'}`} />
                  <span>{item.label}</span>
                </div>
                {!item.active && (
                  <span className="text-[9px] px-1.5 py-0.5 rounded bg-slate-800/80 text-slate-400 font-mono">
                    {item.status}
                  </span>
                )}
                {item.active && (
                  <span className="w-1.5 h-1.5 rounded-full bg-cyan-400 shadow-sm shadow-cyan-400" />
                )}
              </div>
            );
          })}
        </nav>
      </div>

      {/* Footer Info */}
      <div className="p-3 rounded-xl bg-slate-800/40 border border-slate-800 text-[11px] text-slate-400 space-y-1">
        <div className="font-medium text-slate-300">Clean Architecture MVP</div>
        <div className="text-[10px] text-slate-400">Strict Grounding • No-Invention</div>
      </div>
    </aside>
  );
};
