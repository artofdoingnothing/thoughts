import { useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import { Box, Pagination, Stack, Typography, LinearProgress } from '@mui/material';
import Layout from './components/Layout';
import FilterBar from './components/FilterBar';
import ThoughtTable from './components/ThoughtTable';
import CreateThoughtModal from './components/CreateThoughtModal';
import type { Thought, PaginatedResponse } from './types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

function App() {
  const [thoughts, setThoughts] = useState<Thought[]>([]);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [loading, setLoading] = useState(false);

  // Pagination and Search
  const [page, setPage] = useState(1);
  const [total, setTotal] = useState(0);
  const [searchTag, setSearchTag] = useState('');
  const [searchEmotion, setSearchEmotion] = useState('');
  const limit = 10;

  // Expanded Rows State
  const [expandedThoughtIds, setExpandedThoughtIds] = useState<Set<number>>(new Set());

  const fetchThoughts = useCallback(async () => {
    setLoading(true);
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
    } finally {
      setLoading(false);
    }
  }, [page, searchTag, searchEmotion]);

  useEffect(() => {
    fetchThoughts();
    const interval = setInterval(fetchThoughts, 10000);
    return () => clearInterval(interval);
  }, [fetchThoughts]);

  const handleDelete = async (id: number) => {
    if (!confirm('Are you sure you want to delete this thought?')) return;
    try {
      await axios.delete(`${API_BASE_URL}/thoughts/${id}`);
      fetchThoughts();
    } catch (error) {
      console.error('Error deleting thought:', error);
      alert('Failed to delete thought');
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
    } catch (error) {
      const msg = axios.isAxiosError(error) ? error.response?.data?.detail : 'Error linking thoughts';
      alert(msg || 'Error linking thoughts');
    }
  };

  const toggleExpand = (id: number) => {
    const newExpanded = new Set(expandedThoughtIds);
    if (newExpanded.has(id)) {
      newExpanded.delete(id);
    } else {
      newExpanded.add(id);
    }
    setExpandedThoughtIds(newExpanded);
  };

  return (
    <Layout onNewThought={() => setIsModalOpen(true)}>
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" sx={{ mb: 2, fontWeight: 'bold', color: 'primary.main' }}>
          MY THOUGHTS
        </Typography>
        <Typography variant="body1" color="text.secondary" sx={{ mb: 3 }}>
          Aggregating your stream of consciousness.
        </Typography>

        {loading && <LinearProgress sx={{ mb: 2 }} />}

        <FilterBar
          searchTag={searchTag}
          setSearchTag={setSearchTag}
          searchEmotion={searchEmotion}
          setSearchEmotion={setSearchEmotion}
        />

        <ThoughtTable
          thoughts={thoughts}
          expandedThoughtIds={expandedThoughtIds}
          toggleExpand={toggleExpand}
          onLink={handleLink}
          onDelete={handleDelete}
        />

        <Stack spacing={2} sx={{ mt: 4, alignItems: 'center' }}>
          <Pagination
            count={Math.ceil(total / limit) || 1}
            page={page}
            onChange={(_, p) => setPage(p)}
            color="primary"
            showFirstButton
            showLastButton
          />
        </Stack>
      </Box>

      <CreateThoughtModal
        open={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        onSuccess={() => {
          fetchThoughts();
          setIsModalOpen(false);
        }}
        apiBaseUrl={API_BASE_URL}
      />
    </Layout>
  );
}

export default App;
