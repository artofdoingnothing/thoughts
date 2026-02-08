import { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import HomePage from './pages/HomePage';
import Thoughts from './pages/Thoughts';
import Personas from './pages/Personas';
import BlogGenerator from './pages/BlogGenerator';
import EssayGenerator from './pages/EssayGenerator';
import CreateThoughtModal from './components/CreateThoughtModal';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

function App() {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [refreshKey, setRefreshKey] = useState(0);

  const handleThoughtCreated = () => {
    setRefreshKey(prev => prev + 1);
    setIsModalOpen(false);
  };

  return (
    <Router>
      <Layout onNewThought={() => setIsModalOpen(true)}>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/thoughts" element={<Thoughts refreshKey={refreshKey} />} />
          <Route path="/personas" element={<Personas />} />
          <Route path="/generate" element={<BlogGenerator />} />
          <Route path="/essay" element={<EssayGenerator />} />
        </Routes>
      </Layout>

      <CreateThoughtModal
        open={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        onSuccess={handleThoughtCreated}
        apiBaseUrl={API_BASE_URL}
      />
    </Router>
  );
}

export default App;
