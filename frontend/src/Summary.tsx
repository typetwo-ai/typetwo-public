// Summary.tsx
import React from 'react';

interface SummaryProps {
  text: string;
}

const Summary: React.FC<SummaryProps> = ({ text }) => {
  if (!text) return null;

  return (
    <div className="w-full max-w-2xl p-4 border rounded shadow-sm bg-gray-100">
      <p className="mt-2 text-gray-700">{text}</p>
    </div>
  );
};

export default Summary;
