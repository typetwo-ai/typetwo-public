// components/Landing.tsx
import React, { useState, useEffect, useMemo } from 'react';
import { Layout, Data } from 'plotly.js';
import { useQueryService } from '../services/QueryService';
import { useToast } from '../context/ToastContext';
import DynamicTable from '../components/DynamicTable';
import AnimatedBackground from './AnimatedBackground';

const Landing: React.FC = () => {
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

  // Memoize the input change handler to prevent unnecessary re-renders
  const handleInputChange = useMemo(() => (e: React.ChangeEvent<HTMLInputElement>) => {
    setQuery(e.target.value);
  }, []);

  // Extract the form content to its own component
  const SearchForm = useMemo(() => (
    <form className="bg-white rounded-lg shadow-lg p-6" onSubmit={handleSubmit}>
      <div className="flex flex-col md:flex-row gap-4">
        <input
          type="text"
          value={query}
          onChange={handleInputChange}
          className="flex-grow py-3 px-4 bg-gray-50 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all outline-none text-gray-700"
          placeholder="Ask a question about your data..."
        />
        <button 
          type="submit" 
          className="py-3 px-8 bg-indigo-600 hover:bg-indigo-700 text-white font-medium rounded-lg focus:outline-none disabled:opacity-70 flex items-center justify-center transition-all duration-500 ease-in-out"
          style={{ width: loading ? '160px' : '120px', minHeight: '48px' }}
          disabled={loading}
        >
          {loading ? (
            <div className="flex items-center justify-center">
              <div className="animate-spin h-5 w-5 border-2 border-white border-t-transparent rounded-full mr-2"></div>
              Processing
            </div>
          ) : (
            <span>Analyze</span>
          )}
        </button>
      </div>
    </form>
  ), [query, loading, handleSubmit, handleInputChange]);

  const resultsContent = useMemo(() => (
    searchResults.length > 0 && summary ? (
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
    ) : null
  ), [searchResults, summary, summaryVisible, resultsVisible]);

  return (
    <AnimatedBackground>
      <section className="flex-grow w-full py-20 flex flex-col items-center justify-center">
        {/* This wrapper controls the animation of the header and form together */}
        <div 
          className="container mx-auto px-6 flex flex-col items-center transition-all duration-500 ease-in-out"
          style={{
            transform: hasResults ? 'translateY(-4rem)' : 'translateY(0)'
          }}
        >
          {/* Header */}
          <div className="text-center max-w-3xl mb-12">
            <h2 className="text-4xl font-bold text-gray-800 mb-4">Retrieve data from ChEMBL35</h2>
            <p className="text-xl text-gray-600">Simply type your query in raw english. No SQL knowledge required.</p>
          </div>
          
          {/* Search Form */}
          <div className="w-full max-w-2xl">
            {SearchForm}
          </div>
        </div>
        
        {/* Results section */}
        <div className="container mx-auto px-6 flex flex-col items-center">
          <div className="w-full mt-8 flex flex-col items-center">
            {resultsContent}
          </div>
        </div>
      </section>
    </AnimatedBackground>
  );
};

export default Landing;