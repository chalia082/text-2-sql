import { NextResponse } from 'next/server';
import fs from 'fs';
import path from 'path';
import Papa from 'papaparse';

export async function GET() {
  try {
    // Update this path to point to your CSV file
    const csvFilePath = path.join(process.cwd(), 'public', 'data', 'customers.csv');
    
    // Check if file exists
    if (!fs.existsSync(csvFilePath)) {
      throw new Error('CSV file not found');
    }
    
    // Read the CSV file
    const csvData = fs.readFileSync(csvFilePath, 'utf8');
    
    // Parse CSV data
    const parsedData = Papa.parse(csvData, {
      header: true,
      skipEmptyLines: true,
      dynamicTyping: true, // Auto-convert numbers and booleans
    });
    
    if (parsedData.errors.length > 0) {
      console.error('CSV parsing errors:', parsedData.errors);
    }
    
    // Return top 100 records
    const top100Data = parsedData.data.slice(0, 100);
    
    return NextResponse.json(top100Data);
    
  } catch (error) {
    console.error('Error reading CSV file:', error);
    return NextResponse.json(
      { error: 'Failed to load CSV data', message: error.message },
      { status: 500 }
    );
  }
}