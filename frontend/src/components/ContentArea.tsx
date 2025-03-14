// components/ContentArea.tsx
import React, { useState, useEffect } from 'react';
import { useQueryService } from '../services/QueryService';
import { useToast } from '../context/ToastContext';
import SearchForm from './SearchForm';
import ResultsContent from './ResultsContent';

const ContentArea: React.FC = () => {
  const [query, setQuery] = useState('');
  const [summary, setSummary] = useState<string>('');
  const [searchResults, setSearchResults] = useState<Record<string, unknown>[]>([]);
  const [requestId, setRequestId] = useState<string>('');
  
  const [summaryVisible, setSummaryVisible] = useState(false);
  const [resultsVisible, setResultsVisible] = useState(false);
  const [hasResults, setHasResults] = useState(false);
  
  const { loading, submitQuery, submitSecondaryQuery } = useQueryService();
  const { showToast } = useToast();

  useEffect(() => {
    if (loading) {
      setSummaryVisible(false);
      setResultsVisible(false);
    }
  }, [loading]);

  useEffect(() => {
    const hasNewResults = summary !== '' || searchResults.length > 0;
    console.log("Results state:", { summary, searchResults, hasNewResults });
    
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

  const handleSecondarySubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;

    try {
      setSummary('');
      setSearchResults([]);
      
      const result = await submitSecondaryQuery(query);
      console.log("Result received:", result);

      if (result.error) {
        showToast(result.error, 'error');
        setTimeout(() => {
          setSummaryVisible(false);
          setResultsVisible(false);
          setTimeout(() => setHasResults(false), 300);
        }, 100);
        return;
      }

      console.log("Setting summary to:", result.summary);
      setSummary(result.summary || '');
      setSearchResults([]);
      setRequestId('');
      
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

  const handleQueryChange = (newQuery: string) => {
    setQuery(newQuery);

    if (!newQuery.trim()) {
      setSummary('');
      setSearchResults([]);
      setHasResults(false);
      setSummaryVisible(false);
      setResultsVisible(false);
    }
  };

  return (
    <div className="py-8">
      <div className="mx-auto max-w-6xl text-center mb-8">
        <h2 className="text-3xl font-semibold tracking-normal text-gray-900 mb-5">
          Literature Review
        </h2>
        <p className="text-lg tracking-normal text-gray-500">
          Simply type what you want to know about.
        </p>
      </div>
  
      <div className="max-w-2xl mx-auto mb-12 mt-6">
        <SearchForm 
          query={query}
          setQuery={handleQueryChange}
          loading={loading}
          onSubmit={handleSecondarySubmit}
          hasResults={hasResults}
        />
      </div>
  
      <div 
        className={`transition-opacity duration-500 ease-in-out overflow-hidden 
        ${hasResults ? 'opacity-100 visible mt-4' : 'opacity-0 invisible h-0'}`}
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
  );
};

export default ContentArea;
