"use client";

import { useQueryContext } from "@/lib/QueryProvider";
import React, { useEffect } from "react";

export default function APICall() {
  const { queries, currentQueryIndex, addResponse, toggleLoading } = useQueryContext();
  
  useEffect(() => {
    const fetchLLMResonse = async () => {

      if (currentQueryIndex < 0) return;
      
      const currentQuery = queries[currentQueryIndex];

      toggleLoading(true);
      const apiURI = process.env.NEXT_PUBLIC_TEST_API_URI;
      console.log(currentQuery);
      
      try { 
        const response = await fetch(apiURI, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ query: currentQuery }),
        });

        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        const data = await response.json();
        // console.log("data:", data);
        
        addResponse({
          type: 'success',
          response: data,
        });

      } catch (err) {
        // console.log(err);
        
        addResponse({
          type: 'error',
          error: err.message || 'Failed to fetch response'
        });

      } finally {
        toggleLoading(false);
      }
    };

    fetchLLMResonse();
  }, [currentQueryIndex]);

  return (
    <div></div>
  );
}