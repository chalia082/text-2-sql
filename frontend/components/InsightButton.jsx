'use client';

import { useQueryContext } from '@/lib/QueryProvider';
import { fetchInsights } from '@/utils/insightsAPI';
import Image from 'next/image';
import React, { useState } from 'react'

export default function InsightButton({
  userInput,
  queryResult,
  messageIndex,
  disabled = false
}) {

  const { addInsight, toggleInsightsLoading, insights } = useQueryContext();
  const [isGenerating, setIsGenerating] = useState(false);

  const hasInsights = insights[messageIndex];

  const handleGenerateInsights = async () => {
    if (!userInput || !queryResult || queryResult.length === 0) {
      console.warn('Missing required data for insights generation');
      return;
    }

    setIsGenerating(true);
    toggleInsightsLoading(true);

    try {
      const result = await fetchInsights(userInput, queryResult);

      if (result.type === 'success') {
        addInsight({
          messageIndex,
          insights: result.response.insights,
          timestamp: new Date().toISOString()
        });
      } else {
        console.error('Failed to generate insights:', result.error);
      }
    } catch (error) {
      console.error('Error generating insights:', error);
    } finally {
      setIsGenerating(false),
      toggleInsightsLoading(false);
    }
  };

  return (
    <div className="mt-3">
      {!hasInsights ? (
        <button
          onClick={handleGenerateInsights}
          disabled={disabled || isGenerating || !queryResult || queryResult.length === 0}
          className={`px-3 py-2 rounded-lg text-sm font-medium transition-colors ease-in ${
            disabled || isGenerating || !queryResult || queryResult.length === 0
              ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
              : 'border border-[#48B9FD] bg-[#48b8fd14] text-[#48B9FD] hover:bg-[#48B9FD] hover:text-white'
          }`}
        >
          {isGenerating ? (
            <span className="flex items-center gap-2">
              <span className="animate-spin"></span>
              <Image 
                src='/loading.svg'
                width={16}
                height={16}
                alt='loading'
                className='animate-spin'
              />
              Generating Insights...
            </span>
          ) : (
            'Generate Insights'
          )}
        </button>
      ) : (
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
          <h3 className="font-semibold text-blue-900 mb-2">Insights:</h3>
          <div className="text-blue-800 text-sm whitespace-pre-wrap">
            {hasInsights.insights}
          </div>
        </div>
      )}
    </div>
  )
}
