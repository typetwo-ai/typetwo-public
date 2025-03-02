// App.tsx
import './App.css';
import Header from './components/Header';
import ParticlesBackground from './components/ParticlesBackground';
import ContentArea from './components/ContentArea';
import SimpleBar from 'simplebar-react';
import 'simplebar-react/dist/simplebar.min.css';

function App() {
  return (
    <SimpleBar style={{ height: '100vh', width: '100%' }} autoHide={false}>
    <div className="min-h-screen flex flex-col bg-gradient-to-br from-blue-50 to-indigo-50 w-full">
      <ParticlesBackground />
      <div className="relative z-10 w-full min-h-screen flex flex-col">
        <Header />
        <ContentArea />
      </div>
    </div>

    </SimpleBar>

  );
}

export default App;