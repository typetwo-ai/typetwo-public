// components/ContentArea.tsx
import React, { useState, useEffect } from 'react';
import { Layout, Data } from 'plotly.js';
import { useQueryService } from '../services/QueryService';
import { useToast } from '../context/ToastContext';
import DynamicTable from './DynamicTable';
import SearchForm from './SearchForm';
import ResultsContent from './ResultsContent';

const ContentArea: React.FC = () => {
  const [query, setQuery] = useState('');
  const [summary, setSummary] = useState<string>('');
  const [figure, setFigure] = useState<{ data: Data[]; layout: Partial<Layout> } | null>(null);
  const [searchResults, setSearchResults] = useState<any[]>([]);
  
  // Animation states
  const [summaryVisible, setSummaryVisible] = useState(false);
  const [resultsVisible, setResultsVisible] = useState(false);
  const [hasResults, setHasResults] = useState(false);

  const { loading, submitQuery } = useQueryService();
  const { showToast } = useToast();

  // Reset animation states when new query is submitted
  useEffect(() => {
    if (loading) {
      setSummaryVisible(false);
      setResultsVisible(false);
    }
  }, [loading]);

  // Trigger animations when results are available
  useEffect(() => {
    const hasNewResults = summary !== '' || searchResults.length > 0;
    
    if (hasNewResults) {
      // Set the has results state to trigger header movement animation
      setHasResults(true);
      
      // Stagger the content animations
      setTimeout(() => setSummaryVisible(true), 300);
      setTimeout(() => setResultsVisible(true), 600);
    }
  }, [summary, searchResults]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;

    try {
      // Using mock for development, switch to submitQuery for production
      const result = await submitQuery(query);

      if (result.error) {
        showToast(result.error, 'error');
        return;
      }

      setSummary(result.summary || '');
      setFigure(result.figure || null);
      setSearchResults(result.searchResults || []);
      showToast('Query processed successfully', 'success');
    } catch (error) {
      showToast('Failed to process query', 'error');
      console.error(error);
    }
  };

  return (
    <section className="flex-grow w-full py-20 flex flex-col items-center justify-center">
      <SearchForm 
        query={query}
        setQuery={setQuery}
        loading={loading}
        handleSubmit={handleSubmit}
        hasResults={hasResults}
      />
      
      <ResultsContent 
        searchResults={searchResults}
        summary={summary}
        summaryVisible={summaryVisible}
        resultsVisible={resultsVisible}
      />
    </section>
  );
};

export default ContentArea;