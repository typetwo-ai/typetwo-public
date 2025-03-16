// services/QueryService.tsx
import { useState } from 'react';
import axios, { AxiosError } from 'axios';
import { config } from '../config/env.config'

export interface QueryResponse {
  summary?: string;
  searchResults?: Record<string, unknown>[];
  requestId?: string;
  error?: string;
}

export const useQueryService = () => {
  const [loading, setLoading] = useState(false);

  const handleError = (error: unknown): string => {
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
    
    return errorMessage;
  };

  const executeQuery = async (
    endpoint: string, 
    query: string, 
    debug = false
  ): Promise<QueryResponse> => {
    setLoading(true);
    
    try {
      if (debug) {
        console.log("Sending query:", query);
      }
      
      const response = await axios.post(endpoint, { query });
      
      if (debug) {
        console.log("Response:", response.data);
      }
      
      return response.data;
    } catch (error) {
      return { error: handleError(error) };
    } finally {
      setLoading(false);
    }
  };

  const submitQuery = async (query: string): Promise<QueryResponse> => {
    return executeQuery(config.apiEndpoints.query, query);
  };

  const submitSecondaryQuery = async (query: string): Promise<QueryResponse> => {
    return executeQuery(config.apiEndpoints.literature, query, true);
  };

  return {
    loading,
    submitQuery,
    submitSecondaryQuery
  };
};