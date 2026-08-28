export type ModuleId =
  | 'dashboard'
  | 'backlog'
  | 'test-cases'
  | 'test-data'
  | 'execution'
  | 'results'
  | 'bugs'
  | 'configuration';

export interface ModuleNavOption {
  id: ModuleId;
  label: string;
  path: string;
  iconName: string;
  status: 'Activo' | 'Próximamente';
  active: boolean;
  agentName?: string;
  description?: string;
}
