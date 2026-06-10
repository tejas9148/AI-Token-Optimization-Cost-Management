import React, { useState, useEffect } from 'react';
import { useApi } from '../../hooks/useApi';
import type{ AskResponse } from '../../types/api';
import { formatNumber } from '../../utils/formatters';
import ReactMarkdown from 'react-markdown';

const Ask: React.FC = () => {
  const { request, loading, error } = useApi();
  const [prompt, setPrompt] = useState('');
  const [result, setResult] = useState<AskResponse | null>(null);
  const [submitting, setSubmitting] = useState(false);

 const handleSubmit = async (e: React.FormEvent) => {
  e.preventDefault();

  if (!prompt.trim()) return;

  setSubmitting(true);

  try {
    const response = await request<AskResponse>(
      '/ask',
      'POST',
      {
        prompt: prompt.trim(),
      }
    );

    console.log('Ask API Response:', response);

    if (response.data && !response.error) {
      console.log('Result Data:', response.data);
      setResult(response.data);
    } else {
      console.error('API Error:', response.error);
    }
  } catch (err) {
    console.error('Request Failed:', err);
  } finally {
    setSubmitting(false);
  }
};

  return (
    <div className="space-y-6 p-6">
      <div className="flex justify-between items-start">
        <h1 className="text-2xl font-bold">Ask - Prompt Optimization</h1>
        <div className="text-sm text-muted-foreground">
          Optimize your prompts to reduce token usage and costs
        </div>
      </div>

      {/* Form */}
      <form onSubmit={handleSubmit} className="bg-card text-card-foreground shadow-sm rounded-lg border border-border p-6">
        <div className="space-y-4">
          <div>
            <label htmlFor="prompt" className="mb-2 block text-sm font-medium text-muted-foreground">
              Enter your prompt
            </label>
            <textarea
              id="prompt"
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              rows={4}
              className="w-full px-4 py-3 bg-input text-input-foreground border border-input placeholder:text-muted-foreground/50 focus:ring-2 focus:ring-primary focus:ring-offset-0 disabled:opacity-50 resize-none"
              placeholder="Ask me anything..."
              disabled={submitting}
            />
          </div>

          <button
            type="submit"
            disabled={submitting || !prompt.trim()}
            className="w-full px-4 py-3 bg-primary text-primary-foreground hover:bg-primary/90 disabled:opacity-50 transition-colors"
          >
            {submitting ? 'Optimizing...' : 'Optimize Prompt'}
          </button>
        </div>
      </form>

      {/* Results */}
      {result && (
        <div className="bg-card text-card-foreground shadow-sm rounded-lg border border-border p-6">
          <h2 className="text-xl font-semibold mb-4">Results</h2>

          {/* Original vs Optimized Prompt */}
          <div className="space-y-6">
            <div className="space-y-3">
              <h3 className="text-lg font-semibold">Original Prompt</h3>
              <p className="text-muted-foreground">{result.original_prompt}</p>
              <div className="text-xs text-muted-foreground mt-2">
                Tokens: {formatNumber(result.original_tokens)}
              </div>
            </div>

            <div className="space-y-3">
              <h3 className="text-lg font-semibold">Optimized Prompt</h3>
              <p className="text-muted-foreground">{result.optimized_prompt}</p>
              <div className="text-xs text-muted-foreground mt-2">
                Tokens: {formatNumber(result.optimized_tokens)}
              </div>
            </div>
          </div>

          {/* AI Response */}
          <div className="space-y-4">
            <h3 className="text-lg font-semibold">AI Response</h3>
           <div className="prose max-w-none">
                 <ReactMarkdown>
              {result.response}
                </ReactMarkdown>
</div>          </div>

         {/* Metrics */}
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4 mt-6">
  <div className="space-y-3">
    <h3 className="text-lg font-semibold">Tokens Saved</h3>
    <p className="text-2xl font-bold text-green-600">
      {formatNumber(result.tokens_saved)}
    </p>
  </div>

  <div className="space-y-3">
    <h3 className="text-lg font-semibold">Savings Percentage</h3>
    <p className="text-2xl font-bold text-green-600">
      {Number(result.savings_percentage || 0).toFixed(1)}%
    </p>
  </div>

  <div className="space-y-3">
    <h3 className="text-lg font-semibold">Estimated Cost</h3>
    <p className="text-2xl font-bold text-blue-600">
      ${result.estimated_cost}
    </p>
    <p className="text-xs text-muted-foreground">
      Backend Calculated
    </p>
  </div>

  <div className="space-y-3">
    <h3 className="text-lg font-semibold">Cache Status</h3>
    <p
      className={`text-2xl font-bold ${
        result.cached ? 'text-green-600' : 'text-red-600'
      }`}
    >
      {result.cached ? 'CACHE HIT' : 'CACHE MISS'}
    </p>
  </div>

  <div className="space-y-3">
    <h3 className="text-lg font-semibold">Total Tokens</h3>
    <p className="text-2xl font-bold">
      {formatNumber(result.total_tokens || 0)}
    </p>
  </div>
</div>

          {/* Action Buttons */}
          <div className="mt-6 flex flex-col sm:flex-row sm:space-x-3">
            <button
              onClick={() => setPrompt(result.optimized_prompt)}
              className="w-full sm:w-auto px-4 py-2 bg-muted text-muted-foreground hover:bg-muted/80 transition-colors flex-1 sm:flex-1"
            >
              Use Optimized Prompt
            </button>
            <button
              onClick={() => setPrompt('')}
              className="w-full sm:w-auto px-4 py-2 bg-destructive text-destructive-foreground hover:bg-destructive/90 transition-colors flex-1 sm:flex-1"
            >
              New Prompt
            </button>
          </div>
        </div>
      )}

      {/* Loading State */}
      {loading && !result && (
        <div className="flex min-h-[200px] items-center justify-center">
          <div className="text-muted-foreground">Loading...</div>
        </div>
      )}

      {/* Error State */}
      {error && !result && (
        <div className="flex min-h-[200px] items-center justify-center text-red-500">
          Error: {error}
        </div>
      )}
    </div>
  );
};

export default Ask;