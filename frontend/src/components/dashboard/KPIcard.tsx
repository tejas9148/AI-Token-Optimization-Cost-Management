import React from 'react';

interface KPICardProps {
  title: string;
  value: string | number;
  change?: number; // Percentage change (positive or negative)
  icon?: React.ReactNode;
  color?: 'blue' | 'green' | 'red' | 'yellow' | 'purple';
}

const KPICard: React.FC<KPICardProps> = ({
  title,
  value,
  change,
  icon,
  color = 'blue',
}) => {
  const colorClasses = {
    blue: 'text-blue-600',
    green: 'text-green-600',
    red: 'text-red-600',
    yellow: 'text-yellow-600',
    purple: 'text-purple-600',
  };

  const changeColor = change !== undefined 
    ? change >= 0 ? 'text-green-600' : 'text-red-600' 
    : 'text-muted-foreground';

  return (
    <div className="bg-card text-card-foreground shadow-sm rounded-lg border border-border p-6">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-sm font-medium text-muted-foreground">{title}</h3>
        {icon && <div className={`text-${color} ${colorClasses[color]} text-2xl`}>{icon}</div>}
      </div>
      <div className="text-2xl font-bold mb-2">{typeof value === 'number' ? value.toLocaleString() : value}</div>
      {change !== undefined && (
        <div className={`text-sm font-medium ${changeColor}`}>
          {change >= 0 ? '+' : ''}{change.toFixed(1)}%
        </div>
      )}
    </div>
  );
};

export default KPICard;
