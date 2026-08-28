import React from 'react';
import { FileText, KeyRound, FolderGit2 } from 'lucide-react';

interface StoryInputFormProps {
  projectKey: string;
  setProjectKey: (val: string) => void;
  issueKey: string;
  setIssueKey: (val: string) => void;
  userStory: string;
  setUserStory: (val: string) => void;
  disabled?: boolean;
}

export const StoryInputForm: React.FC<StoryInputFormProps> = ({
  projectKey,
  setProjectKey,
  issueKey,
  setIssueKey,
  userStory,
  setUserStory,
  disabled = false,
}) => {
  return (
    <div className="space-y-4">
      {/* Project & Issue Identifiers */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <div>
          <label className="flex items-center gap-1.5 text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">
            <FolderGit2 className="w-3.5 h-3.5 text-cyan-400" />
            <span>Proyecto Jira</span>
          </label>
          <input
            type="text"
            value={projectKey}
            onChange={(e) => setProjectKey(e.target.value.toUpperCase())}
            placeholder="Ej. GES, CAP"
            disabled={disabled}
            className="w-full px-3.5 py-2 bg-slate-950 border border-slate-700/80 rounded-xl text-white placeholder-slate-500 text-xs font-mono font-medium focus:outline-none focus:ring-1 focus:ring-cyan-500 focus:border-cyan-500 transition-all disabled:opacity-50"
          />
        </div>

        <div>
          <label className="flex items-center gap-1.5 text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">
            <KeyRound className="w-3.5 h-3.5 text-cyan-400" />
            <span>Issue Key</span>
          </label>
          <input
            type="text"
            value={issueKey}
            onChange={(e) => setIssueKey(e.target.value.toUpperCase())}
            placeholder="Ej. GES-123"
            disabled={disabled}
            className="w-full px-3.5 py-2 bg-slate-950 border border-slate-700/80 rounded-xl text-white placeholder-slate-500 text-xs font-mono font-medium focus:outline-none focus:ring-1 focus:ring-cyan-500 focus:border-cyan-500 transition-all disabled:opacity-50"
          />
        </div>
      </div>

      {/* User Story Text Area */}
      <div>
        <label className="flex items-center gap-1.5 text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">
          <FileText className="w-3.5 h-3.5 text-cyan-400" />
          <span>Historia de Usuario</span>
        </label>
        <textarea
          rows={3}
          value={userStory}
          onChange={(e) => setUserStory(e.target.value)}
          placeholder="Como [rol] quiero [funcionalidad] para [beneficio]..."
          disabled={disabled}
          className="w-full px-3.5 py-2.5 bg-slate-950 border border-slate-700/80 rounded-xl text-white placeholder-slate-500 text-xs leading-relaxed focus:outline-none focus:ring-1 focus:ring-cyan-500 focus:border-cyan-500 transition-all disabled:opacity-50 resize-none font-sans"
        />
      </div>
    </div>
  );
};
