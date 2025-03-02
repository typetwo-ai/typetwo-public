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
    <div className="container mx-auto px-4 md:px-6 flex flex-col items-center">
      <div className="w-full mt-8 flex flex-col items-center">
        <div className="w-full mt-8 max-w-6xl">
          {/* Summary block with animation */}
          <div 
            className={`bg-white rounded-xl shadow-md border border-gray-100 p-6 mb-8 w-full transition-all duration-500 ease-out ${
              summaryVisible 
                ? 'opacity-100 transform translate-y-0' 
                : 'opacity-0 transform -translate-y-8'
            }`}
          >
            <h3 className="text-xl font-semibold mb-4 text-gray-800 flex items-center">
              <svg className="w-5 h-5 mr-2 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              Summary
            </h3>
            <p className="text-gray-700 leading-relaxed">{summary}</p>
          </div>
          
          {/* Search Results block with animation */}
          <div 
            className={`bg-white rounded-xl shadow-md border border-gray-100 p-6 transition-all duration-500 ease-out ${
              resultsVisible 
                ? 'opacity-100 transform translate-y-0' 
                : 'opacity-0 transform translate-y-8'
            }`}
          >
            <h3 className="text-xl font-semibold mb-4 text-gray-800 flex items-center">
              <svg className="w-5 h-5 mr-2 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
              </svg>
              Search Results
            </h3>
            <DynamicTable data={searchResults} />
          </div>
        </div>
      </div>
    </div>
  );
});

ResultsContent.displayName = 'ResultsContent';
export default ResultsContent;