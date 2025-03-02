// services/QueryService.tsx
import { useState } from 'react';
import axios from 'axios';
import { Layout, Data } from 'plotly.js';

export interface QueryResponse {
  summary?: string;
  figure?: { 
    data: Data[];
    layout: Partial<Layout>;
  };
  searchResults?: any[];
  error?: string;
}

export const useQueryService = () => {
  const [loading, setLoading] = useState(false);
  const API_URL = 'http://127.0.0.1:5000/api/query';

  const submitQuery = async (query: string): Promise<QueryResponse> => {
    setLoading(true);
    
    try {
      const response = await axios.post(API_URL, { query });
      return response.data;
    } catch (error) {
      let errorMessage = 'Unknown error occurred';
      
      if (axios.isAxiosError(error)) {
        if (error.response) {
          errorMessage = error.response.data?.message || 
                         `Server error: ${error.response.status}`;
        } else if (error.request) {
          errorMessage = 'No response from server. Please check your connection.';
        } else {
          errorMessage = error.message;
        }
      } else if (error instanceof Error) {
        errorMessage = error.message;
      }
      
      return { error: errorMessage };
    } finally {
      setLoading(false);
    }
  };

  return {
    loading,
    submitQuery
  };
};