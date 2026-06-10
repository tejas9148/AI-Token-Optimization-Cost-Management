import { useState, useCallback } from 'react';
import { apiService } from '../services/api';

export const useApi = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const request = useCallback(async <T>(
    endpoint: string,
    method: 'GET' | 'POST' | 'PUT' | 'DELETE' = 'GET',
    data: any = null,
    params: any = null
  ): Promise<{ data: T | null; error: string | null }> => {
    setLoading(true);
    setError(null);
    
    try {
      let response;
      switch (method) {
        case 'GET':
          response = await apiService.get<T>(endpoint, params || {});
          break;
        case 'POST':
          response = await apiService.post<T>(endpoint, data || {});
          break;
        case 'PUT':
          response = await apiService.put<T>(endpoint, data || {});
          break;
        case 'DELETE':
          response = await apiService.delete<T>(endpoint);
          break;
        default:
          throw new Error(`Unsupported method: ${method}`);
      }
      
      setLoading(false);
      return { data: response, error: null };
    } catch (err: any) {
      setLoading(false);
      setError(err.message || 'An error occurred');
      return { data: null, error: err.message || 'An error occurred' };
    }
  }, []);

  return { request, loading, error };
};
