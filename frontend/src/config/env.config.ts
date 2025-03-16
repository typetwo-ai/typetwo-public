// src/config/env.config.ts
import { EnvironmentConfig, EnvironmentName } from './types';

const configs: Record<EnvironmentName, EnvironmentConfig> = {
  local: {
    apiEndpoints: {
      downloadExcel: (requestId: string) => `http://127.0.0.1:5000/api/download-excel/${requestId}`,
      query: 'http://127.0.0.1:5000/api/query',
      literature: 'http://127.0.0.1:5000/api/literature'
    }
  },
  dev: {
    apiEndpoints: {
      downloadExcel: (requestId: string) => `https://dev-backend-api-dot-project-1-450712.uc.r.appspot.com/api/download-excel/${requestId}`,
      query: 'https://dev-backend-api-dot-project-1-450712.uc.r.appspot.com/api/query',
      literature: 'https://dev-backend-api-dot-project-1-450712.uc.r.appspot.com/api/literature'
    }
  },
  main: {
    apiEndpoints: {
      downloadExcel: (requestId: string) => `https://beta.typetwo.ai/api/download-excel/${requestId}`,
      query: 'https://beta.typetwo.ai/api/query',
      literature: 'https://beta.typetwo.ai/api/literature'
    }
  }
};

const getEnvironment = (): EnvironmentName => {
    const env = import.meta.env.VITE_NODE_ENV as string;
    
    if (!env) {
      throw new Error('VITE_NODE_ENV environment variable is not defined');
    }
    
    if (!(env in configs)) {
      throw new Error(`Invalid environment: "${env}". Valid environments are: ${Object.keys(configs).join(', ')}`);
    }
    
    return env as EnvironmentName;
  };

export const config = configs[getEnvironment()];