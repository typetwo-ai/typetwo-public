// App.tsx
import './App.css';
import Landing from './components/Landing';
import Header from './components/Header';

function App() {
  return (
    <div className="min-h-screen flex flex-col bg-gradient-to-br from-blue-50 to-indigo-50 w-full">
      <Header />
      <Landing />
    </div>
  )
}

export default App