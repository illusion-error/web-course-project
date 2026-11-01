const test = require('node:test');
const assert = require('node:assert/strict');
const create = require('../site/assets/js/watchlist-store.js');
const catalog = [{id:'one'},{id:'two'}];
function fixture(raw=null) { let value=raw; const storage={getItem:()=>value,setItem:(_,v)=>{value=v;}}; return {storage,store:create(()=>storage,catalog),value:()=>value}; }
test('save, deduplicate, reload, remove and clear',()=>{const f=fixture();assert.equal(f.store.read(),'');assert.equal(f.store.save(['one','two','one']),'');assert.deepEqual(JSON.parse(f.value()),['one','two']);const reload=create(()=>f.storage,catalog);reload.read();assert.deepEqual(reload.ids(),['one','two']);reload.save(['two']);assert.deepEqual(JSON.parse(f.value()),['two']);reload.save([]);assert.equal(f.value(),'[]');});
test('unknown IDs and non-string values never become cards',()=>{const f=fixture('["one","evil",{},"one",null]');assert.equal(f.store.read(),'');assert.deepEqual(f.store.ids(),['one']);});
test('corrupt JSON and wrong shape block overwrite',()=>{for(const raw of ['{broken','{}']) {const f=fixture(raw);assert.ok(f.store.read());assert.ok(f.store.save([]));assert.equal(f.value(),raw);}});
test('denied reads are handled',()=>{const s=create(()=>{throw Error('denied');},catalog);assert.ok(s.read());assert.equal(s.readable(),false);});
test('quota failures retain saved state',()=>{const f=fixture('["one"]');f.store.read();f.storage.setItem=()=>{throw Error('quota');};assert.ok(f.store.save(['two']));assert.deepEqual(f.store.ids(),['one']);assert.equal(f.value(),'["one"]');});
