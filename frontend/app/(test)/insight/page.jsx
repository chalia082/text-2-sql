'use client';

import InsightButton from '@/components/InsightButton'
import React, { useState } from 'react'

export default function InsightTestPage() {
  const [simulatedLoading, setSimulatedLoading] = useState(false);

  // Demo data for testing
  const demoUserInput = "Show me the top 5 customers by total order value";
  
  const demoQueryResult = [
    { customer_id: 1, customer_name: "John Smith", total_orders: 15, total_value: 2500.50 },
    { customer_id: 2, customer_name: "Sarah Johnson", total_orders: 12, total_value: 2100.75 },
    { customer_id: 3, customer_name: "Mike Brown", total_orders: 18, total_value: 1950.25 },
    { customer_id: 4, customer_name: "Emily Davis", total_orders: 8, total_value: 1800.00 },
    { customer_id: 5, customer_name: "David Wilson", total_orders: 10, total_value: 1650.30 }
  ];

  const emptyQueryResult = [];

  const simulateLoading = () => {
    setSimulatedLoading(true);
    setTimeout(() => {
      setSimulatedLoading(false);
    }, 3000); // Simulate 3 seconds of loading
  };

  return (
    <div className="container mx-auto p-6 space-y-8">
      <h1 className="text-3xl font-bold text-gray-800 mb-6">
        InsightButton Component Testing
      </h1>

      {/* Test Case 1: Normal State with Demo Data */}
      <div className="bg-white p-6 rounded-lg shadow-md border">
        <h2 className="text-xl font-semibold text-gray-700 mb-4">
          1. Normal State - With Valid Data
        </h2>
        <div className="bg-gray-50 p-4 rounded mb-4">
          <p className="text-sm text-gray-600 mb-2">
            <strong>User Input:</strong> {demoUserInput}
          </p>
          <p className="text-sm text-gray-600">
            <strong>Query Results:</strong> {demoQueryResult.length} rows of customer data
          </p>
        </div>
        <InsightButton
          userInput={demoUserInput}
          queryResult={demoQueryResult}
          messageIndex={0}
          disabled={false}
        />
      </div>

      {/* Test Case 2: Disabled State - No Results */}
      <div className="bg-white p-6 rounded-lg shadow-md border">
        <h2 className="text-xl font-semibold text-gray-700 mb-4">
          2. Disabled State - No Query Results
        </h2>
        <div className="bg-gray-50 p-4 rounded mb-4">
          <p className="text-sm text-gray-600 mb-2">
            <strong>User Input:</strong> "Find customers with no orders"
          </p>
          <p className="text-sm text-gray-600">
            <strong>Query Results:</strong> Empty array (no data)
          </p>
        </div>
        <InsightButton
          userInput="Find customers with no orders"
          queryResult={emptyQueryResult}
          messageIndex={1}
          disabled={false}
        />
      </div>

      {/* Test Case 3: Disabled State - External Disability */}
      <div className="bg-white p-6 rounded-lg shadow-md border">
        <h2 className="text-xl font-semibold text-gray-700 mb-4">
          3. Disabled State - Externally Disabled
        </h2>
        <div className="bg-gray-50 p-4 rounded mb-4">
          <p className="text-sm text-gray-600 mb-2">
            <strong>User Input:</strong> {demoUserInput}
          </p>
          <p className="text-sm text-gray-600 mb-2">
            <strong>Query Results:</strong> {demoQueryResult.length} rows available
          </p>
          <p className="text-sm text-red-600">
            <strong>Status:</strong> Disabled by parent component (e.g., during other loading)
          </p>
        </div>
        <InsightButton
          userInput={demoUserInput}
          queryResult={demoQueryResult}
          messageIndex={2}
          disabled={true}
        />
      </div>

      {/* Test Case 4: Simulated Loading State */}
      <div className="bg-white p-6 rounded-lg shadow-md border">
        <h2 className="text-xl font-semibold text-gray-700 mb-4">
          4. Loading State Simulation
        </h2>
        <div className="bg-gray-50 p-4 rounded mb-4">
          <p className="text-sm text-gray-600 mb-2">
            <strong>User Input:</strong> {demoUserInput}
          </p>
          <p className="text-sm text-gray-600 mb-2">
            <strong>Query Results:</strong> {demoQueryResult.length} rows of customer data
          </p>
          <button
            onClick={simulateLoading}
            className="bg-blue-500 text-white px-3 py-1 rounded text-sm hover:bg-blue-600"
            disabled={simulatedLoading}
          >
            {simulatedLoading ? 'Simulating...' : 'Trigger Loading Simulation'}
          </button>
        </div>
        <InsightButton
          userInput={demoUserInput}
          queryResult={demoQueryResult}
          messageIndex={3}
          disabled={simulatedLoading}
        />
      </div>

      {/* Test Case 5: Missing User Input */}
      <div className="bg-white p-6 rounded-lg shadow-md border">
        <h2 className="text-xl font-semibold text-gray-700 mb-4">
          5. Edge Case - Missing User Input
        </h2>
        <div className="bg-gray-50 p-4 rounded mb-4">
          <p className="text-sm text-gray-600 mb-2">
            <strong>User Input:</strong> <span className="text-red-600">null/undefined</span>
          </p>
          <p className="text-sm text-gray-600">
            <strong>Query Results:</strong> {demoQueryResult.length} rows available
          </p>
        </div>
        <InsightButton
          userInput={null}
          queryResult={demoQueryResult}
          messageIndex={4}
          disabled={false}
        />
      </div>

      {/* Test Case 6: Different Message Index (for insights state) */}
      <div className="bg-white p-6 rounded-lg shadow-md border">
        <h2 className="text-xl font-semibold text-gray-700 mb-4">
          6. Different Message Index Test
        </h2>
        <div className="bg-gray-50 p-4 rounded mb-4">
          <p className="text-sm text-gray-600 mb-2">
            <strong>User Input:</strong> "Show sales trends by month"
          </p>
          <p className="text-sm text-gray-600">
            <strong>Query Results:</strong> Monthly sales data (simulated)
          </p>
          <p className="text-sm text-blue-600">
            <strong>Message Index:</strong> 5 (different from others to test state isolation)
          </p>
        </div>
        <InsightButton
          userInput="Show sales trends by month"
          queryResult={[
            { month: "January", sales: 15000 },
            { month: "February", sales: 18000 },
            { month: "March", sales: 22000 }
          ]}
          messageIndex={5}
          disabled={false}
        />
      </div>

      {/* Test Information Panel */}
      <div className="bg-blue-50 p-6 rounded-lg border border-blue-200">
        <h3 className="text-lg font-semibold text-blue-800 mb-3">
          🧪 Testing Instructions
        </h3>
        <ul className="list-disc list-inside space-y-2 text-blue-700 text-sm">
          <li><strong>Test Case 1:</strong> Should show a clickable "Generate Insights" button</li>
          <li><strong>Test Case 2:</strong> Button should be disabled (gray) due to empty results</li>
          <li><strong>Test Case 3:</strong> Button should be disabled (gray) due to disabled prop</li>
          <li><strong>Test Case 4:</strong> Click the blue button to simulate loading state</li>
          <li><strong>Test Case 5:</strong> Should be disabled due to missing user input</li>
          <li><strong>Test Case 6:</strong> Test with different messageIndex for state isolation</li>
        </ul>
        
        <div className="mt-4 p-3 bg-white rounded border">
          <p className="text-sm text-gray-600">
            <strong>Note:</strong> Make sure your QueryProvider context is set up and the insights API endpoint 
            is available for full functionality testing. The loading states and disabled states 
            should work regardless of API availability.
          </p>
        </div>
      </div>

      {/* Debug Information */}
      <div className="bg-gray-50 p-4 rounded border">
        <h4 className="font-medium text-gray-700 mb-2">Debug Information</h4>
        <p className="text-xs text-gray-600">
          Simulated Loading: {simulatedLoading ? 'Active' : 'Inactive'}
        </p>
      </div>
    </div>
  )
}