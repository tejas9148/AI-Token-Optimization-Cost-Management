import { VITE_API_URL } from './env';

// API configuration
export const API_CONFIG = {
  baseURL: VITE_API_URL,
  timeout: 10000, // 10 seconds
  headers: {
    'Content-Type': 'application/json',
  },
};

export const API_ENDPOINTS = {
  // AI Gateway
  ASK: '/ask',
  
  // Chat
  CHAT: '/chat',
  CONVERSATIONS: '/conversations',
  
  // History
  HISTORY: '/history',
  
  // Analytics
  ANALYTICS: '/analytics',
  
  // Health
  HEALTH: '/health',
};
