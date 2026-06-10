import React from 'react';
import {
  BarChart as RechartsBarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';

interface BarChartProps {
  data: Array<{
    name: string;
    [key: string]: number | string;
  }>;
  dataKey: string;
  barColor?: string;
  height?: number;
}

const BarChart: React.FC<BarChartProps> = ({
  data,
  dataKey,
  barColor = '#3b82f6',
  height = 250,
}) => {
  if (!data || data.length === 0) {
    return <div className="text-center py-8 text-muted-foreground">No data available</div>;
  }

  return (
    <ResponsiveContainer width="100%" height={height}>
      <RechartsBarChart data={data} margin={{ top: 20, right: 30, left: 0, bottom: 5 }}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="name" tickLine={false} />
        <YAxis tickLine={false} />
        <Tooltip />
        <Legend verticalAlign="top" height={36} />
        <Bar dataKey={dataKey} fill={barColor} radius={[4, 4, 0, 0]} />
      </RechartsBarChart>
    </ResponsiveContainer>
  );
};

export default BarChart;
