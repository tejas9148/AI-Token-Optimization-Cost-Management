import React from 'react';

interface CostSummaryProps {
  totalCost: number | string;
  estimatedSavings: number | string;
  cacheHitRate: number | string;
}

const CostSummary: React.FC<CostSummaryProps> = ({
  totalCost,
  estimatedSavings,
  cacheHitRate,
}) => {
  return (
    <div className="bg-card text-card-foreground shadow-sm rounded-lg border border-border p-6">
      <h3 className="text-lg font-semibold mb-4">Cost Summary</h3>

      <div className="space-y-4">
        <div className="flex justify-between text-sm">
          <span>Total Cost:</span>
          <span className="font-medium">
            ${Number(totalCost || 0).toFixed(4)}
          </span>
        </div>

        <div className="flex justify-between text-sm">
          <span>Estimated Savings:</span>
          <span className="font-medium text-green-600">
            ${Number(estimatedSavings || 0).toFixed(4)}
          </span>
        </div>

        <div className="flex justify-between text-sm">
          <span>Cache Hit Rate:</span>
          <span className="font-medium text-blue-600">
            {Number(cacheHitRate || 0).toFixed(1)}%
          </span>
        </div>
      </div>
    </div>
  );
};

export default CostSummary;