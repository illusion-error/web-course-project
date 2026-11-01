/* Persist only known IDs. A failed write never reports success or changes state. */
(function (root) {
  'use strict';
  function createStore(getStorage, catalog) {
    const key = 'anime-watchlist-v1';
    const valid = new Set(catalog.map(item => item.id));
    let ids = [];
    let readable = true;
    function read() {
      try {
        const raw = getStorage().getItem(key);
        const parsed = raw === null ? [] : JSON.parse(raw);
        if (!Array.isArray(parsed)) throw new Error('invalid data');
        ids = [...new Set(parsed.filter(id => typeof id === 'string' && valid.has(id)))];
        readable = true;
        return '';
      } catch (error) {
        readable = false;
        return '无法读取本地清单：存储可能不可用或数据已损坏。为避免覆盖原记录，本次未修改。请允许站点存储或清理本站损坏的数据后刷新。';
      }
    }
    function save(next) {
      if (!readable) return '清单暂不可修改，请先解决上方的本地存储问题后刷新。';
      const clean = [...new Set(next.filter(id => valid.has(id)))];
      try {
        getStorage().setItem(key, JSON.stringify(clean));
        ids = clean;
        return '';
      } catch (error) {
        return '保存失败：浏览器可能禁止存储或空间不足。本次操作未保存，清单保持原状。';
      }
    }
    return { key, read, save, ids: () => [...ids], readable: () => readable };
  }
  if (typeof module !== 'undefined') module.exports = createStore;
  else root.createWatchlistStore = createStore;
})(typeof window !== 'undefined' ? window : globalThis);
