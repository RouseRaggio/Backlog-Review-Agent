import {
  AnalyzeUserStoryRequest,
  AnalyzeUserStoryResponse,
  GenerateTestCasesRequest,
  GenerateTestCasesResponse,
} from '../types/api';

const API_BASE_URL = import.meta.env.VITE_API_URL || '';

export async function analyzeUserStory(payload: AnalyzeUserStoryRequest): Promise<AnalyzeUserStoryResponse> {
  const response = await fetch(`${API_BASE_URL}/api/test-cases/analyze`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    let errorDetail = 'Error al analizar la Historia de Usuario en Jira';
    try {
      const errorData = await response.json();
      if (errorData.detail) {
        if (typeof errorData.detail === 'string') {
          errorDetail = errorData.detail;
        } else if (Array.isArray(errorData.detail)) {
          errorDetail = errorData.detail.map((err: any) => `${err.loc?.join('.')} ${err.msg}`).join(', ');
        }
      }
    } catch {
      if (response.status === 404) {
        errorDetail = `Historia de Usuario '${payload.issue_key}' no encontrada en Jira.`;
      } else if (response.status === 401 || response.status === 403) {
        errorDetail = 'No tienes permisos para consultar esta Issue en Jira.';
      } else if (response.status >= 500) {
        errorDetail = 'No fue posible comunicarse con Jira (error del servidor).';
      } else {
        errorDetail = `Error ${response.status}: ${response.statusText}`;
      }
    }
    throw new Error(errorDetail);
  }

  return response.json();
}

export async function generateTestCases(payload: GenerateTestCasesRequest): Promise<GenerateTestCasesResponse> {
  const response = await fetch(`${API_BASE_URL}/api/test-cases/generate`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    let errorDetail = 'Error al generar casos de prueba';
    try {
      const errorData = await response.json();
      if (errorData.detail) {
        if (typeof errorData.detail === 'string') {
          errorDetail = errorData.detail;
        } else if (Array.isArray(errorData.detail)) {
          errorDetail = errorData.detail.map((err: any) => `${err.loc?.join('.')} ${err.msg}`).join(', ');
        }
      }
    } catch {
      if (response.status === 404) {
        errorDetail = `Historia de Usuario '${payload.issue_key}' no encontrada en Jira.`;
      } else if (response.status === 401 || response.status === 403) {
        errorDetail = 'No tienes permisos para consultar esta Issue en Jira.';
      } else if (response.status >= 500) {
        errorDetail = 'No fue posible comunicarse con Jira (error del servidor).';
      } else {
        errorDetail = `Error ${response.status}: ${response.statusText}`;
      }
    }
    throw new Error(errorDetail);
  }

  return response.json();
}
