import React from 'react';

interface StatsGridProps {
  stats: Array<{
    label: string;
    value: string | number;
    icon?: React.ReactNode;
  }>;
  columns?: number; // Number of columns (default: 2)
}

const StatsGrid: React.FC<StatsGridProps> = ({
  stats,
  columns = 2,
}) => {
  const gridClass = `grid grid-cols-${columns} gap-4`;

  return (
    <div className={gridClass}>
      {stats.map((stat, index) => (
        <div key={index} className="bg-card text-card-foreground shadow-sm rounded-lg border border-border p-4">
          <div className="flex items-center mb-2">
            {stat.icon && <div className="mr-3 text-muted-foreground text-lg">{stat.icon}</div>}
            <h4 className="text-sm font-medium text-muted-foreground flex-1">{stat.label}</h4>
          </div>
          <div className="text-lg font-bold">{typeof stat.value === 'number' ? stat.value.toLocaleString() : stat.value}</div>
        </div>
      ))}
    </div>
  );
};

export default StatsGrid;
