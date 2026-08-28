export type TestCaseType = 'POSITIVE' | 'NEGATIVE' | 'VALIDATION' | 'BOUNDARY';
export type Category = 'FUNCTIONAL' | 'BUSINESS_RULE' | 'VALIDATION' | 'ERROR_HANDLING' | 'BOUNDARY';
export type Priority = 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
export type Status = 'NEW' | 'READY' | 'REVIEW_REQUIRED';
export type Confidence = 'HIGH' | 'MEDIUM' | 'LOW';

export interface CriterionDTO {
  id: string;
  description: string;
}

export interface GenerationOptionsDTO {
  include_positive: boolean;
  include_negative: boolean;
  include_validation: boolean;
  include_boundary: boolean;
  detail_level: 'basic' | 'standard' | 'detailed' | string;
  min_priority: Priority | string;
}

export interface AnalyzeUserStoryRequest {
  project_key: string;
  issue_key: string;
}

export interface UserStoryPreviewDTO {
  title?: string | null;
  role?: string | null;
  goal?: string | null;
  benefit?: string | null;
  raw_text: string;
}

export interface AnalyzeUserStoryResponse {
  project: ProjectInfoDTO;
  user_story: UserStoryPreviewDTO;
  acceptance_criteria: CriterionDTO[];
  qa_tests?: string[];
  source: string;
  sufficient_information: boolean;
  confidence: Confidence | string;
  warnings: string[];
  metadata?: Record<string, any>;
}


export interface GenerateTestCasesRequest {
  project_key: string;
  issue_key: string;
  user_story?: string;
  acceptance_criteria?: CriterionDTO[];
  options: GenerationOptionsDTO;
}

export interface TestCaseDTO {
  id: string;
  title: string;
  description: string;
  type: TestCaseType | string;
  category: Category | string;
  priority: Priority | string;
  preconditions: string[];
  required_data: Record<string, string>;
  steps: string[];
  expected_result: string;
  requirement_reference: string;
  acceptance_criteria_reference?: string | null;
  confidence: Confidence | string;
  status: Status | string;
}

export interface ProjectInfoDTO {
  key: string;
  issue_key: string;
}

export interface SummaryMetricsDTO {
  total_cases: number;
  positive_count: number;
  negative_count: number;
  validation_count: number;
  boundary_count: number;
  traceability_rate: number;
  overall_confidence: Confidence | string;
}

export interface GenerateTestCasesResponse {
  project: ProjectInfoDTO;
  summary: SummaryMetricsDTO;
  warnings: string[];
  test_cases: TestCaseDTO[];
  traceability: Record<string, string[]>;
}
