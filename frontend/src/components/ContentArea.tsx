// components/ContentArea.tsx
import React, { useState, useEffect } from 'react';
import { Layout, Data } from 'plotly.js';
import { useQueryService } from '../services/QueryService';
import { useToast } from '../context/ToastContext';
import SearchForm from './SearchForm';
import ResultsContent from './ResultsContent';

const ContentArea: React.FC = () => {
  const [query, setQuery] = useState('');
  const [summary, setSummary] = useState<string>('');
  const [searchResults, setSearchResults] = useState<any[]>([]);
  const [requestId, setRequestId] = useState<string>('');
  
  const [summaryVisible, setSummaryVisible] = useState(false);
  const [resultsVisible, setResultsVisible] = useState(false);
  const [hasResults, setHasResults] = useState(false);
  
  const { loading, submitQuery } = useQueryService();
  const { showToast } = useToast();

  useEffect(() => {
    if (loading) {
      setSummaryVisible(false);
      setResultsVisible(false);
    }
  }, [loading]);

  useEffect(() => {
    const hasNewResults = summary !== '' || searchResults.length > 0;
    
    if (hasNewResults && !loading) {
      setHasResults(true);
      setTimeout(() => setSummaryVisible(true), 100);
      setTimeout(() => setResultsVisible(true), 300);
    } else if (!hasNewResults && !loading) {
      setHasResults(false);
    }
  }, [summary, searchResults, loading]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;

    try {
      setSummary('');
      setSearchResults([]);
      
      const result = await submitQuery(query);

      if (result.error) {
        showToast(result.error, 'error');
        setTimeout(() => {
          setSummaryVisible(false);
          setResultsVisible(false);
          setTimeout(() => setHasResults(false), 300);
        }, 100);
        return;
      }

      setSummary(result.summary || '');
      setSearchResults(result.searchResults || []);
      setRequestId(result.requestId || '');
      
      showToast('Query processed successfully', 'success');
    } catch (error) {
      showToast('Failed to process query', 'error');
      console.error(error);
      setTimeout(() => {
        setSummaryVisible(false);
        setResultsVisible(false);
        setTimeout(() => setHasResults(false), 300);
      }, 100);
    }
  };

  // Handle query changes
  const handleQueryChange = (newQuery: string) => {
    setQuery(newQuery);
    
    if (newQuery === '') {
      setSummaryVisible(false);
      setResultsVisible(false);
      setTimeout(() => {
        setSummary('');
        setSearchResults([]);
        setHasResults(false);
      }, 300);
    }
  };

  return (
    <div className="w-full py-8">
      <div className="container mx-auto px-4 max-w-6xl">
        <div className="text-center mb-8">
          <h2 className="text-4xl font-bold text-gray-800 mb-4">Retrieve data from ChEMBL35</h2>
          <p className="text-xl text-gray-600">Simply type your query in raw english. No SQL knowledge required.</p>
        </div>
        
        <div className="w-full max-w-2xl mx-auto mb-12">
          <SearchForm 
            query={query}
            setQuery={handleQueryChange}
            loading={loading}
            handleSubmit={handleSubmit}
            hasResults={hasResults}
          />
        </div>
        
        <div 
          className="w-full transition-opacity duration-500 ease-in-out overflow-hidden"
          style={{ 
            opacity: hasResults ? 1 : 0,
            visibility: hasResults ? 'visible' : 'hidden',
            height: hasResults ? 'auto' : '0',
            marginTop: hasResults ? '16px' : '0',
            position: 'relative'
          }}
        >
          <ResultsContent 
            searchResults={searchResults}
            requestId={requestId}
            summary={summary}
            summaryVisible={summaryVisible}
            resultsVisible={resultsVisible}
          />
        </div>
      </div>
    </div>
  );
};

export default ContentArea;