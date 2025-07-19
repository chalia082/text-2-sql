'use client';

import React from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Bar, Line, Pie } from 'react-chartjs-2';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
  ArcElement,
  Title,
  Tooltip,
  Legend
);

export default function ChartRenderer({ 
  chartType, 
  data, 
  config, 
  explanation 
}) {
  
  const defaultOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: explanation || 'Data Visualization',
      },
    },
  };

  const prepareChartData = () => {
    if (!data || !config) return null;

    switch (chartType) {
      case 'bar':
      case 'line':
        const labels = data.map(item => item[config.x]);
        const values = data.map(item => item[config.y]);
        
        return {
          labels,
          datasets: [
            {
              label: config.y,
              data: values,
              backgroundColor: chartType === 'bar' 
                ? 'rgba(72, 185, 253, 0.6)'
                : 'rgba(72, 185, 253, 0.2)',
              borderColor: 'rgba(72, 185, 253, 1)',
              borderWidth: 2,
              fill: chartType === 'line' ? false : true,
            },
          ],
        };

      case 'pie':
        const pieLabels = data.map(item => item[config.labels]);
        const pieValues = data.map(item => item[config.values]);
        
        return {
          labels: pieLabels,
          datasets: [
            {
              data: pieValues,
              backgroundColor: [
                'rgba(72, 185, 253, 0.8)',
                'rgba(255, 99, 132, 0.8)',
                'rgba(255, 205, 86, 0.8)',
                'rgba(75, 192, 192, 0.8)',
                'rgba(153, 102, 255, 0.8)',
                'rgba(255, 159, 64, 0.8)',
                'rgba(199, 199, 199, 0.8)',
              ],
              borderColor: [
                'rgba(72, 185, 253, 1)',
                'rgba(255, 99, 132, 1)',
                'rgba(255, 205, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)',
                'rgba(199, 199, 199, 1)',
              ],
              borderWidth: 1,
            },
          ],
        };

      default:
        return null;
    }
  };

  const chartData = prepareChartData();

  if (!chartData) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-lg p-4">
        <p className="text-red-600 text-sm">
          Unable to render chart: Invalid data or configuration
        </p>
      </div>
    );
  }

  const renderChart = () => {
    switch (chartType) {
      case 'bar':
        return <Bar data={chartData} options={defaultOptions} />;
      case 'line':
        return <Line data={chartData} options={defaultOptions} />;
      case 'pie':
        return <Pie data={chartData} options={defaultOptions} />;
      default:
        return (
          <div className="text-center text-gray-500">
            Unsupported chart type: {chartType}
          </div>
        );
    }
  };

  return (
    <div className="bg-white border border-gray-200 rounded-lg p-4">
      <div style={{ height: '400px', width: '100%' }}>
        {renderChart()}
      </div>
    </div>
  );
}