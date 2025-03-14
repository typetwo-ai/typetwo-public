// components/SearchForm.tsx
import React, { memo } from 'react';
import TextareaAutosize from 'react-textarea-autosize';

interface SearchFormProps {
  query: string;
  setQuery: (query: string) => void;
  loading: boolean;
  onSubmit: (e: React.FormEvent) => Promise<void>;
  hasResults: boolean;
}

const SearchForm: React.FC<SearchFormProps> = memo(({ 
  query, 
  setQuery, 
  loading, 
  onSubmit
}) => (
  <form className="backdrop-blur-md w-full">
    <div className="flex flex-col sm:flex-row items-center gap-2">
      <div className="w-full relative flex items-center">
        <TextareaAutosize
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          minRows={1}
          maxRows={10}
          className="w-full py-2 px-4 bg-white border shadow-inner rounded-xl focus:ring-1 focus:ring-gray-400 focus:border-gray-400 transition-all outline-none text-gray-700 resize-none overflow-auto"
          placeholder="e.g. Any new protein degradation studies?"
        />
      </div>
      <button 
        type="button" 
        className="ml-0 sm:ml-2 mt-2 sm:mt-0 w-32 h-10 bg-gray-900 hover:bg-gray-700 text-white font-medium rounded-xl focus:outline-none disabled:bg-gray-700 flex items-center justify-center transition duration-200 ease-in-out"
        disabled={loading}
        onClick={onSubmit}
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
));

SearchForm.displayName = 'SearchForm';
export default SearchForm;