import { useState, useEffect } from 'react';
import { StoryInputForm } from './StoryInputForm';
import { CriteriaListEditor } from './CriteriaListEditor';
import { GenerationOptionsForm } from './GenerationOptionsForm';
import { GenerationSummaryCards } from './GenerationSummaryCards';
import { TestCasesTable } from './TestCasesTable';
import { TestCaseDetailModal } from './TestCaseDetailModal';
import {
  AnalyzeUserStoryResponse,
  CriterionDTO,
  GenerationOptionsDTO,
  GenerateTestCasesResponse,
  TestCaseDTO,
} from '../../types/testCase';
import { analyzeUserStory, generateTestCases } from '../../services/testCaseApi';
import {
  Sparkles,
  Loader2,
  AlertCircle,
  Search,
  CheckCircle2,
  FolderGit2,
  KeyRound,
  FileText,
  RefreshCw,
  Edit3,
} from 'lucide-react';

type UIState = 'IDLE' | 'ANALYZING' | 'ANALYZED' | 'GENERATING' | 'SUCCESS' | 'MANUAL_MODE';

interface TestCaseModuleProps {
  initialPayload?: {
    projectKey: string;
    issueKey: string;
    userStory: string;
    criteria: CriterionDTO[];
  } | null;
  onClearInitialPayload?: () => void;
}

export const TestCaseModule: React.FC<TestCaseModuleProps> = ({
  initialPayload,
  onClearInitialPayload,
}) => {
  const [uiState, setUiState] = useState<UIState>('IDLE');
  const [projectKey, setProjectKey] = useState('GES');
  const [issueKey, setIssueKey] = useState('GES-40');

  // Analyzed Jira Data
  const [analysisData, setAnalysisData] = useState<AnalyzeUserStoryResponse | null>(null);

  // Editable Story / Criteria (for manual fallback or tweaking)
  const [userStory, setUserStory] = useState('');
  const [criteria, setCriteria] = useState<CriterionDTO[]>([]);

  // Generation Options
  const [options, setOptions] = useState<GenerationOptionsDTO>({
    include_positive: true,
    include_negative: true,
    include_validation: true,
    include_boundary: true,
    detail_level: 'standard',
    min_priority: 'LOW',
  });

  // Results & Errors
  const [resultData, setResultData] = useState<GenerateTestCasesResponse | null>(null);
  const [selectedTestCase, setSelectedTestCase] = useState<TestCaseDTO | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [transferNotice, setTransferNotice] = useState<string | null>(null);

  // Sync if an issue was sent from Backlog Module
  useEffect(() => {
    if (initialPayload) {
      setProjectKey(initialPayload.projectKey);
      setIssueKey(initialPayload.issueKey);
      setUserStory(initialPayload.userStory);
      setCriteria(
        initialPayload.criteria.length > 0
          ? initialPayload.criteria
          : [{ id: 'AC-001', description: `Validar la funcionalidad descrita en ${initialPayload.issueKey}.` }]
      );
      setTransferNotice(`Historia ${initialPayload.issueKey} cargada desde Backlog Review Agent. Puedes analizarla en Jira o continuar en modo manual.`);
      setResultData(null);
      setAnalysisData(null);
      setUiState('IDLE');
      if (onClearInitialPayload) {
        onClearInitialPayload();
      }
    }
  }, [initialPayload, onClearInitialPayload]);

  // 1. Analyze from Jira
  const handleAnalyze = async (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    if (!projectKey.trim() || !issueKey.trim()) {
      setError('Por favor ingresa la clave del proyecto y el Issue Key.');
      return;
    }

    setUiState('ANALYZING');
    setError(null);
    setResultData(null);
    setTransferNotice(null);

    try {
      const data = await analyzeUserStory({
        project_key: projectKey.trim().toUpperCase(),
        issue_key: issueKey.trim().toUpperCase(),
      });
      setAnalysisData(data);
      setUserStory(data.user_story.raw_text);
      setCriteria(data.acceptance_criteria);
      setUiState('ANALYZED');
    } catch (err: any) {
      setError(err.message || 'Error al conectar con Jira (:8001).');
      setUiState('IDLE');
    }
  };

  // 2. Generate Test Cases (from Jira analysis or manual)
  const handleGenerate = async (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    setUiState('GENERATING');
    setError(null);

    try {
      const payload = {
        project_key: projectKey.trim().toUpperCase(),
        issue_key: issueKey.trim().toUpperCase(),
        user_story: userStory.trim() ? userStory : undefined,
        acceptance_criteria: criteria.length > 0 ? criteria : undefined,
        options,
      };

      const data = await generateTestCases(payload);
      setResultData(data);
      setUiState('SUCCESS');
    } catch (err: any) {
      setError(err.message || 'Error al generar casos de prueba (:8001).');
      setUiState(analysisData ? 'ANALYZED' : 'IDLE');
    }
  };

  // Switch to Manual Mode
  const handleSwitchToManual = () => {
    if (!userStory) {
      setUserStory(
        'Como administrador del sistema quiero gestionar los usuarios para mantener el control sobre el acceso y los permisos.'
      );
    }
    if (criteria.length === 0) {
      setCriteria([
        { id: 'AC-001', description: 'El administrador puede crear un usuario proporcionando nombre, correo y rol.' },
        { id: 'AC-002', description: 'El sistema valida que el correo electrónico sea único.' },
      ]);
    }
    setUiState('MANUAL_MODE');
  };

  return (
    <div className="max-w-7xl mx-auto p-6 space-y-6">
      {/* Transfer Notification from Backlog */}
      {transferNotice && (
        <div className="p-4 rounded-xl bg-cyan-950/40 border border-cyan-800/60 text-cyan-300 text-xs flex items-center justify-between shadow-lg animate-fadeIn">
          <div className="flex items-center gap-2">
            <Sparkles className="w-4 h-4 text-cyan-400 shrink-0" />
            <span className="font-semibold">{transferNotice}</span>
          </div>
          <div className="flex items-center gap-3">
            <button
              onClick={handleSwitchToManual}
              className="text-xs text-amber-300 hover:text-white underline font-semibold"
            >
              Abrir en Modo Manual
            </button>
            <button
              onClick={() => setTransferNotice(null)}
              className="text-cyan-400 hover:text-white text-[11px] underline"
            >
              Descartar
            </button>
          </div>
        </div>
      )}

      {/* Error Alert */}
      {error && (
        <div className="p-4 rounded-2xl bg-rose-950/40 border border-rose-800/60 text-rose-300 text-xs flex items-start gap-3 shadow-lg animate-fadeIn">
          <AlertCircle className="w-5 h-5 text-rose-400 shrink-0 mt-0.5" />
          <div>
            <span className="font-semibold block text-rose-200">Error en la integración / generación (:8001)</span>
            <p className="mt-0.5 text-rose-300/90 leading-relaxed">{error}</p>
          </div>
        </div>
      )}

      {/* STATE 1: JIRA SEARCH INPUT (IDLE / ANALYZING) */}
      {(uiState === 'IDLE' || uiState === 'ANALYZING') && (
        <section className="p-6 rounded-2xl bg-slate-900/80 border border-slate-800 backdrop-blur shadow-xl space-y-5 animate-fadeIn">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <FolderGit2 className="w-4 h-4 text-cyan-400" />
              <h3 className="text-sm font-semibold text-white uppercase tracking-wider">
                Consultar Historia de Usuario en Jira
              </h3>
            </div>
            <span className="text-[10px] font-mono text-cyan-400 bg-cyan-950/60 px-2 py-0.5 rounded border border-cyan-800/50">
              Fuente Principal: Jira Cloud
            </span>
          </div>

          <form onSubmit={handleAnalyze} className="space-y-4">
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">
                  Proyecto Jira
                </label>
                <div className="relative">
                  <FolderGit2 className="absolute left-3.5 top-2.5 w-4 h-4 text-slate-400" />
                  <input
                    type="text"
                    value={projectKey}
                    onChange={(e) => setProjectKey(e.target.value.toUpperCase())}
                    placeholder="Ej. GES, CAP, GESTADOC"
                    disabled={uiState === 'ANALYZING'}
                    className="w-full pl-10 pr-4 py-2 bg-slate-950 border border-slate-700/80 rounded-xl text-white placeholder-slate-500 text-xs font-mono font-medium focus:outline-none focus:ring-1 focus:ring-cyan-500 focus:border-cyan-500 transition-all disabled:opacity-50"
                  />
                </div>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">
                  Issue Key de la Historia
                </label>
                <div className="relative">
                  <KeyRound className="absolute left-3.5 top-2.5 w-4 h-4 text-slate-400" />
                  <input
                    type="text"
                    value={issueKey}
                    onChange={(e) => setIssueKey(e.target.value.toUpperCase())}
                    placeholder="Ej. GES-40"
                    disabled={uiState === 'ANALYZING'}
                    className="w-full pl-10 pr-4 py-2 bg-slate-950 border border-slate-700/80 rounded-xl text-white placeholder-slate-500 text-xs font-mono font-medium focus:outline-none focus:ring-1 focus:ring-cyan-500 focus:border-cyan-500 transition-all disabled:opacity-50"
                  />
                </div>
              </div>
            </div>

            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pt-2">
              <button
                type="button"
                onClick={handleSwitchToManual}
                className="text-xs text-slate-400 hover:text-cyan-400 underline underline-offset-4 text-left"
              >
                ¿Quieres ingresar la información manualmente? (Modo manual)
              </button>

              <button
                type="submit"
                disabled={uiState === 'ANALYZING' || !projectKey.trim() || !issueKey.trim()}
                className="px-6 py-2.5 bg-gradient-to-r from-cyan-500 to-indigo-600 hover:from-cyan-400 hover:to-indigo-500 text-white text-xs font-semibold rounded-xl shadow-lg shadow-cyan-500/20 active:scale-[0.98] transition-all flex items-center justify-center gap-2 disabled:opacity-60 disabled:pointer-events-none"
              >
                {uiState === 'ANALYZING' ? (
                  <>
                    <Loader2 className="w-4 h-4 animate-spin" />
                    <span>Consultando Jira...</span>
                  </>
                ) : (
                  <>
                    <Search className="w-4 h-4" />
                    <span>🔎 Analizar Historia</span>
                  </>
                )}
              </button>
            </div>
          </form>
        </section>
      )}

      {/* STATE 2: JIRA ANALYZED PREVIEW */}
      {uiState === 'ANALYZED' && analysisData && (
        <section className="space-y-6 animate-fadeIn">
          <div className="p-6 rounded-2xl bg-slate-900/90 border border-slate-800 backdrop-blur shadow-xl space-y-5">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-800 pb-4">
              <div className="flex items-center gap-2.5">
                <div className="p-2 rounded-xl bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                  <CheckCircle2 className="w-5 h-5" />
                </div>
                <div>
                  <div className="flex items-center gap-2">
                    <span className="text-base font-mono font-bold text-cyan-300">
                      {analysisData.project.issue_key}
                    </span>
                    <span className="text-xs text-slate-400 font-mono">
                      ({analysisData.project.key})
                    </span>
                  </div>
                  <span className="text-xs text-slate-400 font-medium">
                    {analysisData.user_story.title || 'Historia de Usuario en Jira'}
                  </span>
                </div>
              </div>

              <div className="flex items-center gap-2">
                <span className="px-2.5 py-1 rounded-md text-[11px] font-bold bg-cyan-950 text-cyan-300 border border-cyan-800 font-mono uppercase">
                  Fuente: {analysisData.source}
                </span>
                <span
                  className={`px-2.5 py-1 rounded-md text-[11px] font-bold font-mono uppercase ${
                    analysisData.confidence === 'HIGH'
                      ? 'bg-emerald-950 text-emerald-300 border border-emerald-800'
                      : 'bg-amber-950 text-amber-300 border border-amber-800'
                  }`}
                >
                  Confianza: {analysisData.confidence}
                </span>
              </div>
            </div>

            {/* Story Description */}
            <div className="space-y-1.5">
              <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
                <FileText className="w-3.5 h-3.5 text-cyan-400" />
                Descripción de la Historia
              </span>
              <div className="p-4 rounded-xl bg-slate-950/80 border border-slate-800 text-xs text-slate-200 leading-relaxed font-sans">
                {analysisData.user_story.raw_text}
              </div>
            </div>

            {/* Extracted Criteria List */}
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-xs font-semibold text-slate-300 uppercase tracking-wider">
                  Criterios de Aceptación Encontrados ({analysisData.acceptance_criteria.length})
                </span>
                <button
                  onClick={() => setUiState('MANUAL_MODE')}
                  className="text-xs text-cyan-400 hover:text-cyan-300 underline inline-flex items-center gap-1"
                >
                  <Edit3 className="w-3 h-3" />
                  <span>Editar criterios</span>
                </button>
              </div>

              {analysisData.acceptance_criteria.length === 0 ? (
                <div className="p-4 rounded-xl bg-amber-950/20 border border-amber-800/40 text-xs text-amber-300">
                  No se encontraron criterios de aceptación explícitos en Jira. El generador creará casos preliminares y marcará el estado como REVIEW_REQUIRED.
                </div>
              ) : (
                <div className="space-y-1.5 max-h-56 overflow-y-auto pr-1">
                  {analysisData.acceptance_criteria.map((c) => (
                    <div
                      key={c.id}
                      className="flex items-start gap-2.5 p-2.5 rounded-xl bg-slate-950/60 border border-slate-800/80 text-xs"
                    >
                      <span className="px-2 py-0.5 rounded bg-slate-800 text-cyan-300 font-mono font-semibold text-[11px]">
                        {c.id}
                      </span>
                      <span className="text-slate-200 mt-0.5">{c.description}</span>
                    </div>
                  ))}
                </div>
              )}
            </div>

            {/* Extracted QA Tests Section */}
            {analysisData.qa_tests && analysisData.qa_tests.length > 0 && (
              <div className="space-y-2 pt-2 border-t border-slate-800/80">
                <div className="flex items-center gap-1.5 text-xs font-semibold text-slate-300 uppercase tracking-wider">
                  <FileText className="w-3.5 h-3.5 text-indigo-400" />
                  <span>Pruebas QA Encontradas en Jira ({analysisData.qa_tests.length})</span>
                </div>
                <div className="space-y-1.5 max-h-48 overflow-y-auto pr-1">
                  {analysisData.qa_tests.map((test, idx) => (
                    <div
                      key={idx}
                      className="flex items-start gap-2.5 p-2 rounded-xl bg-slate-950/60 border border-slate-800/80 text-xs"
                    >
                      <span className="px-2 py-0.5 rounded bg-indigo-950/60 text-indigo-300 font-mono font-semibold text-[11px] border border-indigo-800/40">
                        QA-{(idx + 1).toString().padStart(3, '0')}
                      </span>
                      <span className="text-slate-200 mt-0.5">{test}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Generation Options Accordion */}
            <GenerationOptionsForm
              options={options}
              setOptions={setOptions}
            />

            {/* CTA Action Buttons */}
            <div className="flex flex-wrap items-center justify-between gap-3 pt-3 border-t border-slate-800">
              <button
                type="button"
                onClick={() => setUiState('IDLE')}
                className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white text-xs font-semibold rounded-xl transition-all"
              >
                ← Cambiar Issue
              </button>

              <button
                type="button"
                onClick={() => handleGenerate()}
                className="px-6 py-2.5 bg-gradient-to-r from-cyan-500 to-indigo-600 hover:from-cyan-400 hover:to-indigo-500 text-white text-xs font-semibold rounded-xl shadow-lg shadow-cyan-500/20 active:scale-[0.98] transition-all flex items-center gap-2"
              >
                <Sparkles className="w-4 h-4 fill-white" />
                <span>✨ Generar Test Cases</span>
              </button>
            </div>
          </div>
        </section>
      )}

      {/* STATE 3: GENERATING SPINNER */}
      {uiState === 'GENERATING' && (
        <div className="py-20 text-center space-y-4">
          <div className="inline-flex p-4 rounded-2xl bg-slate-900 border border-slate-800 shadow-xl animate-pulse">
            <RefreshCw className="w-8 h-8 text-cyan-400 animate-spin" />
          </div>
          <h4 className="text-sm font-semibold text-white">Sintetizando casos de prueba a partir de Jira...</h4>
          <p className="text-xs text-slate-400 max-w-md mx-auto">
            Evaluando reglas de negocio explícitas, restricciones y construyendo la matriz de trazabilidad.
          </p>
        </div>
      )}

      {/* STATE 4: SUCCESS RESULTS */}
      {uiState === 'SUCCESS' && resultData && (
        <section className="space-y-6 animate-fadeIn">
          <div className="flex items-center justify-between">
            <button
              onClick={() => setUiState('IDLE')}
              className="px-3.5 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white rounded-xl text-xs font-semibold border border-slate-700 transition-all flex items-center gap-1.5"
            >
              <span>← Consultar otra Historia</span>
            </button>
          </div>

          <GenerationSummaryCards
            summary={resultData.summary}
            warnings={resultData.warnings}
          />

          <TestCasesTable
            testCases={resultData.test_cases}
            onSelectTestCase={(tc) => setSelectedTestCase(tc)}
          />
        </section>
      )}

      {/* STATE 5: MANUAL FALLBACK MODE */}
      {uiState === 'MANUAL_MODE' && (
        <section className="bg-slate-900/80 border border-slate-800 rounded-2xl p-5 backdrop-blur shadow-xl space-y-5 animate-fadeIn">
          <div className="flex items-center justify-between border-b border-slate-800 pb-3">
            <div className="flex items-center gap-2">
              <Edit3 className="w-4 h-4 text-amber-400" />
              <h3 className="text-sm font-semibold text-white uppercase tracking-wider">
                Modo Manual (Fallback)
              </h3>
            </div>
            <button
              onClick={() => setUiState('IDLE')}
              className="text-xs text-cyan-400 hover:text-cyan-300 underline"
            >
              Volver a Modo Jira
            </button>
          </div>

          <form onSubmit={handleGenerate} className="space-y-5">
            <StoryInputForm
              projectKey={projectKey}
              setProjectKey={setProjectKey}
              issueKey={issueKey}
              setIssueKey={setIssueKey}
              userStory={userStory}
              setUserStory={setUserStory}
            />

            <CriteriaListEditor
              criteria={criteria}
              setCriteria={setCriteria}
            />

            <GenerationOptionsForm
              options={options}
              setOptions={setOptions}
            />

            <div className="flex justify-between items-center pt-2">
              <button
                type="button"
                onClick={() => setUiState('IDLE')}
                className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white text-xs font-semibold rounded-xl transition-all"
              >
                Cancelar
              </button>

              <button
                type="submit"
                className="px-6 py-2.5 bg-gradient-to-r from-cyan-500 to-indigo-600 hover:from-cyan-400 hover:to-indigo-500 text-white text-xs font-semibold rounded-xl shadow-lg shadow-cyan-500/20 active:scale-[0.98] transition-all flex items-center gap-2"
              >
                <Sparkles className="w-4 h-4 fill-white" />
                <span>✨ Generar Test Cases</span>
              </button>
            </div>
          </form>
        </section>
      )}

      {/* Test Case Detail Modal */}
      <TestCaseDetailModal
        testCase={selectedTestCase}
        onClose={() => setSelectedTestCase(null)}
      />
    </div>
  );
};
