import React, { useMemo } from 'react'
import { Table, TableBody, TableCaption, TableCell, TableHead, TableHeader, TableRow } from './ui/table';


export default function Results({ results }) {

  if (!results || results.length === 0) {
    return null;
  }

  const columns = useMemo(() => {
    if (results.length === 0) return null;
    return Object.keys(results[0]);
  }, [results]);

  const formatCellValue = (value) => {
    if (value === null || value === undefined) {
      return <span className="text-gray-400 italic">null</span>;
    }
    if (typeof value === 'object') {
      return JSON.stringify(value);
    }
    return String(value);
  };

  return (
    <div className='mt-3 w-full'>
      <p className="font-semibold mb-2">Results:</p>
      <div className="bg-white px-5 py-3 rounded-2xl">
        <div className="max-h-96 w-full overflow-auto">
          <Table>
            <TableCaption className='text-start'>
              Query returned {results.length} row{results.length !== 1 ? 's' : ''} with {columns.length} column{columns.length !== 1 ? 's' : ''}
            </TableCaption>
            <TableHeader className='sticky top-0 bg-gray-50 z-10'>
              <TableRow>
                {columns.map((column) => (
                  <TableHead
                    key={column}
                    className='font-semibold text-gray-900 border-b-2 border-gray-200 whitespace-nowrap'
                  >
                    {column}
                  </TableHead>
                ))}
              </TableRow>
            </TableHeader> 
            <TableBody className='rounded-2xl'>
              {results.map((row, rowIndex) => (
                <TableRow key={rowIndex} className="hover:bg-gray-100 transition-colors rounded-2xl">
                  {columns.map((column) => (
                    <TableCell key={`${rowIndex}-${column}`} className="border-b border-gray-100 py-2 px-3">
                      {formatCellValue(row[column])}
                    </TableCell>
                  ))}
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>
      </div>

      <details className="mt-4">
        <summary className="cursor-pointer text-sm text-gray-600 hover:text-gray-800">
          Show raw JSON data
        </summary>
        <div className="mt-2 bg-gray-50 p-3 rounded-lg overflow-x-auto">
          <pre className="whitespace-pre-wrap font-mono text-xs">
            {JSON.stringify(results, null, 2)}
          </pre>
        </div>
      </details>
    </div>
  )
}
