"use strict";
const assert = require("node:assert/strict");
global.window = globalThis;
if (!global.crypto) Object.defineProperty(global, "crypto", {value: require("node:crypto").webcrypto});
class Storage {
  constructor() { this.data = new Map(); this.fail = false; }
  get length() { return this.data.size; }
  key(i) { return [...this.data.keys()][i] ?? null; }
  getItem(key) { return this.data.get(key) ?? null; }
  setItem(key, value) { if (this.fail) throw new Error("Quota exceeded"); this.data.set(key, value); }
  removeItem(key) { this.data.delete(key); }
}
global.localStorage = new Storage();
require("../sklib/static/drafts.js");
const meta = {id: "s_" + "a".repeat(24), name: "same location", path: "E:/sources/SKILL.md"};
const version = "b".repeat(64), value = note => ({tags: "tools", note, state: "useful", favorite: true});
const one = new SklibDrafts(), two = new SklibDrafts(); one.connect("home A"); two.connect("home A");
one.save(meta, value("page one"), version); two.reload(); two.save(meta, value("page two"), version);
one.reload(); assert.equal(one.all().length, 2);
one.save(meta, value("page one updated"), version); two.reload();
assert.deepEqual(two.all().map(record => record.values.note).sort(), ["page one updated", "page two"]);
one.acknowledge(meta.id, {tags: ["tools"], note: "page one updated", state: "useful", favorite: true});
two.reload(); assert.equal(two.all().length, 1); assert.equal(two.all()[0].values.note, "page two");
const otherLibrary = new SklibDrafts(); otherLibrary.connect("home B"); assert.equal(otherLibrary.all().length, 0);
localStorage.fail = true;
const pending = one.save(meta, value("keep despite quota"), version);
assert.equal(pending.persisted, false); one.reload();
assert(one.export().drafts.some(record => record.values.note === "keep despite quota"));
assert(one.all().some(record => record.values.note === "page two"));
localStorage.fail = false;
localStorage.setItem(one.prefix + "corrupt", "{invalid JSON"); one.reload();
assert(one.problem); assert(one.export().unreadable.some(record => record.raw === "{invalid JSON"));
assert.equal(localStorage.getItem(one.prefix + "corrupt"), "{invalid JSON");
console.log("Draft copies, library isolation, acknowledged cleanup, quota recovery and corrupt-record export passed.");
