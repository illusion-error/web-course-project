/* URL is the committed search state; Back/Forward restores controls and results. */
(() => {
  'use strict';
  const form = document.querySelector('#filters');
  if (!form) return;
  const query = form.elements.q;
  const genre = form.elements.genre;
  const mood = form.elements.mood;
  const cards = [...document.querySelectorAll('.card')];
  const sections = [...document.querySelectorAll('.section')];
  const count = document.querySelector('#result-count');
  const empty = document.querySelector('#no-results');
  const valid = (select, value) => [...select.options].some(o => o.value === value) ? value : '';
  const normalize = value => value.normalize('NFKC').toLowerCase();

  function restore() {
    const params = new URLSearchParams(location.search);
    query.value = (params.get('q') || '').trim().slice(0, 100);
    genre.value = valid(genre, params.get('genre') || '');
    mood.value = valid(mood, params.get('mood') || '');
    let visible = 0;
    for (const card of cards) {
      const matches = normalize(card.dataset.title).includes(normalize(query.value))
        && (!genre.value || card.dataset.genre === genre.value)
        && (!mood.value || card.dataset.moods.split('、').includes(mood.value));
      card.hidden = !matches;
      visible += Number(matches);
    }
    for (const section of sections) {
      const total = [...section.querySelectorAll('.card')].filter(c => !c.hidden).length;
      section.hidden = total === 0;
      section.querySelector('.section-title > span').textContent = `${total} 部作品`;
    }
    count.textContent = `共找到 ${visible} 部作品`;
    empty.hidden = visible !== 0;
    // Normalize unsupported parameters without inserting another history entry.
    writeURL(false, true);
  }

  function writeURL(push, preserveHash = false) {
    const url = new URL(location.href);
    url.search = '';
    if (query.value.trim()) url.searchParams.set('q', query.value.trim().slice(0, 100));
    if (genre.value) url.searchParams.set('genre', genre.value);
    if (mood.value) url.searchParams.set('mood', mood.value);
    if (!preserveHash) url.hash = '';
    if (url.href !== location.href) history[push ? 'pushState' : 'replaceState'](null, '', url);
  }

  form.addEventListener('submit', event => {
    event.preventDefault();
    writeURL(true);
    restore();
  });
  function clear() {
    form.reset();
    writeURL(true);
    restore();
    query.focus();
  }
  document.querySelector('#clear-filters').addEventListener('click', clear);
  document.querySelector('#clear-empty').addEventListener('click', clear);
  window.addEventListener('popstate', restore);
  window.addEventListener('pageshow', restore);
  form.hidden = false;
  restore();
})();
