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
    <form className="bg-white rounded-lg shadow-lg p-6" onSubmit={handleSubmit}>
      <div className="flex flex-col md:flex-row gap-4">
        <input
          type="text"
          value={query}
          onChange={(e) => {
            setQuery(e.target.value);
          }}
          className="flex-grow py-3 px-4 bg-gray-50 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all outline-none text-gray-700"
          placeholder="Search with AI in ChEMBL35..."
        />
        <button 
          type="submit" 
          className="py-3 px-8 bg-indigo-600 hover:bg-indigo-700 text-white font-medium rounded-lg focus:outline-none disabled:opacity-70 flex items-center justify-center transition-all duration-300 ease-in-out"
          style={{ minWidth: loading ? '160px' : '120px', minHeight: '48px' }}
          disabled={loading}
        >
          {loading ? (
            <div className="flex items-center justify-center">
              <div className="animate-spin h-5 w-5 border-2 border-white border-t-transparent rounded-full mr-2"></div>
              Processing
            </div>
          ) : (
            <span>Search</span>
          )}
        </button>
      </div>
    </form>
  );
});

SearchForm.displayName = 'SearchForm';

export default SearchForm;