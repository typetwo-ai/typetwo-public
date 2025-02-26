// Table.tsx
import React from 'react';
import './Table.css';

interface TableProps {
  data: any[];
}

const Table: React.FC<TableProps> = ({ data }) => {
  if (!data || data.length === 0) {
    return <div>No data to display.</div>;
  }

  const headers = Object.keys(data[0]);

  return (
    <div className="border rounded overflow-x-auto">
      <table className="mx-auto">
        <thead>
          <tr>
            {headers.map((key) => (
              <th key={key}>{key.replace(/_/g, ' ').toUpperCase()}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.map((row, rowIndex) => (
            <tr key={rowIndex}>
              {headers.map((key, colIndex) => (
                <td key={colIndex}>{row[key] === null ? 'N/A' : row[key]?.toString()}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default Table;