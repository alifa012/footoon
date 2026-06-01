const test = require('node:test');
const assert = require('node:assert/strict');
const { buildScriptIdea } = require('../src/services/scriptGenerator');

test('buildScriptIdea returns structured script idea', () => {
  const result = buildScriptIdea({
    theme: 'Transfer Deadline Frenzy',
    players: ['Player A', 'Player B'],
    meme: 'Press conference chaos',
    song: 'Viral anthem',
  });

  assert.equal(result.title, 'Transfer Deadline Frenzy - FootToon Episode');
  assert.match(result.generatedScript, /Opening:/);
  assert.match(result.generatedScript, /Ending:/);
});
