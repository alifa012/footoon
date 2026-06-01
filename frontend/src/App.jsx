import { useEffect, useMemo, useState } from 'react';
import './App.css';
import TrendsDashboard from './components/TrendsDashboard';
import ScriptGeneratorForm from './components/ScriptGeneratorForm';
import ScriptIdeaBrowser from './components/ScriptIdeaBrowser';
import {
  fetchFootballTrends,
  fetchTrendingContent,
  fetchSavedScripts,
  generateScript,
  saveScript,
} from './services/api';

const emptyTrends = { players: [], matches: [], transfers: [] };
const emptyContent = { memes: [], themes: [], songs: [] };

function App() {
  const [footballTrends, setFootballTrends] = useState(emptyTrends);
  const [trendingContent, setTrendingContent] = useState(emptyContent);
  const [savedScripts, setSavedScripts] = useState([]);
  const [generatedScript, setGeneratedScript] = useState(null);
  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState('');

  const hasData = useMemo(
    () => footballTrends.players.length || trendingContent.memes.length,
    [footballTrends.players.length, trendingContent.memes.length],
  );

  useEffect(() => {
    const load = async () => {
      try {
        const [football, trends, scripts] = await Promise.all([
          fetchFootballTrends(),
          fetchTrendingContent(),
          fetchSavedScripts(),
        ]);
        setFootballTrends(football);
        setTrendingContent(trends);
        setSavedScripts(scripts);
      } catch (loadError) {
        setError(loadError.message);
      }
    };

    load();
  }, []);

  const handleGenerate = async (payload) => {
    setLoading(true);
    setError('');

    try {
      const result = await generateScript(payload);
      setGeneratedScript(result);
    } catch (generateError) {
      setError(generateError.message);
    } finally {
      setLoading(false);
    }
  };

  const handleSave = async (script) => {
    setSaving(true);
    setError('');

    try {
      const saved = await saveScript(script);
      setSavedScripts((prev) => [saved, ...prev]);
    } catch (saveError) {
      setError(saveError.message);
    } finally {
      setSaving(false);
    }
  };

  return (
    <main className="container">
      <header>
        <h1>FootToon Idea Generator</h1>
        <p>Turn live football trends into cartoon-ready script ideas.</p>
      </header>

      {error ? <p className="error">{error}</p> : null}
      {!hasData ? <p>Loading trend feeds...</p> : null}

      <TrendsDashboard footballTrends={footballTrends} trendingContent={trendingContent} />
      <ScriptGeneratorForm onGenerate={handleGenerate} loading={loading} />
      <ScriptIdeaBrowser
        generatedScript={generatedScript}
        savedScripts={savedScripts}
        onSave={handleSave}
        saving={saving}
      />
    </main>
  );
}

export default App;
