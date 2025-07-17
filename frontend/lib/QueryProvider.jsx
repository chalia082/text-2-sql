'use client';

import React, { createContext, useContext, useState } from 'react'

const QueryContext = createContext();

export default function QueryProvider({ children }) {

	const [isSubmitted, setIsSubmitted] = useState(false);
  const [queries, setQueries] = useState([]);
  const [currentQueryIndex, setCurrentQueryIndex] = useState(-1);
  const [responses, setResponses] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  const toggleInput = () => {
    setIsSubmitted(true)
  }

  const toggleLoading = (state) => {
    setIsLoading(state)
  }

  const addQuery = (newQuery) => {
    setQueries(prev => [...prev, newQuery]);
    setCurrentQueryIndex(prev => prev + 1);
  }

  const addResponse = (newResponse) => {
    setResponses(prev => [...prev, newResponse]);
  }

  const clearChat = () => {
    setIsSubmitted(false)
    setQueries([])
    setCurrentQueryIndex(-1)
    setResponses([])
    setIsLoading(false)
  }

  return (
    <QueryContext.Provider 
      value={{ 
        isSubmitted, 
        isLoading,
        currentQueryIndex, 
        responses, 
        queries, 
        setCurrentQueryIndex, 
        addQuery, 
        toggleInput,
        toggleLoading,
        addResponse,
        clearChat 
      }}
    >
			{children}
		</QueryContext.Provider>
  );
}

export function useQueryContext() {
	return useContext(QueryContext);
}