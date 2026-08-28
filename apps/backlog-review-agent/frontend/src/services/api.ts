import { ReviewRequest, ReviewResponse } from '../types/api';

const API_BASE_URL = import.meta.env.VITE_API_URL || '';

export async function executeReview(payload: ReviewRequest): Promise<ReviewResponse> {
  const response = await fetch(`${API_BASE_URL}/api/reviews`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    let errorDetail = 'Error al ejecutar la auditoría';
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
      errorDetail = `Error ${response.status}: ${response.statusText}`;
    }
    throw new Error(errorDetail);
  }

  return response.json();
}

export async function downloadReport(projectKey: string): Promise<void> {
  const response = await fetch(`${API_BASE_URL}/api/reviews/${encodeURIComponent(projectKey)}/report`, {
    method: 'GET',
  });

  if (!response.ok) {
    let errorDetail = 'Error al descargar el reporte';
    try {
      const errorData = await response.json();
      if (errorData.detail) {
        errorDetail = errorData.detail;
      }
    } catch {
      errorDetail = `Error ${response.status}: ${response.statusText}`;
    }
    throw new Error(errorDetail);
  }

  const blob = await response.blob();
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.style.display = 'none';
  a.href = url;
  a.download = `${projectKey}_AUDIT.html`;
  document.body.appendChild(a);
  a.click();
  window.URL.revokeObjectURL(url);
  document.body.removeChild(a);
}
