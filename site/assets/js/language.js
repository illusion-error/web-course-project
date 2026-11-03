(() => {
  const link = document.querySelector('[data-language]');
  if (!link) return;
  function syncLink() {
    const target = new URL(link.href);
    target.search = location.search;
    target.hash = location.hash;
    link.href = target.href;
  }
  syncLink();
  window.addEventListener('pageshow', syncLink);
  window.addEventListener('popstate', syncLink);
  window.addEventListener('filters-restored', syncLink);
})();
