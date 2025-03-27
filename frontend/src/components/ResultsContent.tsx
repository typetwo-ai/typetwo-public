import React, { memo, useState } from 'react';
import axios from 'axios';
import { config } from '../config/env.config'
import DynamicTable from './DynamicTable';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

interface ResultsContentProps {
  searchResults: any[];
  requestId: string;
  summary: string;
  summaryVisible: boolean;
  resultsVisible: boolean;
}

const ResultsContent: React.FC<ResultsContentProps> = memo(({
  searchResults,
  requestId,
  summary,
  summaryVisible,
  resultsVisible
}) => {
  const [isDownloading, setIsDownloading] = useState(false);

  if (!summary) {
    return null;
  }
  
  const handleExcelDownload = async () => {
    try {
      setIsDownloading(true);
      
      const response = await axios({
        method: 'post',
        url: config.apiEndpoints.downloadExcel(requestId),
        responseType: 'blob'
      });
      
      if (response.status !== 200) {
        throw new Error('Failed to download Excel file');
      }
      
      const blob = response.data;
      
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `search_results_${new Date().toISOString().split('T')[0]}.xlsx`;
      document.body.appendChild(a);
      a.click();
      
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
      
      setTimeout(() => {
        setIsDownloading(false);
      }, 1000);
    } catch (error) {
      console.error('Error downloading Excel:', error);
      alert('Failed to download Excel file. Please try again.');
      setIsDownloading(false);
    }
  };
  
  return (
    <>
      <div
        className={`bg-white rounded-xl shadow-md border border-gray-100 p-6 mb-8 transition-all duration-500 ease-out ${
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
        <div className="text-gray-700 leading-relaxed prose max-w-none">
          <ReactMarkdown remarkPlugins={[remarkGfm]}>
            {summary}
          </ReactMarkdown>
        </div>
      </div>
      
      {searchResults.length > 0 && (
        <div
          className={`bg-white rounded-xl shadow-md border border-gray-100 p-6 transition-all duration-500 ease-out ${
            resultsVisible 
              ? 'opacity-100 transform translate-y-0' 
              : 'opacity-0 transform translate-y-8'
          }`}
        >
          <div className="flex justify-between items-center mb-6">
            <h3 className="text-xl font-semibold text-gray-800 flex items-center">
              <svg className="w-5 h-5 mr-2 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
              </svg>
              Search Results
            </h3>
            
            <div className="flex items-center space-x-6">
              {/* Records count - elegant minimal design */}
              <div className="flex items-center text-gray-500 text-sm font-normal">
                <span className="mr-1 text-blue-500 font-medium">{searchResults.length == 100 ? '100+' : searchResults.length}</span>
                <span>{searchResults.length === 1 ? 'result' : 'results'}</span>
              </div>
              
              <div className="relative">
                <button
                  onClick={handleExcelDownload}
                  disabled={isDownloading}
                  className={`flex items-center justify-center border border-gray-300 rounded-md transition-all duration-300 ease-in-out shadow-sm text-gray-700 bg-white hover:bg-gray-50 hover:border-blue-300 whitespace-nowrap text-center ${
                    isDownloading ? 'px-3 py-2 w-10' : 'px-4 py-2 md:w-36 w-10'
                  }`}
                  aria-label="Download Excel"
                >
                  {isDownloading ? (
                    <svg className="animate-spin w-5 h-5 text-blue-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                  ) : (
                    <>
                      <span className="md:hidden text-sm font-medium">↓</span>
                      <span className="text-sm font-medium hidden md:inline">Download Excel</span>
                    </>
                  )}
                </button>
              </div>
            </div>
          </div>
          
          <DynamicTable data={searchResults} />
        </div>
      )}
    </>
  );
});

ResultsContent.displayName = 'ResultsContent';
export default ResultsContent;