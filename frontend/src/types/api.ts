// API Response Types based on backend schemas

export interface AskResponse {
  success: boolean;
  id: number;
  prompt: string;
  original_prompt: string;
  optimized_prompt: string;
  response: string;
  original_tokens: number;
  optimized_tokens: number;
  tokens_saved: number;
  savings_percentage: number;
  input_tokens: number;
  output_tokens: number;
  total_tokens: number;
  estimated_cost: number; // Using number for simplicity, could be string for precision
  cached: boolean;
  created_at: string; // ISO date string
}

export interface ChatRequest {
  conversation_id?: string | null;
  user_message: string;
}

export interface ChatResponse {
  success: boolean;
  conversation_id: string;
  user_message: string;
  assistant_message: string;
  summary_text: string | null;
  original_context_tokens: number;
  compressed_context_tokens: number;
  context_tokens_saved: number;
  compression_percentage: number; // Using number for simplicity
  summary_generated: boolean;
  used_summary: boolean;
  created_at: string; // ISO date string
}

export interface ConversationListItem {
  conversation_id: string;
  summary_text: string | null;
  summary_tokens: number;
  total_context_tokens_saved: number;
  total_summaries_generated: number;
  average_compression_percentage: number;
  created_at: string;
  updated_at: string;
}

export interface ConversationDetailResponse {
  conversation_id: string;
  summary_text: string | null;
  summary_tokens: number;
  total_context_tokens_saved: number;
  total_summaries_generated: number;
  average_compression_percentage: number;
  created_at: string;
  updated_at: string;
  messages: ConversationMessageItem[];
}

export interface ConversationMessageItem {
  id: number;
  user_message: string;
  assistant_message: string;
  original_context_tokens: number;
  compressed_context_tokens: number;
  context_tokens_saved: number;
  compression_percentage: number;
  summary_generated: boolean;
  used_summary: boolean;
  created_at: string;
}

export interface ConversationListResponse {
  items: ConversationListItem[];
  page: number;
  page_size: number;
  total_items: number;
  total_pages: number;
}

export interface HistoryItem {
  id: number;
  prompt: string;
  response: string;
  input_tokens: number;
  output_tokens: number;
  total_tokens: number;
  estimated_cost: number;
  served_from_cache: boolean;
  created_at: string;
}

export interface HistoryResponse {
  items: HistoryItem[];
  page: number;
  page_size: number;
  total_items: number;
  total_pages: number;
}

export interface AnalyticsResponse {
  total_requests: number;
  total_input_tokens: number;
  total_output_tokens: number;
  total_tokens: number;
  total_estimated_cost: number;
  total_cache_hits: number;
  total_cache_misses: number;
  cache_hit_rate: number;
  estimated_requests_saved: number;
  total_tokens_saved: number;
  average_tokens_saved_per_request: number;
  average_savings_percentage: number;
  total_context_tokens_saved: number;
  total_summaries_generated: number;
  average_compression_percentage: number;
}

export interface BudgetData {
  monthly_budget: number;
  used_cost: number;
  remaining_budget: number;
  usage_percentage: number;
}
