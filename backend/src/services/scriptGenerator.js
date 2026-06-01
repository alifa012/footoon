const buildScriptIdea = ({ theme, players = [], meme, song }) => {
  const safeTheme = theme || 'Unexpected Matchday Drama';
  const leadPlayers = players.length ? players.join(' and ') : 'two rival stars';
  const memeLine = meme || 'a chaotic VAR meme moment';
  const songLine = song || 'an over-the-top stadium anthem';

  return {
    title: `${safeTheme} - FootToon Episode`,
    premise: `${leadPlayers} collide during ${safeTheme.toLowerCase()} while ${memeLine} takes over social media.`,
    generatedScript: [
      `Opening: The commentator introduces ${safeTheme}.`,
      `Conflict: ${leadPlayers} argue over ${memeLine}.`,
      `Twist: Fans remix the drama with ${songLine}.`,
      'Ending: Everyone teams up for a funny training montage and a sequel tease.',
    ].join('\n'),
    tags: [safeTheme, memeLine, songLine].join(', '),
  };
};

module.exports = {
  buildScriptIdea,
};
