"use strict";
// Each published storage key is immutable. Editors create independent copies;
// deleting an acknowledged copy cannot erase another page's later keystrokes.
window.SklibDrafts = class {
  constructor() { this.home = null; this.prefix = ""; this.writer = crypto.randomUUID(); this.records = new Map(); this.owned = new Map(); this.problem = null; }
  connect(home) {
    if (this.home === home) return;
    this.home = home; this.prefix = "sklib.drafts.v1:" + encodeURIComponent(home) + ":";
    this.records.clear(); this.owned.clear(); this.reload();
  }
  valid(record) {
    const v = record?.values;
    return record?.schema === 1 && record.home === this.home && typeof record.id === "string" && /^s_[0-9a-f]{24}$/.test(record.id)
      && typeof record.base_revision === "string" && /^[0-9a-f]{64}$/.test(record.base_revision)
      && typeof record.name === "string" && record.name.length <= 1000 && typeof record.path === "string" && record.path.length <= 4000
      && typeof record.updated_at === "string" && record.updated_at.length < 60
      && v && typeof v.tags === "string" && v.tags.length <= 3000 && typeof v.note === "string" && v.note.length <= 10000
      && typeof v.favorite === "boolean" && ["unreviewed", "to_try", "useful", "not_recommended"].includes(v.state);
  }
  reload() {
    if (!this.home) return;
    const pending = [...this.records.values()].filter(record => !record.persisted);
    try {
      const loaded = new Map(); let invalid = false;
      for (let i = 0; i < localStorage.length; i++) {
        const key = localStorage.key(i);
        if (!key?.startsWith(this.prefix)) continue;
        try {
          const raw = localStorage.getItem(key);
          if (!raw || raw.length > 100000) { invalid = true; continue; }
          const record = JSON.parse(raw);
          if (this.valid(record)) loaded.set(key, {...record, key, persisted: true}); else invalid = true;
        } catch { invalid = true; }
      }
      this.records = loaded;
      for (const record of pending) this.records.set(record.key, record);
      this.problem = invalid ? "部分浏览器草稿无法读取，原记录已保留。可导出草稿后检查。" : null;
    } catch { this.problem = "浏览器存储不可用，草稿只保留在当前页面。请保存记录或导出后再关闭页面。"; }
  }
  all() { return [...this.records.values()].sort((a, b) => b.updated_at.localeCompare(a.updated_at) || b.key.localeCompare(a.key)); }
  get(key) { return this.records.get(key); }
  latest(id) { return this.all().find(record => record.id === id); }
  save(meta, values, baseRevision) {
    const key = this.prefix + meta.id + ":" + this.writer + ":" + crypto.randomUUID();
    const record = {schema: 1, home: this.home, id: meta.id, name: String(meta.name).slice(0, 1000), path: String(meta.path).slice(0, 4000),
      base_revision: baseRevision, values: {...values}, updated_at: new Date().toISOString(), key, persisted: false};
    const previous = this.owned.get(meta.id);
    try {
      if (!this.home || !this.valid(record)) throw new Error("Invalid draft");
      localStorage.setItem(key, JSON.stringify(record)); record.persisted = true;
      this.records.set(key, record); this.owned.set(meta.id, key);
      if (previous) this.remove(previous);
      if (this.problem?.startsWith("草稿写入失败")) this.problem = null;
    } catch {
      this.records.set(key, record); this.owned.set(meta.id, key);
      if (previous && this.records.get(previous)?.persisted === false) this.records.delete(previous);
      this.problem = "草稿写入失败，最新输入只保留在当前页面。浏览器空间可能不足；请保存记录或导出后再关闭页面。";
    }
    return record;
  }
  remove(key) {
    const record = this.records.get(key);
    if (!record) return true;
    try {
      if (record.persisted) localStorage.removeItem(key);
      this.records.delete(key);
      if (this.owned.get(record.id) === key) this.owned.delete(record.id);
      return true;
    } catch { this.problem = "无法清理浏览器草稿，副本仍保留。保存结果不受影响，可稍后重试。"; return false; }
  }
  static same(values, annotation) {
    let tags = annotation?.tags || [];
    if (typeof tags === "string") tags = JSON.parse(tags);
    const rawTags = [...new Set(values.tags.split(/[,，]/).map(tag => tag.trim()).filter(Boolean))];
    return JSON.stringify(rawTags) === JSON.stringify(tags) && values.note === (annotation?.note || "")
      && values.state === (annotation?.state || "unreviewed") && values.favorite === Boolean(annotation?.favorite);
  }
  acknowledge(id, annotation) {
    for (const record of this.all()) if (record.id === id && window.SklibDrafts.same(record.values, annotation)) this.remove(record.key);
  }
  export() {
    const unreadable = [];
    try {
      for (let i = 0; i < localStorage.length; i++) {
        const key = localStorage.key(i);
        if (key?.startsWith(this.prefix) && !this.records.has(key)) unreadable.push({key, raw: localStorage.getItem(key)});
      }
    } catch { unreadable.push({error: "Browser storage could not be read"}); }
    return {schema: 1, home: this.home, exported_at: new Date().toISOString(), drafts: this.all(), unreadable};
  }
};
