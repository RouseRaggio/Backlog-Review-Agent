import React from 'react';
import { ModuleId } from '../../types/navigation';
import { User } from 'lucide-react';


interface TopbarProps {
  currentModule: ModuleId;
  backlogOnline: boolean;
  testCaseOnline: boolean;
}

export const Topbar: React.FC<TopbarProps> = ({
  currentModule,
  backlogOnline,
  testCaseOnline,
}) => {
  const getModuleTitle = () => {
    switch (currentModule) {
      case 'dashboard':
        return 'Panel Principal & Estado del Ecosistema';
      case 'backlog':
        return 'Backlog Review Agent (Auditoría de Calidad Jira)';
      case 'test-cases':
        return 'Test Case Generator Agent (Generación de Casos de Prueba)';
      case 'test-data':
        return 'Test Data Generator Agent (Generación de Datos)';
      case 'execution':
        return 'Execution Agent (Ejecución Automatizada)';
      case 'results':
        return 'Result Analysis Agent (Análisis de Resultados)';
      case 'bugs':
        return 'Bug Creation Agent (Creación Automática de Defectos)';
      case 'configuration':
        return 'Configuración Global de la Plataforma';
    }
  };

  return (
    <header className="border-b border-slate-800/80 bg-slate-950/70 backdrop-blur sticky top-0 z-40 px-6 py-3.5 flex items-center justify-between">
      <div className="flex items-center gap-3">
        <h2 className="text-sm font-bold text-white tracking-tight">
          {getModuleTitle()}
        </h2>
      </div>

      <div className="flex items-center gap-4">
        {/* Live Service Indicator Badges */}
        <div className="hidden md:flex items-center gap-3 text-[11px] font-mono">
          <div className="flex items-center gap-1.5 px-2.5 py-1 rounded-lg bg-slate-900 border border-slate-800">
            <span
              className={`w-2 h-2 rounded-full ${
                backlogOnline ? 'bg-emerald-400 shadow-sm shadow-emerald-400' : 'bg-rose-500'
              }`}
            />
            <span className="text-slate-400">Backlog Agent :8000</span>
          </div>

          <div className="flex items-center gap-1.5 px-2.5 py-1 rounded-lg bg-slate-900 border border-slate-800">
            <span
              className={`w-2 h-2 rounded-full ${
                testCaseOnline ? 'bg-emerald-400 shadow-sm shadow-emerald-400' : 'bg-rose-500'
              }`}
            />
            <span className="text-slate-400">Test Case Agent :8001</span>
          </div>
        </div>

        {/* User Profile */}
        <div className="flex items-center gap-2 pl-3 border-l border-slate-800">
          <div className="w-8 h-8 rounded-xl bg-slate-800 border border-slate-700 flex items-center justify-center text-cyan-400">
            <User className="w-4 h-4" />
          </div>
          <div className="hidden sm:block text-left">
            <div className="text-xs font-semibold text-slate-200">QA Engineer</div>
            <div className="text-[10px] text-slate-400">AI-QA Workspace</div>
          </div>
        </div>
      </div>
    </header>
  );
};
