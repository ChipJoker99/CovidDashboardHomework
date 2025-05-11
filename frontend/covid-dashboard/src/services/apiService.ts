import axios from 'axios';
import type { RegionalData } from '../types/regionalData';

const API_BASE_URL = import.meta.env.VITE_API_BACKEND_URL || 'http://127.0.0.1:8000/api/v1';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * Fetches regional COVID-19 data.
 * @param reportDate - Optional. The date for which to fetch data (YYYY-MM-DD). If null, fetches latest.
 * @param sortBy - Optional. Field to sort by.
 * @param sortOrder - Optional. Sort order ('asc' or 'desc').
 * @returns A promise that resolves to an array of RegionalData.
 */
export const getRegionalData = async (
  reportDate: string | null,
  sortBy?: string,
  sortOrder?: 'asc' | 'desc'
): Promise<RegionalData[]> => {
  try {
    const params: Record<string, string> = {};
    if (reportDate) {
      params.report_date = reportDate;
    }
    if (sortBy) {
      params.sort_by = sortBy;
    }
    if (sortOrder) {
      params.sort_order = sortOrder;
    }

    const response = await apiClient.get<RegionalData[]>('/regions/', { params });
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      console.error('Axios error fetching regional data:', error.response?.data || error.message);
      throw new Error(error.response?.data?.detail || 'Failed to fetch regional data');
    } else {
      console.error('Unexpected error fetching regional data:', error);
      throw new Error('An unexpected error occurred');
    }
  }
};