function TrendsDashboard({ footballTrends, trendingContent }) {
  return (
    <section className="card">
      <h2>Trends Dashboard</h2>
      <div className="grid">
        <div>
          <h3>Players</h3>
          <ul>{footballTrends.players.map((item) => <li key={item}>{item}</li>)}</ul>
        </div>
        <div>
          <h3>Matches</h3>
          <ul>{footballTrends.matches.map((item) => <li key={item}>{item}</li>)}</ul>
        </div>
        <div>
          <h3>Transfers</h3>
          <ul>{footballTrends.transfers.map((item) => <li key={item}>{item}</li>)}</ul>
        </div>
        <div>
          <h3>Memes & Themes</h3>
          <ul>
            {trendingContent.memes.map((item) => <li key={item}>{item}</li>)}
            {trendingContent.themes.map((item) => <li key={item}>{item}</li>)}
          </ul>
        </div>
      </div>
    </section>
  );
}

export default TrendsDashboard;
