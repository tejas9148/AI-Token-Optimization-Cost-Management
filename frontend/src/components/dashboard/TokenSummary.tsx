import React from 'react';

interface TokenSummaryProps {
  totalTokens: number;
  tokensSaved: number;
  compressionRate: number; // Percentage
}

const TokenSummary: React.FC<TokenSummaryProps> = ({
  totalTokens,
  tokensSaved,
  compressionRate,
}) => {
  return (
    <div className="bg-card text-card-foreground shadow-sm rounded-lg border border-border p-6">
      <h3 className="text-lg font-semibold mb-4">Token Usage Summary</h3>
      <div className="space-y-4">
        <div className="flex justify-between text-sm">
          <span>Total Tokens Used:</span>
          <span className="font-medium">{totalTokens.toLocaleString()}</span>
        </div>
        <div className="flex justify-between text-sm">
          <span>Tokens Saved:</span>
          <span className="font-medium text-green-600">{tokensSaved.toLocaleString()}</span>
        </div>
        <div className="flex justify-between text-sm">
          <span>Compression Rate:</span>
          <span className="font-medium text-blue-600">{compressionRate.toFixed(1)}%</span>
        </div>
      </div>
    </div>
  );
};

export default TokenSummary;
