// App.tsx
import Header from './components/Header';
import ParticlesBackground from './components/ParticlesBackground';
import ContentArea from './components/ContentArea';
import SimpleBar from 'simplebar-react';
import 'simplebar-react/dist/simplebar.min.css';

const App: React.FC = () => (
  <SimpleBar style={{ height: '100vh', width: '100%' }} autoHide={false}>
    <div className="min-h-screen flex flex-col w-full">
      <ParticlesBackground />
      <div className="relative z-10 w-full min-h-screen flex flex-col">
        <div className="max-w-screen-2xl mx-auto px-6 sm:px-8 w-full">
          <Header />
        </div>
        <div className="max-w-screen-lg mx-auto px-4 sm:px-6 w-full">
          <ContentArea />
        </div>
      </div>
    </div>
  </SimpleBar>
);

export default App;