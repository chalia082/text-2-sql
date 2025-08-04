import React, { useMemo } from 'react'
import { Table, TableBody, TableCaption, TableCell, TableHead, TableHeader, TableRow } from './ui/table';
import { Popover, PopoverContent, PopoverTrigger } from './ui/popover';
import { HiOutlineQuestionMarkCircle } from "react-icons/hi2";


export default function Results({ results, debugInfo }) {

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

  const formatDebugValue = (value) => {
    if (value === null || value === undefined) {
      return 'null';
    }
    if (Array.isArray(value)) {
      return value.join(', ');
    }
    if (typeof value === 'object') {
      return JSON.stringify(value, null, 2);
    }
    return String(value);
  };

  return (
    <div className='mt-3 w-full'>
      <div className="flex items-center mb-2 gap-2">
        <p className="font-semibold">Results:</p>
        <Popover>
          <PopoverTrigger className='p-1 hover:bg-black/10 rounded-full transition duration-150 ease-in'><HiOutlineQuestionMarkCircle className='size-6 text-blue-600 ' /></PopoverTrigger>
            <PopoverContent className={'overflow-y-scroll h-96 flex flex-col gap-3'}>
              {debugInfo.map((info, i) => (
                <div key={i} className='flex gap-1 text-[12px]'>
                  <span className="basis-28 font-semibold whitespace-pre-wrap">{info.heading}</span>
                  <span className="">:</span>
                  <span className='basis-128 ml-1 whitespace-pre-wrap'>{formatDebugValue(info.value)}</span>
                </div>
              ))}
            </PopoverContent>
          
          
        </Popover>
      </div>
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

      {/* <details className="mt-4">
        <summary className="cursor-pointer text-sm text-gray-600 hover:text-gray-800">
          Show raw JSON data
        </summary>
        <div className="mt-2 bg-gray-50 p-3 rounded-lg overflow-x-auto">
          <pre className="whitespace-pre-wrap font-mono text-xs">
            {JSON.stringify(results, null, 2)}
          </pre>
        </div>
      </details> */}
    </div>
  )
}
