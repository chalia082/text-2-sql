'use client';

import { useQueryContext } from '@/lib/QueryProvider';
import { fetchVisualization } from '@/utils/visualizationAPI';
import Image from 'next/image';
import React, { useState } from 'react';
import ChartRenderer from './ui/ChartRenderer';

export default function VisualizationButton({
  userInput,
  queryResult,
  messageIndex,
  disabled = false
}) {
  const { addVisualization, toggleVisualizationsLoading, visualizations } = useQueryContext();
  const [isGenerating, setIsGenerating] = useState(false);

  const hasVisualization = visualizations.find(v => v.messageIndex === messageIndex);

  const handleGenerateVisualization = async () => {
    if (!userInput || !queryResult || queryResult.length === 0) {
      console.warn('Missing required data for visualization generation');
      return;
    }

    setIsGenerating(true);
    toggleVisualizationsLoading(true);

    try {
      const result = await fetchVisualization(userInput, queryResult);

      if (result.type === 'success') {
        addVisualization({
          messageIndex,
          explanation: result.response.explanation,
          visualizationConfig: result.response.visualization_config,
          visualizationData: result.response.visualization_data,
          timestamp: new Date().toISOString()
        });
      } else {
        console.error('Failed to generate visualization:', result.error);
      }
    } catch (error) {
      console.error('Error generating visualization:', error);
    } finally {
      setIsGenerating(false);
      toggleVisualizationsLoading(false);
    }
  };

  return (
    <div className="mt-3">
      {!hasVisualization ? (
        <button
          onClick={handleGenerateVisualization}
          disabled={disabled || isGenerating || !queryResult || queryResult.length === 0}
          className={`px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
            disabled || isGenerating || !queryResult || queryResult.length === 0
              ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
              : 'border border-[#872CC1] bg-[#882cc12e] text-[#872CC1] hover:bg-[#872CC1] hover:text-white'
          }`}
        >
          {isGenerating ? (
            <span className="flex items-center gap-2">
              <Image 
                src="/loading.svg" 
                width={16} 
                height={16} 
                alt="Loading" 
                className="animate-spin"
              />
              Generating Visualization...
            </span>
          ) : (
            'Visualize Data'
          )}
        </button>
      ) : (
        <div className="bg-[#882cc12e] border border-purple-200 rounded-lg p-4">
          <h3 className="font-semibold text-[#872CC1] mb-2">Data Visualization:</h3>
          {hasVisualization.explanation && (
            <p className="text-purple-800 text-sm mb-4">
              {hasVisualization.explanation}
            </p>
          )}
          
          {hasVisualization.visualizationConfig && hasVisualization.visualizationData ? (
            <ChartRenderer
              chartType={hasVisualization.visualizationConfig.chart_type}
              data={hasVisualization.visualizationData}
              config={hasVisualization.visualizationConfig}
              explanation={hasVisualization.explanation}
            />
          ) : (
            <div className="bg-white border rounded p-3">
              <p className="text-sm">
                Unable to generate chart
              </p>
            </div>
          )}
        </div>
      )}
    </div>
  );
}