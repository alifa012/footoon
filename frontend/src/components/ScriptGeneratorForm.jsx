import { useState } from 'react';

const defaultForm = {
  theme: '',
  players: '',
  meme: '',
  song: '',
};

function ScriptGeneratorForm({ onGenerate, loading }) {
  const [form, setForm] = useState(defaultForm);

  const handleChange = (event) => {
    const { name, value } = event.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    onGenerate({
      theme: form.theme,
      players: form.players
        .split(',')
        .map((item) => item.trim())
        .filter(Boolean),
      meme: form.meme,
      song: form.song,
    });
  };

  return (
    <section className="card">
      <h2>Script Generator</h2>
      <form className="form" onSubmit={handleSubmit}>
        <label>
          Theme
          <input name="theme" value={form.theme} onChange={handleChange} placeholder="e.g. Derby Day Banter" />
        </label>
        <label>
          Players (comma separated)
          <input name="players" value={form.players} onChange={handleChange} placeholder="Player 1, Player 2" />
        </label>
        <label>
          Meme trigger
          <input name="meme" value={form.meme} onChange={handleChange} placeholder="e.g. VAR dance" />
        </label>
        <label>
          Song vibe
          <input name="song" value={form.song} onChange={handleChange} placeholder="e.g. stadium remix" />
        </label>
        <button type="submit" disabled={loading}>{loading ? 'Generating...' : 'Generate Script Idea'}</button>
      </form>
    </section>
  );
}

export default ScriptGeneratorForm;
