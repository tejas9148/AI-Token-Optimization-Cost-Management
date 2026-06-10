import axios from 'axios';
import type { AxiosInstance } from 'axios';
import { API_CONFIG } from '../config/api';

class ApiService {
  private api: AxiosInstance;

  constructor() {
    this.api = axios.create({
      baseURL: API_CONFIG.baseURL,
      timeout: API_CONFIG.timeout,
      headers: API_CONFIG.headers,
    });

    this.api.interceptors.request.use(
      (config) => config,
      (error) => Promise.reject(error)
    );

    this.api.interceptors.response.use(
      (response) => response.data,
      (error) =>
        Promise.reject(
          error.response?.data?.message ||
          error.message ||
          'An unknown error occurred'
        )
    );
  }

  async get<T>(endpoint: string, params = {}): Promise<T> {
    return this.api.get(endpoint, { params });
  }

  async post<T>(endpoint: string, data = {}): Promise<T> {
    return this.api.post(endpoint, data);
  }

  async put<T>(endpoint: string, data = {}): Promise<T> {
    return this.api.put(endpoint, data);
  }

  async delete<T>(endpoint: string): Promise<T> {
    return this.api.delete(endpoint);
  }
}

export const apiService = new ApiService();