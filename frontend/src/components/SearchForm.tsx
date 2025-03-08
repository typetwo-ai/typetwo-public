import React, { memo } from 'react';
import TextareaAutosize from 'react-textarea-autosize';

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
    <form className="bg-white/70 backdrop-blur-md rounded-md shadow-md p-4 w-full" onSubmit={handleSubmit}>
      <div className="flex flex-col sm:flex-row items-center gap-2">
        <div className="w-full relative flex items-center">
          <TextareaAutosize
            value={query}
            onChange={(e) => {
              setQuery(e.target.value);
            }}
            minRows={1}
            maxRows={10}
            className="w-full py-3 px-5 bg-gray-100 border border-gray-200 shadow-sm rounded-xl focus:ring-2 focus:ring-gray-400 focus:border-gray-500 transition-all outline-none text-gray-700 resize-none overflow-auto"
            placeholder="e.g. Find all clinical drugs for Alzheimer's disease."
          />
        </div>
        <button 
          type="submit" 
          className="ml-0 sm:ml-2 mt-2 sm:mt-0 w-32 h-12 bg-gray-900 hover:bg-gray-700 text-white font-medium rounded-md focus:outline-none disabled:opacity-70 flex items-center justify-center transition duration-200 ease-in-out"
          disabled={loading}
        >
          {loading ? (
            <div className="flex items-center justify-center">
              <div className="animate-spin h-4 w-4 border-2 border-gray-200 border-t-transparent rounded-full mr-2"></div>
              <span>Search</span>
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