'use client';

import React, { createContext, useContext, useState } from 'react'

const QueryContext = createContext();

export default function QueryProvider({ children }) {

	const [isSubmitted, setIsSubmitted] = useState(false);
  const [queries, setQueries] = useState([]);
  const [currentQueryIndex, setCurrentQueryIndex] = useState(-1);
  const [responses, setResponses] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [insights, setInsights] = useState([]);
  const [insightsLoading, setInsightsLoading] = useState(false);
  const [visualizations, setVisualizations] = useState([]);
  const [visualizationsLoading, setVisualizationsLoading] = useState(false);


  const toggleInput = () => {
    setIsSubmitted(true)
  }

  const toggleLoading = (state) => {
    setIsLoading(state)
  }

  const toggleInsightsLoading = (loading) => {
    setInsightsLoading(loading);
  }

  const toggleVisualizationsLoading = (loading) => {
    setVisualizationsLoading(loading);
  }

  const addQuery = (newQuery) => {
    setQueries(prev => [...prev, newQuery]);
    setCurrentQueryIndex(prev => prev + 1);
  }

  const addResponse = (newResponse) => {
    setResponses(prev => [...prev, newResponse]);
  }

  const addInsight = (insight) => {
    setInsights(prev => [...prev, insight]);
  }

  const addVisualization = (visualization) => {
    setVisualizations(prev => [...prev, visualization]);
  }

  const clearChat = () => {
    setIsSubmitted(false)
    setQueries([])
    setCurrentQueryIndex(-1)
    setResponses([])
    setIsLoading(false)
    setInsights([])
    setVisualizations([])
  }

  return (
    <QueryContext.Provider 
      value={{ 
        isSubmitted, 
        isLoading,
        currentQueryIndex, 
        responses, 
        queries, 
        insights,
        insightsLoading,
        visualizations,
        visualizationsLoading,
        setCurrentQueryIndex, 
        addQuery, 
        toggleInput,
        toggleLoading,
        addResponse,
        addInsight,
        toggleInsightsLoading,
        addVisualization,
        toggleVisualizationsLoading,
        clearChat, 
      }}
    >
			{children}
		</QueryContext.Provider>
  );
}

export function useQueryContext() {
	return useContext(QueryContext);
}