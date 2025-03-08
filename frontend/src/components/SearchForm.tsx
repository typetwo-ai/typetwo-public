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
    <form className="bg-white rounded-lg shadow-lg p-4 w-full" onSubmit={handleSubmit}>
      <div className="flex flex-col sm:flex-row items-center gap-2">
        <div className="w-full relative flex items-center">
          <TextareaAutosize
            value={query}
            onChange={(e) => {
              setQuery(e.target.value);
            }}
            minRows={1}
            maxRows={10}
            className="w-full py-3 px-4 bg-gray-50 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-main focus:border-green-main transition-all outline-none text-gray-700 resize-none overflow-auto"
            placeholder="e.g. Find all clinical drugs for Alzheimer's disease."
          />
        </div>
        <button 
          type="submit" 
          className="ml-0 sm:ml-2 mt-2 sm:mt-0 w-32 h-12 bg-green-main hover:bg-green-light text-white font-medium rounded-lg focus:outline-none disabled:opacity-70 flex items-center justify-center transition-all duration-300 ease-in-out self-center"
          disabled={loading}
        >
          {loading ? (
            <div className="flex items-center justify-center">
              <div className="animate-spin h-4 w-4 border-2 border-white border-t-transparent rounded-full mr-2"></div>
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