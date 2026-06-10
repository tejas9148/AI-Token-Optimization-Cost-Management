import React from 'react';
import {
  LineChart as RechartsLineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';

interface LineChartProps {
  data: Array<{
    name: string;
    [key: string]: number | string;
  }>;
  dataKey: string;
  strokeColor?: string;
  height?: number;
}

const LineChart: React.FC<LineChartProps> = ({
  data,
  dataKey,
  strokeColor = '#3b82f6',
  height = 250,
}) => {
  if (!data || data.length === 0) {
    return <div className="text-center py-8 text-muted-foreground">No data available</div>;
  }

  return (
    <ResponsiveContainer width="100%" height={height}>
      <RechartsLineChart data={data} margin={{ top: 20, right: 30, left: 0, bottom: 5 }}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="name" tickLine={false} />
        <YAxis tickLine={false} />
        <Tooltip />
        <Legend verticalAlign="top" height={36} />
        <Line type="monotone" dataKey={dataKey} stroke={strokeColor} strokeWidth={2} />
      </RechartsLineChart>
    </ResponsiveContainer>
  );
};

export default LineChart;
