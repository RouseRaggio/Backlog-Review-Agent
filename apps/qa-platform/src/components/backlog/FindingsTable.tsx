import React, { useState, useMemo } from 'react';
import { FindingDTO, FindingStatus, FindingSeverity } from '../../types/backlog';
import {
  Search,
  Filter,
  CheckCircle2,
  AlertTriangle,
  XCircle,
  ShieldAlert,
  Eye,
  FileSpreadsheet,
  Sparkles,
} from 'lucide-react';

interface FindingsTableProps {
  findings: FindingDTO[];
  onSelectFinding: (finding: FindingDTO) => void;
  onGenerateTestCasesFromIssue: (issueKey: string, findingMsg: string) => void;
}

export const FindingsTable: React.FC<FindingsTableProps> = ({
  findings,
  onSelectFinding,
  onGenerateTestCasesFromIssue,
}) => {

  const [searchTerm, setSearchTerm] = useState('');
  const [selectedStatus, setSelectedStatus] = useState<string>('ALL');
  const [selectedSeverity, setSelectedSeverity] = useState<string>('ALL');
  const [selectedIssueType, setSelectedIssueType] = useState<string>('ALL');

  const filteredFindings = useMemo(() => {
    return findings.filter((f) => {
      if (searchTerm.trim()) {
        const query = searchTerm.trim().toLowerCase();
        const matchesIssue = f.issue_key.toLowerCase().includes(query);
        const matchesRule = f.rule_name.toLowerCase().includes(query) || f.rule_id.toLowerCase().includes(query);
        const matchesMsg = f.message.toLowerCase().includes(query);
        if (!matchesIssue && !matchesRule && !matchesMsg) return false;
      }
      if (selectedStatus !== 'ALL' && f.status !== selectedStatus) return false;
      if (selectedSeverity !== 'ALL' && (f.severity || 'NONE') !== selectedSeverity) return false;
      if (selectedIssueType !== 'ALL' && f.issue_type !== selectedIssueType) return false;
      return true;
    });
  }, [findings, searchTerm, selectedStatus, selectedSeverity, selectedIssueType]);

  const issueTypes = useMemo(() => {
    const types = new Set(findings.map((f) => f.issue_type));
    return Array.from(types);
  }, [findings]);

  const renderStatusBadge = (status: FindingStatus) => {
    switch (status) {
      case 'PASS':
        return (
          <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[11px] font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
            <CheckCircle2 className="w-3 h-3" /> PASS
          </span>
        );
      case 'WARNING':
        return (
          <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[11px] font-semibold bg-amber-500/10 text-amber-400 border border-amber-500/20">
            <AlertTriangle className="w-3 h-3" /> WARN
          </span>
        );
      case 'FAIL':
        return (
          <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[11px] font-semibold bg-rose-500/10 text-rose-400 border border-rose-500/20">
            <XCircle className="w-3 h-3" /> FAIL
          </span>
        );
      case 'BLOCKED':
        return (
          <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[11px] font-semibold bg-purple-500/10 text-purple-400 border border-purple-500/20">
            <ShieldAlert className="w-3 h-3" /> BLOCKED
          </span>
        );
    }
  };

  const renderSeverityBadge = (severity?: FindingSeverity | null) => {
    if (!severity) return <span className="text-slate-400 text-xs font-mono">-</span>;
    switch (severity) {
      case 'CRITICAL':
        return <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-rose-950 text-rose-300 border border-rose-800 uppercase">CRITICAL</span>;
      case 'HIGH':
        return <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-orange-950 text-orange-300 border border-orange-800 uppercase">HIGH</span>;
      case 'MEDIUM':
        return <span className="px-2 py-0.5 rounded text-[10px] font-semibold bg-amber-950 text-amber-300 border border-amber-800 uppercase">MEDIUM</span>;
      case 'LOW':
        return <span className="px-2 py-0.5 rounded text-[10px] font-medium bg-slate-800 text-slate-300 border border-slate-700 uppercase">LOW</span>;
    }
  };

  return (
    <div className="bg-slate-900/90 border border-slate-800 rounded-2xl overflow-hidden backdrop-blur shadow-xl">
      {/* Table Header Controls */}
      <div className="p-4 border-b border-slate-800 space-y-3">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div className="flex items-center gap-2">
            <h3 className="text-sm font-semibold text-white uppercase tracking-wider">
              Hallazgos de la Auditoría ({findings.length})
            </h3>
            <span className="text-xs font-semibold px-2 py-0.5 rounded-full bg-cyan-500/10 text-cyan-400 border border-cyan-500/20 font-mono">
              {filteredFindings.length} mostrados
            </span>
          </div>

          <div className="relative w-full sm:w-72">
            <Search className="absolute left-3 top-2.5 w-3.5 h-3.5 text-slate-400" />
            <input
              type="text"
              placeholder="Buscar por Issue, regla o mensaje..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-8 pr-3 py-1.5 bg-slate-950 border border-slate-800 rounded-lg text-xs text-white placeholder-slate-500 focus:outline-none focus:ring-1 focus:ring-cyan-500"
            />
          </div>
        </div>

        {/* Filter Dropdowns */}
        <div className="flex flex-wrap items-center gap-2 text-xs">
          <div className="flex items-center gap-1 text-slate-400 font-medium mr-2">
            <Filter className="w-3 h-3" />
            <span>Filtros:</span>
          </div>

          <select
            value={selectedStatus}
            onChange={(e) => setSelectedStatus(e.target.value)}
            className="px-2.5 py-1 bg-slate-950 border border-slate-800 rounded-lg text-slate-200 focus:outline-none focus:ring-1 focus:ring-cyan-500"
          >
            <option value="ALL">Todos los Estados</option>
            <option value="PASS">PASS</option>
            <option value="WARNING">WARNING</option>
            <option value="FAIL">FAIL</option>
            <option value="BLOCKED">BLOCKED</option>
          </select>

          <select
            value={selectedSeverity}
            onChange={(e) => setSelectedSeverity(e.target.value)}
            className="px-2.5 py-1 bg-slate-950 border border-slate-800 rounded-lg text-slate-200 focus:outline-none focus:ring-1 focus:ring-cyan-500"
          >
            <option value="ALL">Todas las Severidades</option>
            <option value="CRITICAL">CRITICAL</option>
            <option value="HIGH">HIGH</option>
            <option value="MEDIUM">MEDIUM</option>
            <option value="LOW">LOW</option>
          </select>

          {issueTypes.length > 0 && (
            <select
              value={selectedIssueType}
              onChange={(e) => setSelectedIssueType(e.target.value)}
              className="px-2.5 py-1 bg-slate-950 border border-slate-800 rounded-lg text-slate-200 focus:outline-none focus:ring-1 focus:ring-cyan-500"
            >
              <option value="ALL">Todos los Tipos de Issue</option>
              {issueTypes.map((type) => (
                <option key={type} value={type}>
                  {type}
                </option>
              ))}
            </select>
          )}

          {(selectedStatus !== 'ALL' || selectedSeverity !== 'ALL' || selectedIssueType !== 'ALL' || searchTerm) && (
            <button
              onClick={() => {
                setSelectedStatus('ALL');
                setSelectedSeverity('ALL');
                setSelectedIssueType('ALL');
                setSearchTerm('');
              }}
              className="text-xs text-cyan-400 hover:text-cyan-300 underline underline-offset-2 ml-auto"
            >
              Limpiar filtros
            </button>
          )}
        </div>
      </div>

      {/* Table Content */}
      <div className="overflow-x-auto max-h-[560px] overflow-y-auto">
        <table className="w-full text-left text-xs">
          <thead className="sticky top-0 bg-slate-950/95 backdrop-blur z-10 border-b border-slate-800 text-slate-400 uppercase tracking-wider font-semibold">
            <tr>
              <th className="py-3 px-4">Issue Key</th>
              <th className="py-3 px-3">Tipo</th>
              <th className="py-3 px-3">Regla</th>
              <th className="py-3 px-3">Estado</th>
              <th className="py-3 px-3">Severidad</th>
              <th className="py-3 px-4">Mensaje</th>
              <th className="py-3 px-3 text-right">Acciones</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/80 font-normal">
            {filteredFindings.length === 0 ? (
              <tr>
                <td colSpan={7} className="py-12 text-center text-slate-500">
                  <FileSpreadsheet className="w-8 h-8 mx-auto mb-2 opacity-50 text-cyan-400" />
                  <span>No se encontraron hallazgos con los filtros seleccionados.</span>
                </td>
              </tr>
            ) : (
              filteredFindings.map((finding, idx) => (
                <tr
                  key={`${finding.issue_key}-${finding.rule_id}-${idx}`}
                  onClick={() => onSelectFinding(finding)}
                  className="hover:bg-slate-800/40 cursor-pointer transition-colors group"
                >
                  <td className="py-3 px-4 font-mono font-bold text-cyan-300 whitespace-nowrap">
                    {finding.issue_key}
                  </td>
                  <td className="py-3 px-3 whitespace-nowrap">
                    <span className="px-2 py-0.5 rounded bg-slate-800 text-slate-300 font-medium text-[11px]">
                      {finding.issue_type}
                    </span>
                  </td>
                  <td className="py-3 px-3 font-medium text-slate-200 whitespace-nowrap">
                    <span className="font-mono text-cyan-400 font-semibold mr-1.5">{finding.rule_id}</span>
                    <span className="text-slate-300">{finding.rule_name}</span>
                  </td>
                  <td className="py-3 px-3 whitespace-nowrap">{renderStatusBadge(finding.status)}</td>
                  <td className="py-3 px-3 whitespace-nowrap">{renderSeverityBadge(finding.severity)}</td>
                  <td className="py-3 px-4 text-slate-300 max-w-md truncate">
                    {finding.message}
                  </td>
                  <td className="py-3 px-3 text-right whitespace-nowrap">
                    <div className="flex items-center justify-end gap-1.5">
                      {/* Inter-Agent Action: Generate Test Cases */}
                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          onGenerateTestCasesFromIssue(finding.issue_key, finding.message);
                        }}
                        className="px-2 py-1 rounded-lg bg-cyan-500/10 hover:bg-cyan-500/20 text-cyan-300 hover:text-white border border-cyan-500/30 text-[11px] font-semibold transition-all inline-flex items-center gap-1"
                        title="Generar Casos de Prueba para esta Historia de Usuario"
                      >
                        <Sparkles className="w-3 h-3 text-cyan-400" />
                        <span>🧪 Test Cases</span>
                      </button>

                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          onSelectFinding(finding);
                        }}
                        className="p-1 rounded-lg text-slate-400 hover:text-white hover:bg-slate-700/60 transition-colors"
                        title="Ver detalle"
                      >
                        <Eye className="w-3.5 h-3.5" />
                      </button>
                    </div>
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
