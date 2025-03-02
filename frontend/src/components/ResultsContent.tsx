// components/ResultsContent.tsx
import React, { memo } from 'react';
import DynamicTable from './DynamicTable';

interface ResultsContentProps {
  searchResults: any[];
  summary: string;
  summaryVisible: boolean;
  resultsVisible: boolean;
}

const ResultsContent: React.FC<ResultsContentProps> = memo(({
  searchResults,
  summary,
  summaryVisible,
  resultsVisible
}) => {
  // Don't render anything if no results
  if (searchResults.length === 0 || !summary) {
    return null;
  }
  
  return (
    <div className="container mx-auto px-6 flex flex-col items-center">
      <div className="w-full mt-8 flex flex-col items-center">
        <div className="w-full mt-8 max-w-6xl">
          {/* Summary block with animation */}
          <div 
            className={`bg-white rounded-lg shadow-lg p-6 mb-8 w-full transition-all duration-500 ease-out ${
              summaryVisible 
                ? 'opacity-100 transform translate-y-0' 
                : 'opacity-0 transform -translate-y-8'
            }`}
          >
            <h3 className="text-xl font-semibold mb-4">Summary</h3>
            <p className="text-gray-700">{summary}</p>
          </div>
          
          {/* Search Results block with animation */}
          <div 
            className={`bg-white rounded-lg shadow-lg p-6 transition-all duration-500 ease-out ${
              resultsVisible 
                ? 'opacity-100 transform translate-y-0' 
                : 'opacity-0 transform translate-y-8'
            }`}
          >
            <h3 className="text-xl font-semibold mb-4">Search Results</h3>
            <DynamicTable data={searchResults} />
          </div>
        </div>
      </div>
    </div>
  );
});

ResultsContent.displayName = 'ResultsContent';

export default ResultsContent;