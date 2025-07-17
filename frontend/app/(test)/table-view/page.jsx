'use client';

import { Table, TableBody, TableCaption, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import React, { useEffect, useMemo, useState } from 'react'

export default function page() {

  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const generateSampleData = (count) => {
    return Array.from({ length: count }, (_, index) => ({
      id: index + 1,
      customer_name: `Customer ${index + 1}`,
      email: `customer${index + 1}@example.com`,
      amount: Math.floor(Math.random() * 10000) + 100,
      status: ['active', 'inactive', 'pending'][Math.floor(Math.random() * 3)],
      created_date: new Date(Date.now() - Math.random() * 365 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
    }));
  };

  useEffect(() => {
    const loadCSVData = async () => {
      try {
        setLoading(true);
        const response = await fetch('/api/csv-data'); 
        
        if (!response.ok) {
          throw new Error('Failed to load CSV data');
        }
        
        const csvData = await response.json();
        
        const top100Results = csvData.slice(0, 100);
        setResults(top100Results);
        
      } catch (err) {
        console.error('Error loading CSV data:', err);
        setError(err.message);
        
        // Fallback to sample data for demonstration
        const sampleData = generateSampleData(100);
        setResults(sampleData);
        
      } finally {
        setLoading(false);
      }
    };

    loadCSVData();
  }, []);

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

  if (loading) {
    return (
      <div className='mt-3 w-full'>
        <div className="flex items-center justify-center h-52">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
          <span className="ml-3 text-gray-600">Loading CSV data...</span>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className='mt-3 w-full'>
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <p className="text-red-800 font-medium">Error loading data:</p>
          <p className="text-red-600 text-sm mt-1">{error}</p>
          <p className="text-gray-600 text-sm mt-2">Showing sample data instead.</p>
        </div>
        <p className="font-semibold mb-2">Results:</p>
        <div className="bg-white px-5 py-3 rounded-2xl">
          <div className="max-h-96 w-full overflow-auto">
            <Table>
              <TableCaption className='text-start'>
                Query returned {results.length} row{results.length !== 1 ? 's' : ''} with {columns.length} column{columns.length !== 1 ? 's' : ''}
              </TableCaption>
              <TableHeader className='relative'>
                <TableRow className='sticky top-0 right-0 left-0 bg-gray-50 z-10'>
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
    );
  }

  return (
    <div className='mt-3 w-full'>
      <p className="font-semibold mb-2">Results:</p>
      <div className="bg-white px-5 py-3 rounded-2xl">
        <div className="max-h-96 w-full overflow-auto">
          <Table>
            <TableCaption className='text-start'>
              Query returned {results.length} row{results.length !== 1 ? 's' : ''} with {columns.length} column{columns.length !== 1 ? 's' : ''}
            </TableCaption>
            <TableHeader className='sticky top-0 z-10'>
              <TableRow className=' bg-gray-50 '>
                {columns.map((column) => (
                  <TableHead
                    key={column}
                    className='font-semibold text-gray-900 border-b-2 border-gray-200 whitespace-nowrap sticky top-0 z-10'
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
