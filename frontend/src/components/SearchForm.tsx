// components/SearchForm.tsx
import React, { memo } from 'react';

interface SearchFormProps {
  query: string;
  setQuery: (query: string) => void;
  loading: boolean;
  handleSubmit: (e: React.FormEvent) => Promise<void>;
  hasResults: boolean;
}

const SearchForm: React.FC<SearchFormProps> = memo(({ 
  query, 
  setQuery, 
  loading, 
  handleSubmit, 
  hasResults 
}) => {
  return (
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
        <form className="bg-white rounded-lg shadow-lg p-6" onSubmit={handleSubmit}>
          <div className="flex flex-col md:flex-row gap-4">
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
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
      </div>
    </div>
  );
});

SearchForm.displayName = 'SearchForm';

export default SearchForm;