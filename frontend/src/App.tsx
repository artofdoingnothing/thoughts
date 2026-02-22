import { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import HomePage from './pages/Home';
import Thoughts from './pages/Thoughts';
import Personas from './pages/Personas';
import ThoughtGenerator from './pages/ThoughtGenerator';
import EssayGenerator from './pages/EssayGenerator';
import ConversationGenerator from './pages/ConversationGenerator';
import CreateThoughtModal from './pages/Thoughts/components/CreateThoughtModal';
import MovieCharacterSearch from './pages/MovieCharacterSearch';

function App() {
  const [isModalOpen, setIsModalOpen] = useState(false);

  const handleThoughtCreated = () => {
    setIsModalOpen(false);
  };

  return (
    <Router>
      <Layout onNewThought={() => setIsModalOpen(true)}>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/thoughts" element={<Thoughts />} />
          <Route path="/personas" element={<Personas />} />
          <Route path="/generate" element={<ThoughtGenerator />} />
          <Route path="/essay" element={<EssayGenerator />} />
          <Route path="/conversation-generator" element={<ConversationGenerator />} />
          <Route path="/character-search" element={<MovieCharacterSearch />} />
        </Routes>
      </Layout>

      <CreateThoughtModal
        open={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        onSuccess={handleThoughtCreated}
      />
    </Router>
  );
}

export default App;
