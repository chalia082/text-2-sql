import { useQueryContext } from '@/lib/QueryProvider';
import React, { useEffect, useRef } from 'react'
import Results from './Results';
import SyntaxHighlighter from 'react-syntax-highlighter';
import { colorBrewer } from 'react-syntax-highlighter/dist/esm/styles/hljs';

export default function Output() {

  const { queries, responses, isLoading } = useQueryContext();
  const chatMessages = [];
  const bottomRef = useRef(null);

  for (let i=0; i < queries.length; i++) {
    if (queries[i]) {
      chatMessages.push({
        id: `query-${i}`,
        type: 'query',
        content: queries[i],
      });
    }
    if (responses[i]) {
      if (responses[i].type === 'success' && responses[i].response) {
        const responseData = responses[i].response;
        chatMessages.push({
          id: `response-${i}`,
          type: 'response',
          content: {
            error: responseData.error,
            query: responseData.generated_sql.query || responseData.generated_sql,
            suggestions: responseData.generated_sql.suggestions || null,
            results: responseData.results || null,
          },
        });
      } else if (responses[i].type === 'error') {
        chatMessages.push({
          id: `error-${i}`,
          type: 'error',
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
  //     console.log(message.content.error);
  //   }
  // })

  return ( 
    <div className='flex flex-col gap-10 w-full'>
      {chatMessages.map((message) => (
        <div key={message.id} className={`flex ${message.type === 'query' ? 'justify-end' : 'justify-start'}`} >
          <div className={`px-4 py-3 rounded-xl shadow-md overflow-x-auto 
            ${
              message.type === 'query'  
              ? 'max-w-[80%]' 
              : message.type === 'error'
              ? 'bg-red-100 text-red-800 dark:bg-red-800 dark:text-red-100' 
              : 'bg-gray-200 text-gray-800 dark:bg-gray-700 dark:text-gray-200'
            }
          `}>
            {message.type === 'response' ? (
              <div className="flex flex-col">
                {/* !------SQL Query------! */}
                {message.content.query && (
                  <div className="mb-3">
                    {message.content.query.blocked_cmds ? (
                      <div>
                        <h2 className="font-semibold mb-4">Error:</h2>
                        <span className="bg-white rounded-2xl px-5 py-3 text-red-700 dark:bg-red-800 dark:text-red-100">{message.content.query.blocked_cmds}</span>
                      </div>
                    ): (
                      <div className="">
                        <h2 className="font-semibold mb-2">SQL Query:</h2>
                        <pre className='whitespace-pre-wrap font-mono bg-white rounded-2xl px-5 py-3'>
                          <SyntaxHighlighter language='sql' style={colorBrewer}>{message.content.query}</SyntaxHighlighter>
                        </pre>
                      </div>
                    )}
                  </div>
                )}
                
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
                <Results results={message.content.results} />
              
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
