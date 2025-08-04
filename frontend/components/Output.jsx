import { useQueryContext } from '@/lib/QueryProvider';
import React, { useEffect, useRef } from 'react'
import Results from './Results';
import SyntaxHighlighter from 'react-syntax-highlighter';
import { colorBrewer } from 'react-syntax-highlighter/dist/esm/styles/hljs';
import InsightButton from './InsightButton';
import VisualizationButton from './VisualizationButton';

export default function Output() {

  const { queries, responses, isLoading } = useQueryContext();
  const chatMessages = [];
  const bottomRef = useRef(null);

  responses.map((response) => {
    console.log('response: ', response);
  })
  

  for (let i=0; i < queries.length; i++) {
    if (queries[i]) {
      chatMessages.push({
        id: `query-${i}`,
        type: 'query',
        content: queries[i],
        messageIndex: i,
      });
    }
    if (responses[i]) {
      if (responses[i].type === 'success' && responses[i].response) {
        const responseData = responses[i].response;
        const debugInformation = [
          { 
            heading: 'Detected Intent',
            value: responseData.detected_intent
          },
          { 
            heading: 'Relevant Schema Context',
            value: responseData.relevant_schema_context
          },
          { 
            heading: 'Relevant Tables',
            value: responseData.relevant_tables
          },
          { 
            heading: 'Relevant Columns',
            value: responseData.relevant_columns
          },
          { 
            heading: 'Used Prompt',
            value: responseData.used_prompt
          },
          { 
            heading: 'Query Metadata',
            value: responseData.query_metadata
          },
          { 
            heading: 'Execution Time',
            value: responseData.execution_time
          },
          { 
            heading: 'Schema Description',
            value: responseData.schema_description
          },
          { 
            heading: 'Prompt Sent to LLM',
            value: responseData.prompt_sent_to_llm
          }
        ];
        chatMessages.push({
          id: `response-${i}`,
          type: 'response',
          messageIndex: i,
          content: {
            error: responseData.error,
            query: responseData.generated_sql,
            output: responseData.final_output,
            suggestions: responseData.suggestions || [],
            results: responseData.query_result || [],
          },
          debugInfo: debugInformation
        });
      } else if (responses[i].type === 'error') {
        chatMessages.push({
          id: `error-${i}`,
          type: 'error',
          messageIndex: i,
          content: responses[i].error,
        });
      }
    }
  }

  useEffect(() => {
    if (bottomRef.current) {
      bottomRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [chatMessages.length, isLoading])

  // chatMessages.map((message) => {
  //   if (message.type === 'response') {
  //     console.log("message:", message);
  //   }
  // })

  return ( 
    <div className='flex flex-col gap-10 w-full'>
      {chatMessages.map((message) => (
        <div key={message.id} className={`flex ${message.type === 'query' ? 'justify-end' : 'justify-start'}`} >
          <div className={`px-4 py-3 rounded-xl shadow-md overflow-x-auto 
            ${
              message.type === 'query'  
              ? 'max-w-[80%] ' 
              : message.type === 'error'
              ? 'bg-red-100 text-red-800 dark:bg-red-800 dark:text-red-100' 
              : 'bg-gray-200 text-gray-800 dark:bg-gray-700 dark:text-gray-400'
            }
          `}>
            {message.type === 'response' ? (
              <div className="flex flex-col">
                {/* !------SQL Query------! */}
                {message.content.query && message.content.query.trim() !== '' ? (
                  <div className="mb-3">
                    <h2 className="font-semibold mb-2">SQL Query:</h2>
                    <pre className='whitespace-pre-wrap font-mono bg-white rounded-2xl px-5 py-3'>
                      <SyntaxHighlighter language='sql' style={colorBrewer}>
                        {message.content.query}
                      </SyntaxHighlighter>
                    </pre>
                  </div>
                ) : message.content.output ? (
                  <div className="mb-3">
                    <h2 className="font-semibold mb-2">Output:</h2>
                    <div className='whitespace-pre-wrap bg-white rounded-2xl px-5 py-3'>
                      {message.content.output}
                    </div>
                  </div>
                ) : null}
                
                {/* !------Suggestions------! */}
                {Array.isArray(message.content.suggestions) && message.content.suggestions.length > 0 && (
                  <div className="mb-3">
                    <h2 className="font-semibold mb-2">Suggestions:</h2>
                    <ol className="space-y-1">
                      {message.content.suggestions.map((sugg, s) => (
                        <li key={s} className="text-sm">{sugg}</li>
                      ))}
                    </ol>
                  </div>
                )}

                {/* !------Errors------! */}
                {message.content.error && (
                  <div className="">
                    <h2 className="font-semibold mb-2">Error:</h2>
                    <div className='bg-white rounded-2xl px-5 py-3'>
                      <span className="text-red-600">{message.content.error}</span>
                    </div>
                  </div>
                )}

                {/* !------Results------! */}
                <Results results={message.content.results} debugInfo={message.debugInfo} />

                {/* !------Action Buttons------! */}
                {message.content.results && message.content.results.length > 0 && (
                  <div className="flex flex-col gap-2 mt-3">
                    <InsightButton 
                      userInput={queries[message.messageIndex]}
                      queryResult={message.content.results}
                      messageIndex={message.messageIndex}
                      disabled={isLoading}
                    />
                    <VisualizationButton 
                      userInput={queries[message.messageIndex]}
                      queryResult={message.content.results}
                      messageIndex={message.messageIndex}
                      disabled={isLoading}
                    />
                  </div>
                )}
              
              </div>
            ) : message.type === 'error' ? (
              <div className="flex items-center gap-2">
                <span className="text-red-600">⚠️</span>
                <span>Error: {message.content}</span>
              </div>
            ) : ( 
              <p>{message.content}</p>
            )}
          </div>
        </div>
      ))}

      {isLoading && queries.length > responses.length && (
        <div className="flex w-full justify-start">
          <div className="max-w-xl lg:max-w-2xl px-4 py-3 rounded-xl shadow-md bg-yellow-100 text-yellow-800 dark:bg-yellow-800 dark:text-yellow-100">
            <div className="animate-pulse">
              <span className="inline-block">Generating response</span>
              <span className="inline-block animate-bounce">...</span>
            </div>
          </div>
        </div>
      )}
      <div ref={bottomRef} />
    </div>
  )
}
