(() => {
  'use strict';
  const catalog = window.ANIME_CATALOG;
  const store = window.createWatchlistStore(() => window.localStorage, catalog);
  const feedback = document.querySelector('#save-feedback');
  const panel = document.querySelector('#watchlist-panel');
  const grid = document.querySelector('#saved-grid');
  const confirmation = document.querySelector('#clear-confirm');
  const clearButton = document.querySelector('#clear-list');
  function message(text, error = false) {
    feedback.textContent = text;
    feedback.classList.toggle('save-error', error);
  }
  function button(item, saved, remove = false) {
    const node = document.createElement('button');
    node.type = 'button';
    node.className = 'save-button';
    node.dataset.save = item.id;
    node.textContent = remove ? '移除' : saved ? '已加入 · 取消想看' : '加入想看';
    node.setAttribute('aria-label', `${node.textContent}：${item.title}`);
    node.setAttribute('aria-pressed', String(saved));
    return node;
  }
  function render() {
    const ids = store.ids();
    document.querySelectorAll('[data-save]').forEach(node => {
      const item = catalog.find(item => item.id === node.dataset.save);
      if (!item) return;
      const state = button(item, ids.includes(item.id));
      node.textContent = state.textContent;
      node.setAttribute('aria-label', state.getAttribute('aria-label'));
      node.setAttribute('aria-pressed', state.getAttribute('aria-pressed'));
      node.hidden = false;
      node.disabled = !store.readable();
    });
    if (!panel) return;
    panel.hidden = false;
    grid.replaceChildren();
    for (const id of ids) {
      const item = catalog.find(item => item.id === id);
      const card = document.createElement('article');
      card.className = 'card saved-card';
      const label = document.createElement('p');
      label.className = 'eyebrow';
      label.textContent = item.genre;
      const heading = document.createElement('h3');
      const link = document.createElement('a');
      link.href = item.path;
      link.textContent = item.title;
      heading.append(link);
      const summary = document.createElement('p');
      summary.textContent = item.summary;
      const remove = button(item, true, true);
      remove.disabled = !store.readable();
      card.append(label, heading, summary, remove);
      grid.append(card);
    }
    document.querySelector('#saved-count').textContent = store.readable() ? `我的想看清单 · ${ids.length} 部` : '清单暂时无法读取';
    document.querySelector('#saved-empty').hidden = ids.length !== 0 || !store.readable();
    clearButton.disabled = !ids.length || !store.readable();
  }
  function sync() {
    const error = store.read();
    render();
    message(error, Boolean(error));
  }
  document.addEventListener('click', event => {
    const node = event.target.closest('[data-save]');
    if (!node) return;
    const item = catalog.find(item => item.id === node.dataset.save);
    if (!item) return;
    const error = store.read();
    if (error) { render(); message(error, true); return; }
    const ids = store.ids();
    const removing = ids.includes(item.id);
    const failure = store.save(removing ? ids.filter(id => id !== item.id) : [...ids, item.id]);
    render();
    message(failure || `《${item.title}》${removing ? '已移出清单' : '已加入想看'}。`, Boolean(failure));
    if (panel) document.querySelector('#saved-count').focus();
  });
  if (panel) {
    clearButton.addEventListener('click', () => {
      confirmation.hidden = false;
      document.querySelector('#cancel-clear').focus();
    });
    function cancel() { confirmation.hidden = true; clearButton.focus(); }
    document.querySelector('#cancel-clear').addEventListener('click', cancel);
    confirmation.addEventListener('keydown', event => { if (event.key === 'Escape') cancel(); });
    document.querySelector('#confirm-clear').addEventListener('click', () => {
      const error = store.read() || store.save([]);
      confirmation.hidden = true;
      render();
      message(error || '想看清单已清空。', Boolean(error));
      document.querySelector('#saved-count').focus();
    });
  }
  window.addEventListener('pageshow', sync);
  window.addEventListener('storage', event => {
    if (event.key === store.key || event.key === null) {
      if (confirmation) confirmation.hidden = true;
      sync();
    }
  });
  sync();
})();
