import React, { useState, useMemo, useEffect } from 'react';

interface DynamicTableProps {
  data: any[];
}

const DynamicTable: React.FC<DynamicTableProps> = ({ data }) => {
  const [sortConfig, setSortConfig] = useState<{ key: string; direction: 'asc' | 'desc' } | null>(null);
  const [filterText, setFilterText] = useState('');
  const [visible, setVisible] = useState(false);
  const [rowsVisible, setRowsVisible] = useState<boolean[]>([]);

  // If no data, return null
  if (!data || data.length === 0) return null;

  // Get column headers dynamically from first row
  const columns = Object.keys(data[0]);

  // Sorting logic
  const sortedData = useMemo(() => {
    if (!sortConfig) return data;
    return [...data].sort((a, b) => {
      if (a[sortConfig.key] < b[sortConfig.key]) {
        return sortConfig.direction === 'asc' ? -1 : 1;
      }
      if (a[sortConfig.key] > b[sortConfig.key]) {
        return sortConfig.direction === 'asc' ? 1 : -1;
      }
      return 0;
    });
  }, [data, sortConfig]);

  // Filtering logic
  const filteredData = useMemo(() => {
    if (!filterText) return sortedData;
    return sortedData.filter(row => 
      columns.some(column => 
        String(row[column]).toLowerCase().includes(filterText.toLowerCase())
      )
    );
  }, [sortedData, filterText]);

  // Handle sorting
  const handleSort = (key: string) => {
    let direction: 'asc' | 'desc' = 'asc';
    if (sortConfig?.key === key && sortConfig.direction === 'asc') {
      direction = 'desc';
    }
    setSortConfig({ key, direction });
  };

  // Animation effects
  useEffect(() => {
    // Animate the table container
    setVisible(true);
    
    // Animate rows one by one
    const newRowsVisible = Array(filteredData.length).fill(false);
    filteredData.forEach((_, index) => {
      setTimeout(() => {
        setRowsVisible(prev => {
          const updated = [...prev];
          updated[index] = true;
          return updated;
        });
      }, 50 * index); // Stagger the row animations
    });
    
    // Initialize rows visibility array
    setRowsVisible(newRowsVisible);
  }, [filteredData]);

  return (
    <div 
      className={`w-full overflow-x-auto transition-all duration-500 ease-in-out ${
        visible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4'
      }`}
    >
      <div className="mb-4 flex justify-between items-center">
        <input
          type="text"
          placeholder="Filter results..."
          className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-none"
          value={filterText}
          onChange={(e) => setFilterText(e.target.value)}
        />
      </div>
      
      <table className="w-full bg-white shadow-md rounded-lg overflow-hidden">
        <thead className="bg-gray-100">
          <tr>
            {columns.map((column) => (
              <th 
                key={column}
                onClick={() => handleSort(column)}
                className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-200 transition"
              >
                {column}
                {sortConfig?.key === column && (
                  <span className="ml-2">
                    {sortConfig.direction === 'asc' ? '▲' : '▼'}
                  </span>
                )}
              </th>
            ))}
          </tr>
        </thead>
        <tbody className="divide-y divide-gray-200">
          {filteredData.map((row, rowIndex) => (
            <tr 
              key={rowIndex} 
              className={`hover:bg-gray-50 transition-all duration-300 ease-in-out ${
                rowsVisible[rowIndex] ? 'opacity-100 translate-x-0' : 'opacity-0 -translate-x-4'
              }`}
            >
              {columns.map((column) => (
                <td 
                  key={column} 
                  className="px-4 py-3 text-sm text-gray-700"
                >
                  {row[column] !== null && row[column] !== undefined 
                    ? String(row[column]) 
                    : 'N/A'}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
      
      {/* Results count */}
      <div className={`mt-4 text-sm text-gray-600 transition-all duration-500 ease-in-out ${
        visible ? 'opacity-100' : 'opacity-0'
      }`}>
        Showing {filteredData.length} of {data.length} results
      </div>
    </div>
  );
};

export default DynamicTable;