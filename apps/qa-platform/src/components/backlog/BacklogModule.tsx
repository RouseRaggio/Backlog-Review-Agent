import React, { useState } from 'react';
import { executeReview, downloadReport } from '../../services/backlogApi';
import { FindingDTO, ReviewResponse } from '../../types/backlog';
import { ReviewForm } from './ReviewForm';
import { ScoreGauge } from './ScoreGauge';
import { StatsCards } from './StatsCards';
import { FindingsTable } from './FindingsTable';
import { FindingDetailModal } from './FindingDetailModal';
import { AlertCircle, RefreshCw, Layers, Download, Check, Loader2 } from 'lucide-react';

interface BacklogModuleProps {
  onGenerateTestCasesFromIssue: (projectKey: string, issueKey: string, findingMsg: string) => void;
}

export const BacklogModule: React.FC<BacklogModuleProps> = ({
  onGenerateTestCasesFromIssue,
}) => {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [reviewData, setReviewData] = useState<ReviewResponse | null>(null);
  const [selectedFinding, setSelectedFinding] = useState<FindingDTO | null>(null);

  // Download state
  const [isDownloading, setIsDownloading] = useState(false);
  const [downloadSuccess, setDownloadSuccess] = useState(false);
  const [downloadError, setDownloadError] = useState<string | null>(null);

  const handleStartReview = async (projectKey: string, maxResults: number) => {
    setIsLoading(true);
    setError(null);
    setDownloadSuccess(false);
    setDownloadError(null);
    try {
      const data = await executeReview({
        project_key: projectKey,
        max_results: maxResults,
      });
      setReviewData(data);
    } catch (err: any) {
      setError(err.message || 'Ocurrió un error al conectar con el Backlog Review Agent (:8000).');
    } finally {
      setIsLoading(false);
    }
  };

  const handleDownloadReport = async () => {
    if (!reviewData?.project.key) return;
    setIsDownloading(true);
    setDownloadError(null);
    setDownloadSuccess(false);
    try {
      await downloadReport(reviewData.project.key);
      setDownloadSuccess(true);
      setTimeout(() => {
        setDownloadSuccess(false);
      }, 3500);
    } catch (err: any) {
      setDownloadError(err.message || 'Error al descargar el reporte.');
    } finally {
      setIsDownloading(false);
    }
  };

  return (
    <div className="max-w-7xl mx-auto p-6 space-y-6">
      {/* Review Form Control */}
      <section>
        <ReviewForm
          onSubmit={handleStartReview}
          isLoading={isLoading}
          initialProject={reviewData?.project.key || 'GESTADOC'}
          initialMaxResults={100}
        />
      </section>

      {/* Error Alert */}
      {error && (
        <div className="p-4 rounded-2xl bg-rose-950/40 border border-rose-800/60 text-rose-300 text-xs flex items-start gap-3 shadow-lg">
          <AlertCircle className="w-5 h-5 text-rose-400 shrink-0 mt-0.5" />
          <div>
            <span className="font-semibold block text-rose-200">Error durante la auditoría de Backlog</span>
            <p className="text-xs text-rose-300/90 mt-0.5">{error}</p>
          </div>
        </div>
      )}

      {/* Loading State */}
      {isLoading && (
        <div className="py-16 text-center space-y-4">
          <div className="inline-flex p-4 rounded-2xl bg-slate-900 border border-slate-800 shadow-xl animate-pulse">
            <RefreshCw className="w-8 h-8 text-sky-400 animate-spin" />
          </div>
          <div>
            <h4 className="text-base font-semibold text-white">Conectando con Jira y evaluando reglas de calidad...</h4>
            <p className="text-xs text-slate-400 mt-1 max-w-md mx-auto">
              Analizando historias de usuario, descripciones, criterios de aceptación, estimaciones y dependencias.
            </p>
          </div>
        </div>
      )}

      {/* Audit Results Dashboard */}
      {!isLoading && reviewData && (
        <div className="space-y-6 animate-fadeIn">
          {/* Project Header Banner & Score */}
          <div className="grid grid-cols-1 lg:grid-cols-4 gap-6 items-stretch">
            {/* Score Gauge Card */}
            <div className="lg:col-span-1">
              <ScoreGauge score={reviewData.quality_score} />
            </div>

            {/* Project Info & Summary Metrics */}
            <div className="lg:col-span-3 flex flex-col justify-between p-6 rounded-2xl bg-slate-900/80 border border-slate-800 backdrop-blur shadow-xl space-y-6">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-800 pb-4">
                <div>
                  <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">
                    Proyecto Auditado
                  </span>
                  <div className="flex items-center gap-2 mt-1">
                    <span className="text-2xl font-bold text-white font-mono tracking-tight">
                      {reviewData.project.key}
                    </span>
                    {reviewData.project.name && (
                      <span className="text-sm font-medium text-slate-300">
                        - {reviewData.project.name}
                      </span>
                    )}
                  </div>
                </div>

                <div className="flex flex-wrap items-center gap-3">
                  <div className="flex items-center gap-2 text-xs">
                    <span className="px-3 py-1 rounded-lg bg-slate-950 border border-slate-800 text-slate-300 font-mono">
                      {reviewData.statistics.total_issues} Issues
                    </span>
                    <span className="px-3 py-1 rounded-lg bg-slate-950 border border-slate-800 text-slate-300 font-mono">
                      {reviewData.statistics.total_findings} Findings
                    </span>
                  </div>

                  {/* Download HTML Report Button */}
                  <button
                    onClick={handleDownloadReport}
                    disabled={isDownloading}
                    title="Descargar reporte HTML de la auditoría"
                    className="px-4 py-2 bg-slate-950 hover:bg-slate-800 text-slate-200 hover:text-white border border-slate-700 hover:border-slate-500 text-xs font-semibold rounded-xl shadow transition-all flex items-center gap-2 disabled:opacity-60 disabled:pointer-events-none active:scale-[0.98]"
                  >
                    {isDownloading ? (
                      <>
                        <Loader2 className="w-4 h-4 animate-spin text-sky-400" />
                        <span>Descargando...</span>
                      </>
                    ) : downloadSuccess ? (
                      <>
                        <Check className="w-4 h-4 text-emerald-400" />
                        <span className="text-emerald-300">Reporte descargado</span>
                      </>
                    ) : (
                      <>
                        <Download className="w-4 h-4 text-sky-400" />
                        <span>Descargar reporte HTML</span>
                      </>
                    )}
                  </button>
                </div>
              </div>

              {downloadError && (
                <div className="p-3 rounded-xl bg-rose-950/30 border border-rose-800/40 text-rose-300 text-xs flex items-center gap-2">
                  <AlertCircle className="w-4 h-4 text-rose-400 shrink-0" />
                  <span>{downloadError}</span>
                </div>
              )}

              {/* Quantitative Stat Cards */}
              <StatsCards statistics={reviewData.statistics} />
            </div>
          </div>

          {/* Findings Interactive Table */}
          <section className="space-y-3">
            <FindingsTable
              findings={reviewData.findings}
              onSelectFinding={(f) => setSelectedFinding(f)}
              onGenerateTestCasesFromIssue={(issueKey, findingMsg) => {

                onGenerateTestCasesFromIssue(reviewData.project.key, issueKey, findingMsg);
              }}
            />
          </section>
        </div>
      )}

      {/* Empty State */}
      {!isLoading && !reviewData && !error && (
        <div className="py-20 text-center rounded-3xl border border-dashed border-slate-800 bg-slate-900/30 p-8 space-y-4">
          <div className="inline-flex p-4 rounded-2xl bg-slate-800/50 text-slate-400 border border-slate-700/50">
            <Layers className="w-10 h-10 text-sky-400/80" />
          </div>
          <div className="max-w-md mx-auto">
            <h3 className="text-lg font-bold text-white">Auditoría de Calidad de Backlog</h3>
            <p className="text-xs text-slate-400 mt-2 leading-relaxed">
              Ingresa la clave de tu proyecto Jira (ej. <code className="text-sky-300 font-mono">GESTADOC</code>) y haz clic en <span className="text-slate-200 font-semibold">Iniciar Auditoría</span> para obtener el reporte de calidad, métricas y hallazgos detallados.
            </p>
          </div>
        </div>
      )}

      {/* Finding Detail Modal */}
      <FindingDetailModal
        finding={selectedFinding}
        onClose={() => setSelectedFinding(null)}
        onGenerateTestCases={(issueKey, findingMsg) => {
          if (reviewData) {
            onGenerateTestCasesFromIssue(reviewData.project.key, issueKey, findingMsg);
          }
        }}
      />
    </div>
  );
};
