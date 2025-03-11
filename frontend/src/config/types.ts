// src/config/types.ts
export interface ApiEndpoints {
    downloadExcel: (requestId: string) => string;
    query: string;
    literature: string;
  }
  
  export interface EnvironmentConfig {
    apiEndpoints: ApiEndpoints;
  }
  
  export type EnvironmentName = 'local' | 'dev' | 'main';