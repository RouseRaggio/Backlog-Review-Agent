import { useState, useEffect } from 'react';
import { ModuleId } from './types/navigation';
import { Sidebar } from './components/layout/Sidebar';
import { Topbar } from './components/layout/Topbar';
import { DashboardModule } from './components/dashboard/DashboardModule';
import { BacklogModule } from './components/backlog/BacklogModule';
import { TestCaseModule } from './components/testCases/TestCaseModule';
import { PlaceholderModule } from './components/common/PlaceholderModule';
import { checkBacklogHealth } from './services/backlogApi';
import { checkTestCaseHealth } from './services/testCaseApi';
import { CriterionDTO } from './types/testCase';

export function App() {
  const [currentModule, setCurrentModule] = useState<ModuleId>('dashboard');

  // Agent Health statuses
  const [backlogOnline, setBacklogOnline] = useState<boolean>(false);
  const [testCaseOnline, setTestCaseOnline] = useState<boolean>(false);
  const [isCheckingHealth, setIsCheckingHealth] = useState<boolean>(false);

  // Inter-agent transfer state
  const [transferredStoryPayload, setTransferredStoryPayload] = useState<{
    projectKey: string;
    issueKey: string;
    userStory: string;
    criteria: CriterionDTO[];
  } | null>(null);

  const refreshHealthStatuses = async () => {
    setIsCheckingHealth(true);
    const [backlogStatus, testCaseStatus] = await Promise.all([
      checkBacklogHealth(),
      checkTestCaseHealth(),
    ]);
    setBacklogOnline(backlogStatus);
    setTestCaseOnline(testCaseStatus);
    setIsCheckingHealth(false);
  };

  useEffect(() => {
    refreshHealthStatuses();
    // Periodic healthcheck every 30 seconds
    const interval = setInterval(refreshHealthStatuses, 30000);
    return () => clearInterval(interval);
  }, []);

  // Inter-agent transfer handler
  const handleGenerateTestCasesFromIssue = (
    projectKey: string,
    issueKey: string,
    findingMsg: string
  ) => {
    setTransferredStoryPayload({
      projectKey: projectKey,
      issueKey: issueKey,
      userStory: `Como usuario del sistema quiero gestionar la funcionalidad correspondiente a ${issueKey} (${findingMsg.slice(0, 100)}).`,
      criteria: [
        { id: 'AC-001', description: `El sistema debe procesar adecuadamente el requerimiento de ${issueKey}.` },
        { id: 'AC-002', description: `Validar reglas de negocio y restricciones asociadas a ${issueKey}.` },
      ],
    });
    setCurrentModule('test-cases');
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex font-sans selection:bg-cyan-500 selection:text-white">
      {/* Permanent Unified Sidebar */}
      <Sidebar
        currentModule={currentModule}
        onNavigate={(mod) => setCurrentModule(mod)}
      />

      {/* Main Content Viewport */}
      <div className="flex-1 flex flex-col min-w-0 h-screen overflow-hidden">
        <Topbar
          currentModule={currentModule}
          backlogOnline={backlogOnline}
          testCaseOnline={testCaseOnline}
        />

        <main className="flex-1 overflow-y-auto">
          {currentModule === 'dashboard' && (
            <DashboardModule
              backlogOnline={backlogOnline}
              testCaseOnline={testCaseOnline}
              isCheckingHealth={isCheckingHealth}
              onRefreshHealth={refreshHealthStatuses}
              onNavigate={(mod) => setCurrentModule(mod)}
            />
          )}

          {currentModule === 'backlog' && (
            <BacklogModule
              onGenerateTestCasesFromIssue={handleGenerateTestCasesFromIssue}
            />
          )}

          {currentModule === 'test-cases' && (
            <TestCaseModule
              initialPayload={transferredStoryPayload}
              onClearInitialPayload={() => setTransferredStoryPayload(null)}
            />
          )}

          {['test-data', 'execution', 'results', 'bugs', 'configuration'].includes(currentModule) && (
            <PlaceholderModule
              moduleId={currentModule}
              onNavigate={(mod) => setCurrentModule(mod)}
            />
          )}
        </main>
      </div>
    </div>
  );
}

export default App;
