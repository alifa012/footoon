function ScriptIdeaBrowser({ generatedScript, savedScripts, onSave, saving }) {
  return (
    <section className="card">
      <h2>Script Idea Browser</h2>
      {generatedScript ? (
        <article className="script-preview">
          <h3>{generatedScript.title}</h3>
          <p>{generatedScript.premise}</p>
          <pre>{generatedScript.generatedScript}</pre>
          <button type="button" onClick={() => onSave(generatedScript)} disabled={saving}>
            {saving ? 'Saving...' : 'Save This Script'}
          </button>
        </article>
      ) : (
        <p>Generate a script idea to preview it here.</p>
      )}

      <h3>Saved Ideas</h3>
      {savedScripts.length ? (
        <ul>
          {savedScripts.map((item) => (
            <li key={item.id}>
              <strong>{item.title}</strong>
              <p>{item.premise}</p>
            </li>
          ))}
        </ul>
      ) : (
        <p>No scripts saved yet.</p>
      )}
    </section>
  );
}

export default ScriptIdeaBrowser;
