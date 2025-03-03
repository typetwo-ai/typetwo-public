// components/ContentArea.tsx
import React, { useState, useEffect } from 'react';
import { Layout, Data } from 'plotly.js';
import { useQueryService } from '../services/QueryService';
import { useToast } from '../context/ToastContext';
import SearchForm from './SearchForm';
import ResultsContent from './ResultsContent';

// Cross-browser compatible CSS
const crossBrowserScrollbarStyle = `
  html {
    overflow-y: scroll;
  }
  
  body {
    width: 100vw;
    max-width: 100%;
    overflow-x: hidden;
  }
  
  /* For Chrome */
  ::-webkit-scrollbar {
    width: 8px;
  }
  
  ::-webkit-scrollbar-track {
    background: transparent;
  }
  
  ::-webkit-scrollbar-thumb {
    background: rgba(0, 0, 0, 0.2);
    border-radius: 4px;
  }
  
  /* For Firefox */
  * {
    scrollbar-width: thin;
    scrollbar-color: rgba(0, 0, 0, 0.2) transparent;
  }
`;

const ContentArea: React.FC = () => {
  const [query, setQuery] = useState('');
  const [summary, setSummary] = useState<string>('');
  const [figure, setFigure] = useState<{ data: Data[]; layout: Partial<Layout> } | null>(null);
  const [searchResults, setSearchResults] = useState<any[]>([]);
  
  // Animation states
  const [summaryVisible, setSummaryVisible] = useState(false);
  const [resultsVisible, setResultsVisible] = useState(false);
  const [hasResults, setHasResults] = useState(false);

  // Apply scrollbar fixes on mount
  useEffect(() => {
    // Create style element
    const style = document.createElement('style');
    style.innerHTML = crossBrowserScrollbarStyle;
    document.head.appendChild(style);
    
    // Clean up
    return () => {
      document.head.removeChild(style);
    };
  }, []);
  
  const { loading, submitQuery } = useQueryService();
  const { showToast } = useToast();

  // Reset visibility when loading
  useEffect(() => {
    if (loading) {
      setSummaryVisible(false);
      setResultsVisible(false);
    }
  }, [loading]);

  // Animate results
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

  // Handle form submission
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
      setFigure(result.figure || null);
      setSearchResults(result.searchResults || []);
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
      {/* Return to tailwind but with a more stable structure */}
      <div className="container mx-auto px-4 max-w-6xl">
        {/* Title section */}
        <div className="text-center mb-8">
          <h2 className="text-4xl font-bold text-gray-800 mb-4">Retrieve data from ChEMBL35</h2>
          <p className="text-xl text-gray-600">Simply type your query in raw english. No SQL knowledge required.</p>
        </div>
        
        {/* Search form section - fixed width */}
        <div className="w-full max-w-2xl mx-auto mb-12">
          <SearchForm 
            query={query}
            setQuery={handleQueryChange}
            loading={loading}
            handleSubmit={handleSubmit}
            hasResults={hasResults}
          />
        </div>
        
        {/* Results container - hidden when empty but preserves space */}
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