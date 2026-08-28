import React from 'react';
import { StatisticsDTO } from '../../types/backlog';
import { CheckCircle2, AlertTriangle, XCircle, ShieldAlert, FileText, CheckCheck } from 'lucide-react';

interface StatsCardsProps {
  statistics: StatisticsDTO;
}

export const StatsCards: React.FC<StatsCardsProps> = ({ statistics }) => {
  const cards = [
    {
      title: 'Total Issues',
      value: statistics.total_issues,
      subtitle: 'Historias evaluadas',
      icon: FileText,
      color: 'text-sky-400',
      bg: 'bg-sky-500/10 border-sky-500/20',
    },
    {
      title: 'Total Findings',
      value: statistics.total_findings,
      subtitle: 'Evaluaciones de reglas',
      icon: CheckCheck,
      color: 'text-indigo-400',
      bg: 'bg-indigo-500/10 border-indigo-500/20',
    },
    {
      title: 'Reglas Aprobadas',
      value: statistics.passed,
      subtitle: 'Criterios cumplidos',
      icon: CheckCircle2,
      color: 'text-emerald-400',
      bg: 'bg-emerald-500/10 border-emerald-500/20',
    },
    {
      title: 'Advertencias',
      value: statistics.warnings,
      subtitle: 'Oportunidades de mejora',
      icon: AlertTriangle,
      color: 'text-amber-400',
      bg: 'bg-amber-500/10 border-amber-500/20',
    },
    {
      title: 'Fallos de Calidad',
      value: statistics.failed,
      subtitle: 'Reglas no satisfechas',
      icon: XCircle,
      color: 'text-rose-400',
      bg: 'bg-rose-500/10 border-rose-500/20',
    },
    {
      title: 'Bloqueos / Críticos',
      value: statistics.blocked,
      subtitle: 'Impiden refinamiento',
      icon: ShieldAlert,
      color: 'text-purple-400',
      bg: 'bg-purple-500/10 border-purple-500/20',
    },
  ];

  return (
    <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
      {cards.map((card, idx) => {
        const Icon = card.icon;
        return (
          <div
            key={idx}
            className="p-4 rounded-xl bg-slate-900/80 border border-slate-800 backdrop-blur shadow-sm flex flex-col justify-between"
          >
            <div className="flex items-center justify-between text-slate-400">
              <span className="text-xs font-medium">{card.title}</span>
              <div className={`p-1.5 rounded-lg border ${card.bg}`}>
                <Icon className={`w-3.5 h-3.5 ${card.color}`} />
              </div>
            </div>
            <div className="mt-2">
              <span className="text-2xl font-bold text-white tracking-tight">{card.value}</span>
              <p className="text-[10px] text-slate-400 mt-0.5">{card.subtitle}</p>
            </div>
          </div>
        );
      })}
    </div>
  );
};
