// App.tsx
import './App.css';
import Header from './components/Header';
import ParticlesBackground from './components/ParticlesBackground';
import ContentArea from './components/ContentArea';

function App() {
  return (
    <div className="min-h-screen flex flex-col bg-gradient-to-br from-blue-50 to-indigo-50 w-full">
      <ParticlesBackground />
      <div className="relative z-10 w-full min-h-screen flex flex-col">
        <Header />
        <ContentArea />
      </div>
    </div>
  );
}

export default App;