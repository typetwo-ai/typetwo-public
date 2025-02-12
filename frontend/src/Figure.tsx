// Figure.tsx
import React from 'react';
import Plot from 'react-plotly.js';
import { Layout, Data } from 'plotly.js';

interface FigureProps {
  figure: { data: Data[]; layout: Partial<Layout> } | null;
}

const Figure: React.FC<FigureProps> = ({ figure }) => {
  if (!figure) {
    return <div>No figure to display.</div>;
  }

  return (
    <div className="w-full border rounded mx-auto">
      <Plot
        data={figure.data}
        layout={figure.layout}
        config={{ responsive: true }}
      />
    </div>
  );
};

export default Figure;