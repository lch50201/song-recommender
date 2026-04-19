const record   = document.getElementById('record');
const tonearm  = document.getElementById('tonearm');
const labelTitle  = document.getElementById('label-title');
const labelArtist = document.getElementById('label-artist');

const resultCard  = document.getElementById('result-card');
const loadingEl   = document.getElementById('loading');
const trackInfoEl = document.getElementById('track-info');
const errorEl     = document.getElementById('error-state');
const errorMsg    = document.getElementById('error-msg');

const albumArt      = document.getElementById('album-art');
const trackTitle    = document.getElementById('track-title');
const trackArtist   = document.getElementById('track-artist');
const trackGenreTag = document.getElementById('track-genre-tag');
const trackListeners = document.getElementById('track-listeners');
const lastfmLink    = document.getElementById('lastfm-link');

let activeBtn = null;

function setState(state) {
  loadingEl.classList.toggle('visible', state === 'loading');
  trackInfoEl.classList.toggle('visible', state === 'result');
  errorEl.classList.toggle('visible', state === 'error');
  resultCard.classList.add('visible');
}

function startSpinning() {
  record.classList.add('spinning');
  tonearm.classList.add('playing');
}

function stopSpinning() {
  record.classList.remove('spinning');
  tonearm.classList.remove('playing');
}

async function fetchRecommendation(genre) {
  resultCard.classList.add('visible');
  setState('loading');
  startSpinning();

  try {
    const resp = await fetch('/recommend', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ genre }),
    });

    const data = await resp.json();

    if (!resp.ok || data.error) {
      stopSpinning();
      errorMsg.textContent = data.error || 'Something went wrong.';
      setState('error');
      labelTitle.textContent  = '—';
      labelArtist.textContent = 'error';
      return;
    }

    // Populate card
    trackTitle.textContent    = data.title;
    trackArtist.textContent   = data.artist;
    trackGenreTag.textContent = data.genre;
    trackListeners.textContent = data.listeners !== 'Unknown'
      ? `${data.listeners} listeners` : '';
    lastfmLink.href = data.url;

    if (data.image_url) {
      albumArt.src = data.image_url;
      albumArt.classList.remove('hidden');
    } else {
      albumArt.classList.add('hidden');
    }

    // Update record label
    labelTitle.textContent  = data.title;
    labelArtist.textContent = data.artist;

    setState('result');

  } catch (err) {
    stopSpinning();
    errorMsg.textContent = 'Could not reach the server. Is it running?';
    setState('error');
  }
}

// Genre button clicks
document.querySelectorAll('.genre-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    if (activeBtn) activeBtn.classList.remove('active');
    btn.classList.add('active');
    activeBtn = btn;
    fetchRecommendation(btn.dataset.genre);
  });
});
