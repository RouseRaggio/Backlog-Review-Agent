import React, { useState, useMemo } from 'react';
import { TestCaseDTO } from '../types/api';
import {
  Search,
  Filter,
  Eye,
  Copy,
  Check,
  Download,
  CheckCircle2,
  XCircle,
  AlertTriangle,
  Maximize2,
  FileCode2,
} from 'lucide-react';

interface TestCasesTableProps {
  testCases: TestCaseDTO[];
  onSelectTestCase: (tc: TestCaseDTO) => void;
}

export const TestCasesTable: React.FC<TestCasesTableProps> = ({
  testCases,
  onSelectTestCase,
}) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedType, setSelectedType] = useState<string>('ALL');
  const [selectedPriority, setSelectedPriority] = useState<string>('ALL');
  const [selectedStatus, setSelectedStatus] = useState<string>('ALL');
  const [copiedId, setCopiedId] = useState<string | null>(null);

  // Filtered test cases
  const filteredCases = useMemo(() => {
    return testCases.filter((tc) => {
      if (searchTerm.trim()) {
        const query = searchTerm.trim().toLowerCase();
        const matchesId = tc.id.toLowerCase().includes(query);
        const matchesTitle = tc.title.toLowerCase().includes(query);
        const matchesAc = (tc.acceptance_criteria_reference || '').toLowerCase().includes(query);
        if (!matchesId && !matchesTitle && !matchesAc) return false;
      }
      if (selectedType !== 'ALL' && tc.type !== selectedType) return false;
      if (selectedPriority !== 'ALL' && tc.priority !== selectedPriority) return false;
      if (selectedStatus !== 'ALL' && tc.status !== selectedStatus) return false;
      return true;
    });
  }, [testCases, searchTerm, selectedType, selectedPriority, selectedStatus]);

  const handleCopyTestCase = (tc: TestCaseDTO, e: React.MouseEvent) => {
    e.stopPropagation();
    const formatted = `=== ${tc.id}: ${tc.title} ===
Tipo: ${tc.type} | Prioridad: ${tc.priority} | Estado: ${tc.status}
Criterio: ${tc.acceptance_criteria_reference || 'USER_STORY'} (Requisito: ${tc.requirement_reference})
Confianza: ${tc.confidence}

Precondiciones:
${tc.preconditions.map((p) => `- ${p}`).join('\n')}

Datos requeridos:
${Object.entries(tc.required_data).map(([k, v]) => `- ${k}: ${v}`).join('\n')}

Pasos:
${tc.steps.join('\n')}

Resultado Esperado:
${tc.expected_result}`;

    navigator.clipboard.writeText(formatted);
    setCopiedId(tc.id);
    setTimeout(() => setCopiedId(null), 2500);
  };

  const handleExportJSON = () => {
    const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(testCases, null, 2));
    const downloadAnchor = document.createElement('a');
    downloadAnchor.setAttribute("href", dataStr);
    downloadAnchor.setAttribute("download", "test_cases.json");
    document.body.appendChild(downloadAnchor);
    downloadAnchor.click();
    downloadAnchor.remove();
  };

  const renderTypeBadge = (type: string) => {
    switch (type) {
      case 'POSITIVE':
        return (
          <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[11px] font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
            <CheckCircle2 className="w-3 h-3" /> POSITIVO
          </span>
        );
      case 'NEGATIVE':
        return (
          <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[11px] font-semibold bg-rose-500/10 text-rose-400 border border-rose-500/20">
            <XCircle className="w-3 h-3" /> NEGATIVO
          </span>
        );
      case 'VALIDATION':
        return (
          <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[11px] font-semibold bg-amber-500/10 text-amber-400 border border-amber-500/20">
            <AlertTriangle className="w-3 h-3" /> VALIDACIÓN
          </span>
        );
      case 'BOUNDARY':
        return (
          <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[11px] font-semibold bg-purple-500/10 text-purple-400 border border-purple-500/20">
            <Maximize2 className="w-3 h-3" /> LÍMITE
          </span>
        );
      default:
        return <span className="text-xs text-slate-400 font-mono">{type}</span>;
    }
  };

  const renderPriorityBadge = (priority: string) => {
    switch (priority) {
      case 'CRITICAL':
        return <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-rose-950 text-rose-300 border border-rose-800 uppercase">CRITICAL</span>;
      case 'HIGH':
        return <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-orange-950 text-orange-300 border border-orange-800 uppercase">HIGH</span>;
      case 'MEDIUM':
        return <span className="px-2 py-0.5 rounded text-[10px] font-semibold bg-amber-950 text-amber-300 border border-amber-800 uppercase">MEDIUM</span>;
      case 'LOW':
        return <span className="px-2 py-0.5 rounded text-[10px] font-medium bg-slate-800 text-slate-300 border border-slate-700 uppercase">LOW</span>;
      default:
        return <span className="text-xs text-slate-400">{priority}</span>;
    }
  };

  return (
    <div className="bg-slate-900/90 border border-slate-800 rounded-2xl overflow-hidden backdrop-blur shadow-xl">
      {/* Table Header Controls */}
      <div className="p-4 border-b border-slate-800 space-y-3">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div className="flex items-center gap-2">
            <h3 className="text-sm font-semibold text-white uppercase tracking-wider">
              Casos de Prueba Generados
            </h3>
            <span className="text-xs font-semibold px-2 py-0.5 rounded-full bg-cyan-500/10 text-cyan-400 border border-cyan-500/20 font-mono">
              {filteredCases.length} de {testCases.length}
            </span>
          </div>

          <div className="flex items-center gap-2">
            {/* Search Input */}
            <div className="relative w-full sm:w-64">
              <Search className="absolute left-3 top-2.5 w-3.5 h-3.5 text-slate-400" />
              <input
                type="text"
                placeholder="Buscar por ID, título o criterio..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-8 pr-3 py-1.5 bg-slate-950 border border-slate-800 rounded-lg text-xs text-white placeholder-slate-500 focus:outline-none focus:ring-1 focus:ring-cyan-500"
              />
            </div>

            {/* Export JSON Button */}
            <button
              onClick={handleExportJSON}
              className="inline-flex items-center gap-1.5 px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-medium rounded-lg border border-slate-700 transition-all shrink-0"
              title="Exportar casos en formato JSON"
            >
              <Download className="w-3.5 h-3.5" />
              <span>Exportar JSON</span>
            </button>
          </div>
        </div>

        {/* Filter Dropdowns */}
        <div className="flex flex-wrap items-center gap-2 text-xs">
          <div className="flex items-center gap-1 text-slate-400 font-medium mr-2">
            <Filter className="w-3 h-3" />
            <span>Filtros:</span>
          </div>

          <select
            value={selectedType}
            onChange={(e) => setSelectedType(e.target.value)}
            className="px-2.5 py-1 bg-slate-950 border border-slate-800 rounded-lg text-slate-200 focus:outline-none focus:ring-1 focus:ring-cyan-500"
          >
            <option value="ALL">Todos los Tipos</option>
            <option value="POSITIVE">POSITIVO</option>
            <option value="NEGATIVE">NEGATIVO</option>
            <option value="VALIDATION">VALIDACIÓN</option>
            <option value="BOUNDARY">LÍMITE</option>
          </select>

          <select
            value={selectedPriority}
            onChange={(e) => setSelectedPriority(e.target.value)}
            className="px-2.5 py-1 bg-slate-950 border border-slate-800 rounded-lg text-slate-200 focus:outline-none focus:ring-1 focus:ring-cyan-500"
          >
            <option value="ALL">Todas las Prioridades</option>
            <option value="CRITICAL">CRITICAL</option>
            <option value="HIGH">HIGH</option>
            <option value="MEDIUM">MEDIUM</option>
            <option value="LOW">LOW</option>
          </select>

          <select
            value={selectedStatus}
            onChange={(e) => setSelectedStatus(e.target.value)}
            className="px-2.5 py-1 bg-slate-950 border border-slate-800 rounded-lg text-slate-200 focus:outline-none focus:ring-1 focus:ring-cyan-500"
          >
            <option value="ALL">Todos los Estados</option>
            <option value="READY">READY</option>
            <option value="REVIEW_REQUIRED">REVIEW_REQUIRED</option>
            <option value="NEW">NEW</option>
          </select>

          {(selectedType !== 'ALL' || selectedPriority !== 'ALL' || selectedStatus !== 'ALL' || searchTerm) && (
            <button
              onClick={() => {
                setSelectedType('ALL');
                setSelectedPriority('ALL');
                setSelectedStatus('ALL');
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
              <th className="py-3 px-4">ID</th>
              <th className="py-3 px-4">Título</th>
              <th className="py-3 px-3">Tipo</th>
              <th className="py-3 px-3">Prioridad</th>
              <th className="py-3 px-3">Criterio</th>
              <th className="py-3 px-3">Estado</th>
              <th className="py-3 px-3 text-right">Acciones</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/80 font-normal">
            {filteredCases.length === 0 ? (
              <tr>
                <td colSpan={7} className="py-12 text-center text-slate-500">
                  <FileCode2 className="w-8 h-8 mx-auto mb-2 opacity-50 text-cyan-400" />
                  <span>No se encontraron casos de prueba con los filtros aplicados.</span>
                </td>
              </tr>
            ) : (
              filteredCases.map((tc) => (
                <tr
                  key={tc.id}
                  onClick={() => onSelectTestCase(tc)}
                  className="hover:bg-slate-800/40 cursor-pointer transition-colors group"
                >
                  <td className="py-3 px-4 font-mono font-bold text-cyan-300 whitespace-nowrap">
                    {tc.id}
                  </td>
                  <td className="py-3 px-4 font-medium text-slate-200 max-w-sm truncate">
                    {tc.title}
                  </td>
                  <td className="py-3 px-3 whitespace-nowrap">{renderTypeBadge(tc.type)}</td>
                  <td className="py-3 px-3 whitespace-nowrap">{renderPriorityBadge(tc.priority)}</td>
                  <td className="py-3 px-3 whitespace-nowrap">
                    <span className="px-2 py-0.5 rounded bg-slate-800 text-slate-300 font-mono text-[11px]">
                      {tc.acceptance_criteria_reference || 'USER_STORY'}
                    </span>
                  </td>
                  <td className="py-3 px-3 whitespace-nowrap">
                    <span className={`text-[10px] font-semibold px-2 py-0.5 rounded ${
                      tc.status === 'READY' ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20' : 'bg-amber-500/10 text-amber-400 border border-amber-500/20'
                    }`}>
                      {tc.status}
                    </span>
                  </td>
                  <td className="py-3 px-3 text-right whitespace-nowrap">
                    <div className="flex items-center justify-end gap-1.5">
                      <button
                        onClick={(e) => handleCopyTestCase(tc, e)}
                        className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-700/60 transition-colors"
                        title="Copiar caso de prueba"
                      >
                        {copiedId === tc.id ? (
                          <Check className="w-3.5 h-3.5 text-emerald-400" />
                        ) : (
                          <Copy className="w-3.5 h-3.5" />
                        )}
                      </button>
                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          onSelectTestCase(tc);
                        }}
                        className="p-1.5 rounded-lg text-slate-400 hover:text-cyan-300 hover:bg-slate-700/60 transition-colors"
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
