// components/Dynamictable.tsx
import React, { useState, useMemo, useEffect } from 'react';

interface DynamicTableProps {
  data: any[];
}

const DynamicTable: React.FC<DynamicTableProps> = ({ data }) => {
  const [sortConfig, setSortConfig] = useState<{ key: string; direction: 'asc' | 'desc' } | null>(null);
  const [visible, setVisible] = useState(false);
  const [rowsVisible, setRowsVisible] = useState<boolean[]>([]);
  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 10;

  if (!data || data.length === 0) return null;

  const columns = Object.keys(data[0]);
  
  const columnsWithLargeValues = useMemo(() => {
    const result: Record<string, boolean> = {};
    columns.forEach(column => {
      result[column] = data.some(row => {
        const value = row[column];
        return typeof value === 'string' && value.length > 40;
      });
    });
    return result;
  }, [data, columns]);

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

  const paginatedData = useMemo(() => {
    const startIndex = (currentPage - 1) * itemsPerPage;
    return sortedData.slice(startIndex, startIndex + itemsPerPage);
  }, [sortedData, currentPage]);

  const totalPages = Math.ceil(sortedData.length / itemsPerPage);

  const handleSort = (key: string) => {
    let direction: 'asc' | 'desc' = 'asc';
    if (sortConfig?.key === key && sortConfig.direction === 'asc') {
      direction = 'desc';
    }
    setSortConfig({ key, direction });
  };

  const handlePageChange = (page: number) => {
    setCurrentPage(page);
    const tableElement = document.getElementById('dynamic-table');
    if (tableElement) {
      tableElement.scrollIntoView({ behavior: 'smooth' });
    }
  };

  const renderPaginationButtons = () => {
    const buttons = [];
    
    buttons.push(
      <button
        key="prev"
        onClick={() => currentPage > 1 && handlePageChange(currentPage - 1)}
        disabled={currentPage === 1}
        className={`px-3 py-1 rounded-md ${
          currentPage === 1
            ? 'text-gray-400 cursor-not-allowed'
            : 'text-blue-600 hover:bg-blue-50'
        }`}
        aria-label="Previous page"
      >
        ←
      </button>
    );
    
    const range = 2; // How many pages to show on each side of current page
    let startPage = Math.max(1, currentPage - range);
    let endPage = Math.min(totalPages, currentPage + range);
    
    if (endPage - startPage + 1 < Math.min(5, totalPages)) {
      if (currentPage < totalPages / 2) {
        endPage = Math.min(startPage + 4, totalPages);
      } else {
        startPage = Math.max(1, endPage - 4);
      }
    }
    
    if (startPage > 1) {
      buttons.push(
        <button
          key="1"
          onClick={() => handlePageChange(1)}
          className="px-3 py-1 rounded-md text-blue-600 hover:bg-blue-50"
        >
          1
        </button>
      );
      if (startPage > 2) {
        buttons.push(<span key="start-ellipsis" className="px-2">...</span>);
      }
    }
    
    // Add page numbers
    for (let i = startPage; i <= endPage; i++) {
      buttons.push(
        <button
          key={i}
          onClick={() => handlePageChange(i)}
          className={`px-3 py-1 rounded-md ${
            currentPage === i
              ? 'bg-blue-600 text-white'
              : 'text-blue-600 hover:bg-blue-50'
          }`}
        >
          {i}
        </button>
      );
    }
    
    if (endPage < totalPages) {
      if (endPage < totalPages - 1) {
        buttons.push(<span key="end-ellipsis" className="px-2">...</span>);
      }
      buttons.push(
        <button
          key={totalPages}
          onClick={() => handlePageChange(totalPages)}
          className="px-3 py-1 rounded-md text-blue-600 hover:bg-blue-50"
        >
          {totalPages}
        </button>
      );
    }
    
    buttons.push(
      <button
        key="next"
        onClick={() => currentPage < totalPages && handlePageChange(currentPage + 1)}
        disabled={currentPage === totalPages}
        className={`px-3 py-1 rounded-md ${
          currentPage === totalPages
            ? 'text-gray-400 cursor-not-allowed'
            : 'text-blue-600 hover:bg-blue-50'
        }`}
        aria-label="Next page"
      >
        →
      </button>
    );
    
    return buttons;
  };

  useEffect(() => {
    setVisible(true);
    
    const newRowsVisible = Array(paginatedData.length).fill(false);
    paginatedData.forEach((_, index) => {
      setTimeout(() => {
        setRowsVisible(prev => {
          const updated = [...prev];
          updated[index] = true;
          return updated;
        });
      }, 50 * index);
    });
    
    setRowsVisible(newRowsVisible);
  }, [paginatedData]);

  return (
    <div 
      id="dynamic-table"
      className={`w-full overflow-x-auto transition-all duration-500 ease-in-out ${
        visible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4'
      }`}
    >
      
      <div className="overflow-hidden rounded-xl border border-gray-200 shadow-sm">
        <div className="overflow-x-auto max-h-[70vh]">
          <table className="w-full bg-white divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              {columns.map((column) => (
                <th 
                  key={column}
                  onClick={() => handleSort(column)}
                  className={`group px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100 transition-all ${
                    columnsWithLargeValues[column] ? 'min-w-[200px]' : ''
                  }`}
                >
                  <div className="flex items-center space-x-1">
                    <span>{column}</span>
                    <span className="transition-opacity">
                      {sortConfig?.key === column ? (
                        sortConfig.direction === 'asc' ? 
                          <svg className="w-4 h-4 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 15l7-7 7 7" />
                          </svg> : 
                          <svg className="w-4 h-4 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                          </svg>
                      ) : (
                        <svg className="w-4 h-4 text-gray-400 opacity-0 group-hover:opacity-100" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16V4m0 0L3 8m4-4l4 4m6 0v12m0 0l4-4m-4 4l-4-4" />
                        </svg>
                      )}
                    </span>
                  </div>
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {paginatedData.length > 0 ? (
              paginatedData.map((row, rowIndex) => (
                <tr 
                  key={rowIndex} 
                  className={`hover:bg-gray-50 transition-all duration-300 ease-in-out ${
                    rowsVisible[rowIndex] ? 'opacity-100 translate-x-0' : 'opacity-0 -translate-x-4'
                  }`}
                >
                  {columns.map((column) => (
                    <td 
                      key={column} 
                      className="px-6 py-4 text-sm text-gray-700"
                    >
                      {row[column] !== null && row[column] !== undefined ? (
                        <div className="relative group">
                          <div className="max-w-xs overflow-hidden text-ellipsis">
                            {typeof row[column] === 'string' && row[column].length > 100 ? (
                              <div className="truncate" title={String(row[column])}>
                                {String(row[column])}
                              </div>
                            ) : (
                              <div className={typeof row[column] === 'string' && row[column].length > 40 ? "truncate" : ""} 
                                title={typeof row[column] === 'string' && row[column].length > 40 ? String(row[column]) : ""}>
                                {String(row[column])}
                              </div>
                            )}
                          </div>
                          {typeof row[column] === 'string' && row[column].length > 40 && (
                            <div className="absolute z-10 invisible bg-gray-800 text-white text-xs rounded py-1 px-2 right-0 bottom-full mb-2 group-hover:visible whitespace-normal max-w-sm break-words opacity-0 group-hover:opacity-100 transition-opacity duration-200">
                              {String(row[column])}
                            </div>
                          )}
                        </div>
                      ) : (
                        <span className="text-gray-400">N/A</span>
                      )}
                    </td>
                  ))}
                </tr>
              ))
            ) : (
              <tr>
                <td 
                  colSpan={columns.length} 
                  className="px-6 py-8 text-center text-gray-500"
                >
                  No results found
                </td>
              </tr>
            )}
          </tbody>
        </table>
        </div>
      </div>
      
      {sortedData.length > itemsPerPage && (
        <div className="flex justify-center items-center space-x-1 mt-4 py-2">
          {renderPaginationButtons()}
        </div>
      )}
      
      {sortedData.length > 0 && (
        <div className="mt-2 text-sm text-center text-gray-600">
          Page {currentPage} of {totalPages}
        </div>
      )}
    </div>
  );
};

export default DynamicTable;