import React, { useState, useEffect } from 'react';
import { useApi } from '../../hooks/useApi';
import type { HistoryResponse, HistoryItem } from '../../types/api';

const History: React.FC = () => {
  const { request, loading, error } = useApi();
  const [history, setHistory] = useState<HistoryItem[]>([]);
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(10);
  const [totalItems, setTotalItems] = useState(0);
  const [totalPages, setTotalPages] = useState(0);

  const fetchHistory = async () => {
    const response = await request<HistoryResponse>('/history', 'GET', undefined, {
      page,
      page_size: pageSize,
    });

    if (response.data && !response.error) {
      setHistory(response.data.items);
      setTotalItems(response.data.total_items);
      setTotalPages(response.data.total_pages);
    } else {
      console.error('Error fetching history:', response.error);
    }
  };

  useEffect(() => {
    fetchHistory();
  }, [page, pageSize]);

  const handlePageChange = (newPage: number) => {
    if (newPage >= 1 && newPage <= totalPages) {
      setPage(newPage);
    }
  };

  const handlePageSizeChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setPageSize(Number(e.target.value));
    setPage(1); // Reset to first page when changing page size
  };

  if (loading && history.length === 0) {
    return (
      <div className="flex min-h-[200px] items-center justify-center">
        <div className="text-muted-foreground">Loading history...</div>
      </div>
    );
  }

  if (error && history.length === 0) {
    return (
      <div className="flex min-h-[200px] items-center justify-center text-red-500">
        Error: {error}
      </div>
    );
  }

  return (
    <div className="space-y-6 p-6">
      <div className="flex justify-between items-start">
        <h1 className="text-2xl font-bold">History - Request History</h1>
        <div className="text-sm text-muted-foreground">
          View your past AI requests and token usage
        </div>
      </div>

      {/* Controls */}
      <div className="flex flex-col md:flex-row md:justify-between md:items-center space-y-3 md:space-y-0">
        <div className="flex items-center space-x-3">
          <label htmlFor="pageSize" className="text-sm font-medium text-muted-foreground">
            Records per page:
          </label>
          <select
            id="pageSize"
            value={pageSize}
            onChange={handlePageSizeChange}
            className="px-3 py-2 bg-input text-input-foreground border border-input rounded-md focus:ring-2 focus-ring-primary focus-ring-offset-0"
          >
            <option value={5}>5</option>
            <option value={10}>10</option>
            <option value={25}>25</option>
            <option value={50}>50</option>
          </select>
        </div>

        <div className="flex items-center space-x-3 text-sm text-muted-foreground">
          <span>
            Page {page} of {totalPages > 0 ? totalPages : 1}
          </span>
          <span>
            {totalItems} total records
          </span>
        </div>
      </div>

      {/* Pagination Controls */}
      <div className="flex justify-center space-x-2">
        <button
          onClick={() => handlePageChange(page - 1)}
          disabled={page <= 1}
          className="px-3 py-1 bg-muted text-muted-foreground hover:bg-muted/80 transition-colors rounded-md disabled:opacity-50"
        >
          Previous
        </button>

        <button
          onClick={() => handlePageChange(page + 1)}
          disabled={page >= totalPages || totalPages === 0}
          className="px-3 py-1 bg-muted text-muted-foreground hover:bg-muted/80 transition-colors rounded-md disabled:opacity-50"
        >
          Next
        </button>
      </div>

      {/* History Table */}
      <div className="bg-card text-card-foreground shadow-sm rounded-lg border border-border overflow-hidden">
        <table className="w-full border-collapse">
          <thead>
            <tr className="bg-muted">
              <th className="px-4 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">
                Timestamp
              </th>
              <th className="px-4 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">
                Prompt
              </th>
              <th className="px-4 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">
                Response
              </th>
              <th className="px-4 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">
                Tokens
              </th>
              <th className="px-4 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">
                Cost
              </th>
              <th className="px-4 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">
                Cached
              </th>
            </tr>
          </thead>
          <tbody>
            {history.length === 0 ? (
              <tr>
                <td colSpan="6" className="px-4 py-4 text-center text-muted-foreground">
                  No history records found.
                </td>
              </tr>
            ) : (
              history.map((item, index) => (
                <tr key={index} className="border-b">
                  <td className="px-4 py-3 text-sm text-muted-foreground">
                    {new Date(item.created_at).toLocaleString()}
                  </td>
                  <td className="px-4 py-3 text-sm text-muted-foreground max-w-[200px] truncate" title={item.prompt}>
                    {item.prompt}
                  </td>
                  <td className="px-4 py-3 text-sm text-muted-foreground max-w-[200px] truncate" title={item.response}>
                    {item.response}
                  </td>
                  <td className="px-4 py-3 text-sm text-muted-foreground">
                    {item.total_tokens}
                  </td>
                  <td className="px-4 py-3 text-sm text-muted-foreground">
  ${Number(item.estimated_cost || 0).toFixed(6)}
</td>
                  <td className="px-4 py-3 text-sm text-muted-foreground">
                    {item.served_from_cache ? 'Yes' : 'No'}
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default History;