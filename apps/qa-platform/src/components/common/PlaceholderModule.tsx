import React from 'react';
import { Sparkles, Clock, ArrowRight } from 'lucide-react';
import { ModuleId } from '../../types/navigation';

interface PlaceholderModuleProps {
  moduleId: ModuleId;
  onNavigate: (module: ModuleId) => void;
}

export const PlaceholderModule: React.FC<PlaceholderModuleProps> = ({
  moduleId,
  onNavigate,
}) => {
  const getModuleDetails = () => {
    switch (moduleId) {
      case 'test-data':
        return {
          title: 'Test Data Generator Agent',
          description: 'Generación inteligente y sintética de datos de prueba válidos, inválidos y casos de borde para alimentar los casos de prueba.',
          pipelineStep: 'Paso 3 del flujo de automatización',
          iconColor: 'text-indigo-400',
        };
      case 'execution':
        return {
          title: 'Execution Agent',
          description: 'Orquestador de ejecución automatizada de pruebas end-to-end, API y pruebas de integración sobre entornos de QA.',
          pipelineStep: 'Paso 4 del flujo de automatización',
          iconColor: 'text-purple-400',
        };
      case 'results':
        return {
          title: 'Result Analysis Agent',
          description: 'Análisis automatizado de logs, screenshots y métricas de fallos tras la ejecución de pruebas con diagnóstico de causas raíz.',
          pipelineStep: 'Paso 5 del flujo de automatización',
          iconColor: 'text-amber-400',
        };
      case 'bugs':
        return {
          title: 'Bug Creation Agent',
          description: 'Creación automática y estructurada de defectos en Jira con pasos de reproducción precisos, severidad y evidencias.',
          pipelineStep: 'Paso 6 del flujo de automatización',
          iconColor: 'text-rose-400',
        };
      case 'configuration':
        return {
          title: 'Configuración de la Plataforma',
          description: 'Administración de conexiones con Jira, modelos de IA (OpenAI, Claude, Ollama), perfiles de usuario y políticas de calidad.',
          pipelineStep: 'Ajustes globales del ecosistema',
          iconColor: 'text-cyan-400',
        };
      default:
        return {
          title: 'Módulo en Desarrollo',
          description: 'Este módulo estará disponible en próximas actualizaciones del ecosistema AI-QA-Agents.',
          pipelineStep: 'Ecosistema QA',
          iconColor: 'text-cyan-400',
        };
    }
  };

  const details = getModuleDetails();

  return (
    <div className="max-w-4xl mx-auto py-12 px-4 space-y-6">
      <div className="p-8 rounded-3xl bg-slate-900/80 border border-slate-800 backdrop-blur text-center space-y-6 shadow-xl">
        <div className="inline-flex p-4 rounded-2xl bg-slate-800/80 border border-slate-700 text-cyan-400">
          <Clock className={`w-10 h-10 ${details.iconColor}`} />
        </div>

        <div className="space-y-2 max-w-lg mx-auto">
          <span className="inline-block px-3 py-1 rounded-full text-[10px] font-bold bg-amber-500/10 text-amber-400 border border-amber-500/20 uppercase tracking-wide">
            Próximamente en el Ecosistema
          </span>
          <h2 className="text-xl font-bold text-white tracking-tight">{details.title}</h2>
          <p className="text-xs text-slate-400 leading-relaxed">{details.description}</p>
        </div>

        <div className="p-4 rounded-2xl bg-slate-950/60 border border-slate-800 max-w-md mx-auto text-left text-xs space-y-2">
          <div className="flex items-center gap-2 text-slate-300 font-semibold">
            <Sparkles className="w-4 h-4 text-cyan-400" />
            <span>{details.pipelineStep}</span>
          </div>
          <p className="text-slate-400 text-[11px] leading-relaxed">
            La arquitectura de este agente se encuentra en la hoja de ruta para integrarse de forma modular y sin acoplamiento a la plataforma.
          </p>
        </div>

        <div className="flex flex-wrap items-center justify-center gap-3 pt-2">
          <button
            onClick={() => onNavigate('backlog')}
            className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 hover:text-white rounded-xl text-xs font-semibold border border-slate-700 transition-colors inline-flex items-center gap-1.5"
          >
            <span>Ir a Backlog Review</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </button>
          <button
            onClick={() => onNavigate('test-cases')}
            className="px-4 py-2 bg-cyan-500/10 hover:bg-cyan-500/20 text-cyan-300 rounded-xl text-xs font-semibold border border-cyan-500/30 transition-colors inline-flex items-center gap-1.5"
          >
            <span>Ir a Test Case Generator</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </button>
        </div>
      </div>
    </div>
  );
};
