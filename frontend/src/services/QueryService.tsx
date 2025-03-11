// services/QueryService.tsx
import { useState } from 'react';
import axios from 'axios';
import { config } from '../config/env.config'

export interface QueryResponse {
  summary?: string;
  searchResults?: Record<string, unknown>[];
  requestId?: string;
  error?: string;
}

export const useQueryService = () => {
  const [loading, setLoading] = useState(false);

  const submitQuery = async (query: string): Promise<QueryResponse> => {
    setLoading(true);
    
    try {
      const response = await axios.post(config.apiEndpoints.query, { query });
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

  const submitSecondaryQuery = async (query: string): Promise<QueryResponse> => {
    setLoading(true);
    
    try {
      console.log("Sending query:", query);
      const response = await axios.post(config.apiEndpoints.literature, { query });
      console.log("Response:", response.data);
      
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
    submitQuery,
    submitSecondaryQuery
  };
};