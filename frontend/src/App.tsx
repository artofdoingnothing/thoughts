import { useState, useEffect } from 'react'
import axios from 'axios'
import './App.css'

interface Emotion {
  name: string;
  is_generated: boolean;
}

interface Tag {
  name: string;
  is_generated: boolean;
}

interface Thought {
  id: number;
  title: string;
  content: string;
  status: string;
  is_generated: boolean;
  created_at: string;
  updated_at: string;
  emotions: Emotion[];
  tags: Tag[];
  links: number[];
}

interface PaginatedResponse {
  total: number;
  page: number;
  limit: number;
  items: Thought[];
}

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

function App() {
  const [thoughts, setThoughts] = useState<Thought[]>([]);
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [selectedEmotions, setSelectedEmotions] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);

  // Pagination and Search
  const [page, setPage] = useState(1);
  const [total, setTotal] = useState(0);
  const [searchTag, setSearchTag] = useState('');
  const [searchEmotion, setSearchEmotion] = useState('');
  const limit = 5;

  const availableEmotions = ['Happy', 'Sad', 'Angry', 'Anxious', 'Excited', 'Calm'];

  const fetchThoughts = async () => {
    try {
      const params = new URLSearchParams({
        page: page.toString(),
        limit: limit.toString(),
      });
      if (searchTag) params.append('tag', searchTag);
      if (searchEmotion) params.append('emotion', searchEmotion);

      const response = await axios.get<PaginatedResponse>(`${API_BASE_URL}/thoughts/?${params.toString()}`);
      setThoughts(response.data.items);
      setTotal(response.data.total);
    } catch (error) {
      console.error('Error fetching thoughts:', error);
    }
  };

  useEffect(() => {
    fetchThoughts();
    const interval = setInterval(fetchThoughts, 5000); // Poll for updates less frequently
    return () => clearInterval(interval);
  }, [page, searchTag, searchEmotion]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!title || !content) return;

    setLoading(true);
    try {
      await axios.post(`${API_BASE_URL}/thoughts/`, {
        title,
        content,
        emotions: selectedEmotions
      });
      setTitle('');
      setContent('');
      setSelectedEmotions([]);
      fetchThoughts();
    } catch (error) {
      console.error('Error creating thought:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleLink = async (sourceId: number) => {
    const targetIdStr = prompt('Enter Thought ID to link to:');
    if (!targetIdStr) return;
    const targetId = parseInt(targetIdStr);
    if (isNaN(targetId)) return;

    try {
      await axios.post(`${API_BASE_URL}/thoughts/${sourceId}/links`, { target_id: targetId });
      alert('Linked successfully!');
      fetchThoughts();
    } catch (error: any) {
      alert(error.response?.data?.detail || 'Error linking thoughts');
    }
  };

  const toggleEmotion = (emotion: string) => {
    setSelectedEmotions(prev =>
      prev.includes(emotion) ? prev.filter(e => e !== emotion) : [...prev, emotion]
    );
  };

  return (
    <div className="container full-width">
      <h1>Thought Aggregator</h1>

      <div className="layout-grid">
        <div className="creation-section">
          <h2>New Thought</h2>
          <form onSubmit={handleSubmit} className="thought-form">
            <input
              type="text"
              placeholder="Title"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
            />
            <textarea
              placeholder="What's on your mind?"
              value={content}
              onChange={(e) => setContent(e.target.value)}
            />
            <div className="emotion-selector">
              <label>Emotions:</label>
              <div className="emotion-chips">
                {availableEmotions.map(e => (
                  <span
                    key={e}
                    className={`emotion-chip ${selectedEmotions.includes(e) ? 'selected' : ''}`}
                    onClick={() => toggleEmotion(e)}
                  >
                    {e}
                  </span>
                ))}
              </div>
            </div>
            <button type="submit" disabled={loading}>
              {loading ? 'Adding...' : 'Add Thought'}
            </button>
          </form>
        </div>

        <div className="view-section">
          <div className="view-header">
            <h2>Thought Vault</h2>
            <div className="filters">
              <input
                type="text"
                placeholder="Search Tag..."
                value={searchTag}
                onChange={(e) => setSearchTag(e.target.value)}
              />
              <input
                type="text"
                placeholder="Search Emotion..."
                value={searchEmotion}
                onChange={(e) => setSearchEmotion(e.target.value)}
              />
            </div>
          </div>

          <div className="table-container">
            <table className="thoughts-table">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Title</th>
                  <th>Status</th>
                  <th>Type</th>
                  <th>Emotions</th>
                  <th>Tags</th>
                  <th>Links</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {thoughts.map((thought) => (
                  <tr key={thought.id}>
                    <td>{thought.id}</td>
                    <td>
                      <div className="thought-title" title={thought.content}>
                        {thought.title}
                      </div>
                    </td>
                    <td>
                      <span className={`status-badge ${thought.status}`}>
                        {thought.status}
                      </span>
                    </td>
                    <td>{thought.is_generated ? '🤖 Gen' : '👤 Org'}</td>
                    <td>
                      <div className="tag-list">
                        {thought.emotions.map(e => (
                          <span key={e.name} className={`inline-tag emotion ${e.is_generated ? 'generated' : 'manual'}`} title={e.is_generated ? 'Inferred by AI' : 'User Assigned'}>
                            {e.name} {e.is_generated && '🤖'}
                          </span>
                        ))}
                      </div>
                    </td>
                    <td>
                      <div className="tag-list">
                        {thought.tags.map(t => (
                          <span key={t.name} className={`inline-tag tag ${t.is_generated ? 'generated' : 'manual'}`} title={t.is_generated ? 'Inferred by AI' : 'User Assigned'}>
                            {t.name} {t.is_generated && '🤖'}
                          </span>
                        ))}
                      </div>
                    </td>
                    <td>{thought.links.join(', ')}</td>
                    <td>
                      <button className="small-button" onClick={() => handleLink(thought.id)}>
                        Link
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <div className="pagination">
            <button
              disabled={page === 1}
              onClick={() => setPage(p => p - 1)}
            >
              Previous
            </button>
            <span>Page {page} of {Math.ceil(total / limit) || 1}</span>
            <button
              disabled={page * limit >= total}
              onClick={() => setPage(p => p + 1)}
            >
              Next
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

export default App
