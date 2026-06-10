import React, { useEffect, useState } from 'react';
import { useApi } from '../../hooks/useApi';
import type { AnalyticsResponse } from '../../types/api';
import  KPIcard  from '../../components/dashboard/KPIcard';
import  StatsGrid  from '../../components/dashboard/StatsGrid';
import  TokenSummary  from '../../components/dashboard/TokenSummary';
import CostSummary from '../../components/dashboard/CostSummary';
import  LineChart  from '../../components/charts/LineChart';
//import { BarChart } from '../../components/charts/BarChart';
import { formatCurrency, formatNumber, formatDate } from '../../utils/formatters';

const Dashboard: React.FC = () => {
  const { request, loading, error } = useApi();
  const [analytics, setAnalytics] = useState<AnalyticsResponse | null>(null);
  const [tokenHistory, setTokenHistory] = useState<Array<any>>([]);
  const [costHistory, setCostHistory] = useState<Array<any>>([]);

  useEffect(() => {
    const fetchData = async () => {
      // Fetch analytics data
      const analyticsResult = await request<AnalyticsResponse>('/analytics', 'GET');
      if (analyticsResult.data && !analyticsResult.error) {
        setAnalytics(analyticsResult.data);
      }

      // For demo purposes, we'll generate some mock historical data
      // In a real app, you'd fetch this from dedicated endpoints
      const generateMockData = (days: number = 7) => {
        const data = [];
        for (let i = days; i >= 0; i--) {
          const date = new Date();
          date.setDate(date.getDate() - i);
          data.push({
            name: date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
            tokens: Math.floor(Math.random() * 1000) + 500,
            cost: Math.random() * 5 + 1,
          });
        }
        return data;
      };

      setTokenHistory(generateMockData());
      setCostHistory(generateMockData());
    };

    fetchData();
  }, [request]);

  if (loading && !analytics) {
    return <div className="flex min-h-[200px] items-center justify-center">Loading...</div>;
  }

  if (error) {
    return <div className="flex min-h-[200px] items-center justify-center text-red-500">Error: {error}</div>;
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-start">
        <h1 className="text-2xl font-bold">TokenWise Dashboard</h1>
        <div className="text-sm text-muted-foreground">
          Last updated: {new Date().toLocaleTimeString()}
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {analytics && (
          <>
            <KPIcard
              title="Total Requests"
              value={formatNumber(analytics.total_requests)}
              change={Math.random() * 10 - 5} // Mock change
              icon={<svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20"><path d="M8.943 12h2.114l2.636-5.876H12l-3.014 6.736 3.014 6.736h-2.114l-2.636-5.876zM5 5a2 2 0 110-4 2 2 0 010 4z"/></svg>}
              color="blue"
            />
            <KPIcard
              title="Total Tokens Used"
              value={formatNumber(analytics.total_tokens)}
              change={Math.random() * 15 - 7} // Mock change
              icon={<svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20"><path d="M10 0a10 10 0 100 0 20 10 10 0 00-20zm1 15a3 3 0 110 0-6 3 3 0 010 6zm0-8a1 1 0 100 0-2 1 1 0 000 2z"/></svg>}
              color="green"
            />
            <KPIcard
              title="Total Cost"
              value={formatCurrency(analytics.total_estimated_cost)}
              change={Math.random() * 20 - 10} // Mock change
              icon={<svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20"><path d="M2 10a8 8 0 018-8v8h-8z"/></svg>}
              color="yellow"
            />
            <KPIcard
              title="Cache Hit Rate"
              value={`${(analytics.cache_hit_rate * 100).toFixed(1)}%`}
              change={Math.random() * 15 - 5} // Mock change
              icon={<svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20"><path d="M10 15a3 3 0 100-6 3 3 0 000 6zm0-8a1 1 0 100-2 1 1 0 000 2z"/></svg>}
              color="purple"
            />
          </>
        )}
      </div>

      {/* Summary Sections */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {analytics && (
          <TokenSummary
            totalTokens={analytics.total_tokens}
            tokensSaved={analytics.total_tokens_saved}
            compressionRate={analytics.average_compression_percentage}
          />
        )}
        {analytics && (
          <CostSummary
            totalCost={analytics.total_estimated_cost}
            estimatedSavings={analytics.total_estimated_cost * (analytics.average_savings_percentage / 100)}
            cacheHitRate={analytics.cache_hit_rate * 100}
          />
        )}
      </div>

      {/* Charts Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-card text-card-foreground shadow-sm rounded-lg border border-border p-6">
          <h3 className="text-lg font-semibold mb-4">Token Usage Trend</h3>
          <LineChart data={tokenHistory} dataKey="tokens" strokeColor="#3b82f6" />
        </div>
        <div className="bg-card text-card-foreground shadow-sm rounded-lg border border-border p-6">
          <h3 className="text-lg font-semibold mb-4">Cost Trend</h3>
          <LineChart data={costHistory} dataKey="cost" strokeColor="#f59e0b" />
        </div>
      </div>

      {/* Additional Stats Grid */}
      {analytics && (
        <div className="bg-card text-card-foreground shadow-sm rounded-lg border border-border p-6">
          <h3 className="text-lg font-semibold mb-4">Additional Statistics</h3>
          <StatsGrid
            stats={[
              { label: 'Cache Hits', value: analytics.total_cache_hits, icon: <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20"><path d="M10 15a3 3 0 100-6 3 3 0 000 6zm0-8a1 1 0 100-2 1 1 0 000 2z"/></svg> },
              { label: 'Cache Misses', value: analytics.total_cache_misses, icon: <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20"><path d="M10 15a3 3 0 110 6 3 3 0 010-6zM10 7a1 1 0 100-2 1 1 0 000 2z"/></svg> },
              { label: 'Requests Saved', value: analytics.estimated_requests_saved, icon: <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20"><path d="M10 0a10 10 0 100 20 10 10 0 000-20zm1 15a3 3 0 110-6 3 3 0 010 6z"/></svg> },
              { label: 'Avg. Savings/Req', value: `${(analytics.average_savings_percentage || 0).toFixed(1)}%`, icon: <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20"><path d="M10 15a3 3 0 100-6 3 3 0 000 6zm0-8a1 1 0 100-2 1 1 0 000 2z"/></svg> },
            ]}
            columns={2}
          />
        </div>
      )}
    </div>
  );
};

export default Dashboard;