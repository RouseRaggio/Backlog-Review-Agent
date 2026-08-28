export type FindingStatus = 'PASS' | 'WARNING' | 'FAIL' | 'BLOCKED' | 'NOT_APPLICABLE';

export type FindingSeverity = 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';

export interface ProjectDTO {
  key: string;
  name?: string | null;
}

export interface StatisticsDTO {
  total_issues: number;
  total_findings: number;
  passed: number;
  warnings: number;
  failed: number;
  blocked: number;
}

export interface FindingDTO {
  rule_id: string;
  rule_name: string;
  issue_key: string;
  issue_type: string;
  status: FindingStatus | string;
  severity?: FindingSeverity | string | null;
  message: string;
  recommendation?: string | null;
}

export interface ReviewResponse {
  project: ProjectDTO;
  quality_score: number;
  statistics: StatisticsDTO;
  findings: FindingDTO[];
}

export interface ReviewRequest {
  project_key: string;
  max_results?: number;
}

export interface ApiError {
  detail: string;
  error_type?: string;
}
