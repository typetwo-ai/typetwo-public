// App.tsx
import { useState } from 'react';
import './App.css';
import { Layout, Data } from 'plotly.js';
import Figure from './Figure';
import Table from './Table';

function App() {
  const [query, setQuery] = useState('')
  const [figure, setFigure] = useState<{ data: Data[]; layout: Partial<Layout> } | null>(null);
  const [tableData, setTableData] = useState<any[]>([]);
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    try {
      const response = await fetch('https://beta.typetwo.ai/api/query', { // Local: http://127.0.0.1:5000/api/query, Cloud: https://beta.typetwo.ai/api/query
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query })
      })
      const data = await response.json()
      console.log('API Response:', data);
      setFigure(data.figure)
      setTableData(data.search_results)
    } catch (error) {
      console.error(error)
    }
    setLoading(false)
  }

  return (
    <main className="p-8 mt-12">
      <form className="mb-12 flex gap-2" onSubmit={handleSubmit}>
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          style={{
            padding: '10px 12px',
            border: '1px solid #ccc',
            borderRadius: '4px',
            fontSize: '16px',
            lineHeight: '1.3',
            width: '400px', 
          }}
          placeholder="Enter your query..."
        />
        <button 
          type="submit" 
          className="px-6 bg-blue-500 text-white rounded"
          disabled={loading}
        >
          {loading ? 'Loading...' : 'Enter'}
        </button>
      </form>
      <div className="flex flex-col items-center gap-4">
        <Figure figure={figure} />
        <Table data={tableData} />
      </div>
    </main>
  )
}

export default App