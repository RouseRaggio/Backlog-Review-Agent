import React, { useState, useMemo } from 'react';
import { FindingDTO } from '../types/api';
import { Filter, Search, ChevronRight, AlertCircle, CheckCircle2, XCircle, AlertTriangle, ShieldAlert } from 'lucide-react';

interface FindingsTableProps {
  findings: FindingDTO[];
  onSelectFinding: (finding: FindingDTO) => void;
}

export const FindingsTable: React.FC<FindingsTableProps> = ({
  findings,
  onSelectFinding,
}) => {
  const [searchKey, setSearchKey] = useState('');
  const [selectedStatus, setSelectedStatus] = useState<string>('ALL');
  const [selectedSeverity, setSelectedSeverity] = useState<string>('ALL');
  const [selectedRule, setSelectedRule] = useState<string>('ALL');

  // Extract unique rules for filter dropdown
  const uniqueRules = useMemo(() => {
    const rulesMap = new Map<string, string>();
    findings.forEach((f) => {
      rulesMap.set(f.rule_id, f.rule_name);
    });
    return Array.from(rulesMap.entries()).map(([id, name]) => ({ id, name }));
  }, [findings]);

  // Filtered findings
  const filteredFindings = useMemo(() => {
    return findings.filter((finding) => {
      // Search by issue key
      if (searchKey.trim() && !finding.issue_key.toLowerCase().includes(searchKey.trim().toLowerCase())) {
        return false;
      }
      // Filter by status
      if (selectedStatus !== 'ALL' && finding.status !== selectedStatus) {
        return false;
      }
      // Filter by severity
      if (selectedSeverity !== 'ALL' && (finding.severity || '-') !== selectedSeverity) {
        return false;
      }
      // Filter by rule
      if (selectedRule !== 'ALL' && finding.rule_id !== selectedRule) {
        return false;
      }
      return true;
    });
  }, [findings, searchKey, selectedStatus, selectedSeverity, selectedRule]);

  const renderStatusBadge = (status: string) => {
    switch (status) {
      case 'PASS':
        return (
          <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
            <CheckCircle2 className="w-3 h-3" /> PASS
          </span>
        );
      case 'FAIL':
        return (
          <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-rose-500/10 text-rose-400 border border-rose-500/20">
            <XCircle className="w-3 h-3" /> FAIL
          </span>
        );
      case 'WARNING':
        return (
          <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-amber-500/10 text-amber-400 border border-amber-500/20">
            <AlertTriangle className="w-3 h-3" /> WARNING
          </span>
        );
      case 'BLOCKED':
        return (
          <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-purple-500/10 text-purple-400 border border-purple-500/20">
            <ShieldAlert className="w-3 h-3" /> BLOCKED
          </span>
        );
      default:
        return (
          <span className="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-slate-800 text-slate-400 border border-slate-700">
            {status}
          </span>
        );
    }
  };

  const renderSeverityBadge = (severity?: string | null) => {
    if (!severity) return <span className="text-xs text-slate-500 font-mono">-</span>;
    switch (severity.toUpperCase()) {
      case 'CRITICAL':
        return (
          <span className="px-2 py-0.5 rounded text-[11px] font-bold bg-rose-950/80 text-rose-300 border border-rose-700/60 uppercase tracking-wide">
            CRITICAL
          </span>
        );
      case 'HIGH':
        return (
          <span className="px-2 py-0.5 rounded text-[11px] font-bold bg-orange-950/80 text-orange-300 border border-orange-700/60 uppercase tracking-wide">
            HIGH
          </span>
        );
      case 'MEDIUM':
        return (
          <span className="px-2 py-0.5 rounded text-[11px] font-semibold bg-amber-950/80 text-amber-300 border border-amber-700/60 uppercase tracking-wide">
            MEDIUM
          </span>
        );
      case 'LOW':
        return (
          <span className="px-2 py-0.5 rounded text-[11px] font-medium bg-slate-800 text-slate-300 border border-slate-700 uppercase tracking-wide">
            LOW
          </span>
        );
      default:
        return <span className="text-xs text-slate-400 font-medium">{severity}</span>;
    }
  };

  return (
    <div className="bg-slate-800/80 border border-slate-700/60 rounded-2xl overflow-hidden backdrop-blur shadow-xl">
      {/* Header with Filters */}
      <div className="p-4 border-b border-slate-700/70 space-y-3">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div className="flex items-center gap-2">
            <h3 className="text-sm font-semibold text-white uppercase tracking-wider">
              Findings de Auditoría
            </h3>
            <span className="text-xs font-semibold px-2 py-0.5 rounded-full bg-slate-700 text-sky-400">
              {filteredFindings.length} de {findings.length}
            </span>
          </div>

          {/* Search Box */}
          <div className="relative w-full sm:w-64">
            <Search className="absolute left-3 top-2.5 w-4 h-4 text-slate-400" />
            <input
              type="text"
              placeholder="Buscar por Issue Key..."
              value={searchKey}
              onChange={(e) => setSearchKey(e.target.value)}
              className="w-full pl-9 pr-4 py-1.5 bg-slate-900/90 border border-slate-700 rounded-lg text-xs text-white placeholder-slate-500 focus:outline-none focus:ring-1 focus:ring-sky-500"
            />
          </div>
        </div>

        {/* Filter Controls */}
        <div className="flex flex-wrap items-center gap-2 pt-1 text-xs">
          <div className="flex items-center gap-1.5 text-slate-400 mr-2 font-medium">
            <Filter className="w-3.5 h-3.5" />
            <span>Filtros:</span>
          </div>

          {/* Status Filter */}
          <select
            value={selectedStatus}
            onChange={(e) => setSelectedStatus(e.target.value)}
            className="px-2.5 py-1.5 bg-slate-900/90 border border-slate-700 rounded-lg text-slate-200 focus:outline-none focus:ring-1 focus:ring-sky-500"
          >
            <option value="ALL">Todos los Estados</option>
            <option value="PASS">PASS</option>
            <option value="FAIL">FAIL</option>
            <option value="WARNING">WARNING</option>
            <option value="BLOCKED">BLOCKED</option>
          </select>

          {/* Severity Filter */}
          <select
            value={selectedSeverity}
            onChange={(e) => setSelectedSeverity(e.target.value)}
            className="px-2.5 py-1.5 bg-slate-900/90 border border-slate-700 rounded-lg text-slate-200 focus:outline-none focus:ring-1 focus:ring-sky-500"
          >
            <option value="ALL">Todas las Severidades</option>
            <option value="CRITICAL">CRITICAL</option>
            <option value="HIGH">HIGH</option>
            <option value="MEDIUM">MEDIUM</option>
            <option value="LOW">LOW</option>
          </select>

          {/* Rule Filter */}
          <select
            value={selectedRule}
            onChange={(e) => setSelectedRule(e.target.value)}
            className="px-2.5 py-1.5 bg-slate-900/90 border border-slate-700 rounded-lg text-slate-200 max-w-xs truncate focus:outline-none focus:ring-1 focus:ring-sky-500"
          >
            <option value="ALL">Todas las Reglas</option>
            {uniqueRules.map((rule) => (
              <option key={rule.id} value={rule.id}>
                {rule.id} - {rule.name}
              </option>
            ))}
          </select>

          {(selectedStatus !== 'ALL' || selectedSeverity !== 'ALL' || selectedRule !== 'ALL' || searchKey) && (
            <button
              onClick={() => {
                setSelectedStatus('ALL');
                setSelectedSeverity('ALL');
                setSelectedRule('ALL');
                setSearchKey('');
              }}
              className="text-xs text-sky-400 hover:text-sky-300 underline underline-offset-2 ml-auto"
            >
              Limpiar filtros
            </button>
          )}
        </div>
      </div>

      {/* Table Content */}
      <div className="overflow-x-auto max-h-[580px] overflow-y-auto">
        <table className="w-full text-left text-xs">
          <thead className="sticky top-0 bg-slate-900/95 backdrop-blur z-10 border-b border-slate-700 text-slate-400 uppercase tracking-wider font-semibold">
            <tr>
              <th className="py-3 px-4">Issue</th>
              <th className="py-3 px-3">Tipo</th>
              <th className="py-3 px-3">Estado</th>
              <th className="py-3 px-3">Severidad</th>
              <th className="py-3 px-4">Regla</th>
              <th className="py-3 px-4">Mensaje</th>
              <th className="py-3 px-4">Recomendación</th>
              <th className="py-3 px-3 text-center">Acción</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/80 font-normal">
            {filteredFindings.length === 0 ? (
              <tr>
                <td colSpan={8} className="py-12 text-center text-slate-500">
                  <AlertCircle className="w-8 h-8 mx-auto mb-2 opacity-50" />
                  <span>No se encontraron findings con los filtros aplicados.</span>
                </td>
              </tr>
            ) : (
              filteredFindings.map((finding, idx) => (
                <tr
                  key={`${finding.issue_key}-${finding.rule_id}-${idx}`}
                  onClick={() => onSelectFinding(finding)}
                  className="hover:bg-slate-700/40 cursor-pointer transition-colors group"
                >
                  <td className="py-3 px-4 font-mono font-semibold text-sky-300">
                    {finding.issue_key}
                  </td>
                  <td className="py-3 px-3">
                    <span className="px-2 py-0.5 rounded bg-slate-700/60 text-slate-300 font-medium">
                      {finding.issue_type}
                    </span>
                  </td>
                  <td className="py-3 px-3">{renderStatusBadge(finding.status)}</td>
                  <td className="py-3 px-3">{renderSeverityBadge(finding.severity)}</td>
                  <td className="py-3 px-4">
                    <div className="font-semibold text-slate-200">{finding.rule_id}</div>
                    <div className="text-[11px] text-slate-400">{finding.rule_name}</div>
                  </td>
                  <td className="py-3 px-4 max-w-xs truncate text-slate-300">
                    {finding.message}
                  </td>
                  <td className="py-3 px-4 max-w-xs truncate text-slate-400">
                    {finding.recommendation || '-'}
                  </td>
                  <td className="py-3 px-3 text-center text-slate-500 group-hover:text-sky-400">
                    <ChevronRight className="w-4 h-4 mx-auto transition-transform group-hover:translate-x-0.5" />
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};
