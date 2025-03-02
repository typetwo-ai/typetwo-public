// components/Header.tsx
import React from 'react';

const Header: React.FC = () => {
  return (
    <header className="w-full py-6 px-8">
      <div className="container mx-auto">
        <div className="flex items-center gap-3">
          <div className="bg-white p-2 rounded-lg shadow-sm flex items-center justify-center">
            <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="text-indigo-600">
              <ellipse cx="12" cy="5" rx="9" ry="3"></ellipse>
              <path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"></path>
              <path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"></path>
            </svg>
          </div>
          <h1 className="text-3xl font-bold text-gray-800 tracking-tight">TypeTwo</h1>
        </div>
      </div>
    </header>
  );
};

export default Header;