import React from 'react';
import { ModuleId } from '../../types/navigation';
import {
  FileSpreadsheet,
  FileCheck2,
  Database,
  PlayCircle,
  BarChart3,
  Bug,
  ArrowRight,
  RefreshCw,
  Layers,
  Activity,
} from 'lucide-react';


interface DashboardModuleProps {
  backlogOnline: boolean;
  testCaseOnline: boolean;
  isCheckingHealth: boolean;
  onRefreshHealth: () => void;
  onNavigate: (module: ModuleId) => void;
}

export const DashboardModule: React.FC<DashboardModuleProps> = ({
  backlogOnline,
  testCaseOnline,
  isCheckingHealth,
  onRefreshHealth,
  onNavigate,
}) => {
  const agents = [
    {
      id: 'backlog' as ModuleId,
      name: 'Backlog Review Agent',
      port: ':8000',
      description: 'Auditoría automática de calidad de requerimientos en Jira, cálculo del Backlog Quality Score (BQS) y detección de ambigüedades.',
      icon: FileSpreadsheet,
      online: backlogOnline,
      ready: true,
      accent: 'border-sky-500/30 hover:border-sky-500/60',
      tagColor: 'bg-sky-500/10 text-sky-400 border-sky-500/20',
    },
    {
      id: 'test-cases' as ModuleId,
      name: 'Test Case Generator Agent',
      port: ':8001',
      description: 'Generación automática, determinista y trazable de casos de prueba (positivos, negativos, validación y límites) a partir de HU y AC.',
      icon: FileCheck2,
      online: testCaseOnline,
      ready: true,
      accent: 'border-cyan-500/30 hover:border-cyan-500/60',
      tagColor: 'bg-cyan-500/10 text-cyan-400 border-cyan-500/20',
    },
    {
      id: 'test-data' as ModuleId,
      name: 'Test Data Generator Agent',
      port: 'Futuro',
      description: 'Generación sintética de datos y fixtures de prueba para alimentar los escenarios generados.',
      icon: Database,
      online: false,
      ready: false,
      accent: 'border-slate-800',
      tagColor: 'bg-indigo-500/10 text-indigo-400 border-indigo-500/20',
    },
    {
      id: 'execution' as ModuleId,
      name: 'Execution Agent',
      port: 'Futuro',
      description: 'Orquestación de ejecución de suites de prueba end-to-end en entornos de integración y staging.',
      icon: PlayCircle,
      online: false,
      ready: false,
      accent: 'border-slate-800',
      tagColor: 'bg-purple-500/10 text-purple-400 border-purple-500/20',
    },
    {
      id: 'results' as ModuleId,
      name: 'Result Analysis Agent',
      port: 'Futuro',
      description: 'Análisis inteligente de resultados, categorización de fallos y telemetría de regresiones.',
      icon: BarChart3,
      online: false,
      ready: false,
      accent: 'border-slate-800',
      tagColor: 'bg-amber-500/10 text-amber-400 border-amber-500/20',
    },
    {
      id: 'bugs' as ModuleId,
      name: 'Bug Creation Agent',
      port: 'Futuro',
      description: 'Creación automática y estructurada de tickets de error en Jira ante fallos confirmados.',
      icon: Bug,
      online: false,
      ready: false,
      accent: 'border-slate-800',
      tagColor: 'bg-rose-500/10 text-rose-400 border-rose-500/20',
    },
  ];

  return (
    <div className="max-w-7xl mx-auto space-y-8 p-6">
      {/* Welcome Banner */}
      <div className="p-6 rounded-3xl bg-gradient-to-r from-slate-900 via-slate-900/90 to-indigo-950/40 border border-slate-800 shadow-2xl relative overflow-hidden">
        <div className="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-6">
          <div className="space-y-2">
            <div className="flex items-center gap-2">
              <span className="px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-cyan-500/10 text-cyan-400 border border-cyan-500/20 uppercase tracking-wide">
                AI-QA Automation Platform
              </span>
              <span className="text-xs text-slate-400">• Ecosistema Unificado</span>
            </div>
            <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
              Centro de Control de Agentes de QA
            </h1>
            <p className="text-xs sm:text-sm text-slate-300 max-w-2xl leading-relaxed">
              Plataforma integral para auditoría de calidad de requerimientos, generación automática de casos de prueba y orquestación de aseguramiento de calidad.
            </p>
          </div>

          <div className="flex items-center gap-3">
            <button
              onClick={onRefreshHealth}
              disabled={isCheckingHealth}
              className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 hover:text-white rounded-xl text-xs font-semibold border border-slate-700 transition-all flex items-center gap-2 disabled:opacity-50"
            >
              <RefreshCw className={`w-3.5 h-3.5 text-cyan-400 ${isCheckingHealth ? 'animate-spin' : ''}`} />
              <span>Verificar Servicios</span>
            </button>
          </div>
        </div>
      </div>

      {/* Agents Status & Directory Grid */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Activity className="w-4 h-4 text-cyan-400" />
            <h2 className="text-sm font-bold text-white uppercase tracking-wider">
              Estado de los Agentes del Ecosistema
            </h2>
          </div>
          <span className="text-xs text-slate-400 font-mono">2 Activos • 4 en Roadmap</span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
          {agents.map((agent) => {
            const Icon = agent.icon;
            return (
              <div
                key={agent.id}
                onClick={() => onNavigate(agent.id)}
                className={`p-5 rounded-2xl bg-slate-900/80 border transition-all flex flex-col justify-between cursor-pointer group hover:bg-slate-800/50 hover:shadow-xl ${agent.accent}`}
              >
                <div className="space-y-3">
                  <div className="flex items-start justify-between">
                    <div className="p-2.5 rounded-xl bg-slate-800 border border-slate-700 text-cyan-400 group-hover:scale-105 transition-transform">
                      <Icon className="w-5 h-5" />
                    </div>

                    <div className="flex items-center gap-2">
                      {agent.ready ? (
                        agent.online ? (
                          <span className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-[11px] font-bold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 font-mono">
                            <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
                            Online ({agent.port})
                          </span>
                        ) : (
                          <span className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-[11px] font-bold bg-rose-500/10 text-rose-400 border border-rose-500/20 font-mono">
                            <span className="w-1.5 h-1.5 rounded-full bg-rose-400" />
                            Offline ({agent.port})
                          </span>
                        )
                      ) : (
                        <span className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-[11px] font-semibold bg-slate-800 text-slate-400 border border-slate-700 font-mono">
                          Próximamente
                        </span>
                      )}
                    </div>
                  </div>

                  <div>
                    <h3 className="text-sm font-bold text-white group-hover:text-cyan-300 transition-colors">
                      {agent.name}
                    </h3>
                    <p className="text-xs text-slate-400 mt-1 leading-relaxed line-clamp-3">
                      {agent.description}
                    </p>
                  </div>
                </div>

                <div className="pt-4 mt-4 border-t border-slate-800 flex items-center justify-between text-xs font-semibold text-cyan-400 group-hover:translate-x-1 transition-transform">
                  <span>{agent.ready ? 'Abrir Agente' : 'Ver Detalles'}</span>
                  <ArrowRight className="w-3.5 h-3.5" />
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Ecosystem Workflow Pipeline Visualization */}
      <div className="p-6 rounded-3xl bg-slate-900/80 border border-slate-800 space-y-4">
        <div className="flex items-center gap-2">
          <Layers className="w-4 h-4 text-cyan-400" />
          <h3 className="text-sm font-bold text-white uppercase tracking-wider">
            Flujo de Trabajo del Ecosistema AI-QA
          </h3>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-6 gap-3 pt-2">
          {[
            { step: '1', title: 'Backlog Review', desc: 'Auditoría y Quality Score', status: 'Activo', active: true },
            { step: '2', title: 'Test Cases', desc: 'Casos Positivos y Negativos', status: 'Activo', active: true },
            { step: '3', title: 'Test Data', desc: 'Fixtures y Datos de Prueba', status: 'Roadmap', active: false },
            { step: '4', title: 'Ejecución', desc: 'Runner E2E y API', status: 'Roadmap', active: false },
            { step: '5', title: 'Resultados', desc: 'Análisis y Diagnóstico', status: 'Roadmap', active: false },
            { step: '6', title: 'Bugs', desc: 'Creación Automática Jira', status: 'Roadmap', active: false },
          ].map((item, idx) => (
            <div
              key={idx}
              className={`p-4 rounded-xl border flex flex-col justify-between space-y-2 ${
                item.active
                  ? 'bg-slate-950/80 border-cyan-500/30 text-white'
                  : 'bg-slate-950/40 border-slate-800 text-slate-400'
              }`}
            >
              <div className="flex items-center justify-between">
                <span className="w-6 h-6 rounded-lg bg-slate-800 border border-slate-700 flex items-center justify-center font-bold text-xs font-mono text-cyan-400">
                  {item.step}
                </span>
                <span
                  className={`text-[9px] px-1.5 py-0.5 rounded font-mono font-semibold ${
                    item.active ? 'bg-cyan-500/10 text-cyan-300' : 'bg-slate-800 text-slate-400'
                  }`}
                >
                  {item.status}
                </span>
              </div>
              <div>
                <h4 className="text-xs font-bold text-slate-200">{item.title}</h4>
                <p className="text-[11px] text-slate-400 mt-0.5">{item.desc}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
