"use strict";
const $ = id => document.getElementById(id);
const token = document.querySelector('meta[name="sklib-token"]').content;
let selected = null, selectionSerial = 0, searchSerial = 0, offset = 0, nextOffset = null, controller = null;
let offsetHistory = [];
let displayedOffset = 0, displayedHistory = [];
let resource = null, resourceSerial = 0;
let previewToken = null;
let recordsSerial = 0;
let jobTimer = null, jobsLoading = false, jobsRefreshRequested = false;
const observedJobs = new Map(), trackedJobs = new Set();
const noteDrafts = new Map();
const draftStore = new SklibDrafts();
const picked = new Map();
const stateNames = {unreviewed: "待了解", to_try: "待试用", useful: "常用", not_recommended: "暂不推荐"};
let currentResults = [], batchBusy = false, searchLoading = false, draftLimit = 20;
let detailLoading = false, noteSaving = false, homeMismatch = false, desiredDetailTab = "content";
function updateNoteControls() {
  const blocked = detailLoading || homeMismatch || !draftStore.home;
  document.querySelectorAll("#notes-panel input,#notes-panel select,#notes-panel textarea").forEach(el => { el.disabled = blocked; });
  $("note-save").disabled = blocked || noteSaving; $("note-rebase").disabled = blocked || noteSaving;
}
function draftValues() { return {tags: $("note-tags").value, note: $("note-text").value, state: $("note-state").value, favorite: $("note-favorite").checked}; }
function rememberNoteDraft() {
  if (!selected) return;
  const base = noteDrafts.get(selected.id)?.base_revision || selected.annotation_revision;
  noteDrafts.set(selected.id, draftStore.save(selected, draftValues(), base));
  updateDraftUi(); showNoteConflict();
}
$("notes-panel").addEventListener("input", rememberNoteDraft);
$("notes-panel").addEventListener("change", rememberNoteDraft);
function fillNotes(annotation) {
  let tags = annotation?.tags || [];
  if (typeof tags === "string") tags = JSON.parse(tags);
  $("note-tags").value = tags.join(", "); $("note-text").value = annotation?.note || "";
  $("note-state").value = annotation?.state || "unreviewed"; $("note-favorite").checked = Boolean(annotation?.favorite);
}
function showNoteConflict() {
  const draft = selected && noteDrafts.get(selected.id);
  const conflict = draft && draft.base_revision !== selected.annotation_revision;
  $("note-conflict").hidden = !conflict;
  if (conflict) {
    const value = selected.annotation || {}; let tags = value.tags || [];
    if (typeof tags === "string") tags = JSON.parse(tags);
    $("note-current").textContent = `当前标签：${tags.join(", ") || "无"}\n当前状态：${stateNames[value.state || "unreviewed"]}\n当前收藏：${value.favorite ? "是" : "否"}\n当前笔记：\n${value.note || "（空）"}`;
  }
}
function updateDraftUi() {
  $("drafts-toggle").textContent = `草稿箱 ${draftStore.records.size}`;
  const draft = selected && noteDrafts.get(selected.id);
  $("draft-status").className = draft && !draft.persisted ? "warning" : "path";
  $("draft-status").textContent = !draftStore.home ? "正在确认资料库位置，请稍候…" : draft ? (draft.persisted ? "草稿已保存在此浏览器，尚未保存到资料库。" : draftStore.problem || "最新草稿只保留在当前页面，请保存或导出。") : "";
  $("draft-storage-warning").textContent = draftStore.problem || ""; $("draft-storage-warning").hidden = !draftStore.problem;
  if (!$("draft-box").hidden) renderDraftBox();
}
function renderDraftBox() {
  const records = draftStore.all(); $("draft-list").replaceChildren();
  for (const record of records.slice(0, draftLimit)) {
    const card = text("article", "", "draft-card");
    card.append(text("h3", record.name), text("p", `${record.updated_at} · ${record.path}`, "path"), text("p", `标签：${record.values.tags || "无"} · 状态：${stateNames[record.values.state]} · 收藏：${record.values.favorite ? "是" : "否"}`));
    const body = document.createElement("textarea"); body.readOnly = true; body.rows = 4; body.value = record.values.note; body.setAttribute("aria-label", "草稿笔记内容"); card.append(body);
    const restore = text("button", "打开并恢复此副本"); restore.addEventListener("click", async () => { if (await select(record.id, record.key)) tab("notes"); });
    const discard = text("button", "删除此草稿副本"); discard.addEventListener("click", () => {
      if (!draftStore.remove(record.key)) { updateDraftUi(); return; }
      if (noteDrafts.get(record.id)?.key === record.key) {
        noteDrafts.delete(record.id);
        if (selected?.id === record.id) { fillNotes(selected.annotation); showNoteConflict(); }
      }
      updateDraftUi();
    });
    card.append(restore, discard); $("draft-list").append(card);
  }
  if (records.length > draftLimit) { const more = text("button", `显示更多草稿（共 ${records.length} 份）`); more.addEventListener("click", () => { draftLimit += 20; renderDraftBox(); }); $("draft-list").append(more); }
  if (!records.length) $("draft-list").append(text("p", "当前资料库没有浏览器草稿。", "path"));
}
$("drafts-toggle").addEventListener("click", () => { $("draft-box").hidden = !$("draft-box").hidden; draftStore.reload(); updateDraftUi(); });
$("drafts-export").addEventListener("click", () => {
  const url = URL.createObjectURL(new Blob([JSON.stringify(draftStore.export(), null, 2)], {type: "application/json"}));
  const link = document.createElement("a"); link.href = url; link.download = "sklib-drafts.json"; link.click(); setTimeout(() => URL.revokeObjectURL(url), 1000);
});
$("note-rebase").addEventListener("click", () => {
  if (!selected) return;
  noteDrafts.set(selected.id, draftStore.save(selected, draftValues(), selected.annotation_revision)); updateDraftUi(); showNoteConflict();
});
let draftEventTimer;
window.addEventListener("storage", event => {
  if (event.key && !event.key.startsWith(draftStore.prefix)) return;
  clearTimeout(draftEventTimer); draftEventTimer = setTimeout(() => { draftStore.reload(); updateDraftUi(); }, 100);
});
let recordsBusy = false;
function recordsWorking(busy) { recordsBusy = busy; for (const action of ["init", "preview", "log", "status"]) $("records-" + action).disabled = busy; }
function invalidatePreview() { ++recordsSerial; previewToken = null; $("commit-button").disabled = true; }
function notice(message, error = false) { $("notice").textContent = message; $("notice").className = error ? "error" : ""; $("notice").hidden = false; }
async function api(path, data, signal) {
  if (data !== undefined && homeMismatch) throw new Error("资料库位置已变化。请先导出当前草稿，然后刷新页面再操作。");
  if (data !== undefined && (["/api/annotate", "/api/annotate-batch", "/api/index", "/api/remove-root"].includes(path) || path.startsWith("/api/index-jobs") || /\/api\/records\/(import|migrate)-/.test(path))) invalidatePreview();
  let response;
  try { response = await fetch(path, {signal, ...(data === undefined ? {} : {method: "POST", headers: {"Content-Type": "application/json", "X-Sklib-Token": token}, body: JSON.stringify(data)})}); }
  catch (err) {
    if (err.name === "AbortError") throw err;
    throw new Error(data === undefined ? "无法连接本地服务。服务恢复后可重试读取。" : "连接中断，操作结果尚未确认。请先检查当前状态或提交历史，再决定是否重试；输入内容仍保留。");
  }
  let result;
  try { result = await response.json(); }
  catch { throw new Error(data === undefined ? "服务返回了无法解析的响应，请检查服务后重试读取。" : "服务响应无法解析，操作结果尚未确认。先检查当前状态或提交历史；输入内容仍保留。"); }
  if (!response.ok) { const error = new Error((result.error || "请求失败") + (result.recovery ? " · " + result.recovery : "")); error.details = result; throw error; }
  return result;
}
function text(tag, content, cls) { const el = document.createElement(tag); el.textContent = content; if (cls) el.className = cls; return el; }
function showView(view) {
  for (const name of ["library", "sources", "records"]) $("view-" + name).hidden = name !== view;
  document.querySelectorAll(".nav").forEach(el => el.classList.toggle("active", el.dataset.view === view));
  $("view-title").textContent = {library: "找到下一步的做法。", sources: "每一项能力，都有来处。", records: "把经验留给下一次。"}[view];
  if (view === "records") loadHistory();
}
document.querySelectorAll(".nav").forEach(el => el.addEventListener("click", () => showView(el.dataset.view)));
async function refreshStatus() {
  const data = await api("/api/status");
  if (draftStore.home && draftStore.home !== data.home) { homeMismatch = true; updateNoteControls(); throw new Error("资料库位置已变化。原库草稿保留，请导出后刷新页面。"); }
  draftStore.connect(data.home); updateDraftUi(); updateNoteControls();
  $("summary").textContent = `${data.counts.skill || 0} 个技能 · ${data.counts.project || 0} 项项目资料 · ${data.roots.length} 个来源`;
  $("home-label").textContent = data.home;
  document.dispatchEvent(new CustomEvent("sklib-status", {detail: data}));
  const previousRoot = $("root-filter").value;
  $("root-filter").replaceChildren(new Option("全部来源", ""));
  for (const root of data.roots) $("root-filter").append(new Option(root.path, root.path));
  $("root-filter").value = data.roots.some(root => root.path === previousRoot) ? previousRoot : "";
  $("source-list").replaceChildren();
  for (const root of data.roots) {
    const card = text("article", "", "source-card");
    const report = root.last_report;
    card.append(text("h3", root.path), text("p", `最近扫描 ${root.scanned_at} · 新增 ${report.added} · 更新 ${report.updated} · 未变化 ${report.unchanged} · 移除 ${report.removed}`));
    if (!report.complete) card.append(text("p", "扫描未完整完成，保留了未确认丢失的索引记录。"));
    if (report.failures?.length) card.append(text("p", report.failures.slice(0, 3).map(item => `${item.path} · ${item.error} · ${item.recovery}`).join("\n")));
    else if (report.errors.length) card.append(text("p", report.errors.slice(0, 3).join("\n")));
    if (report.failure_count > 3) card.append(text("p", `共 ${report.failure_count} 项失败，此处显示前 3 项。修正原因后可重新扫描。`));
    const refresh = text("button", "重新扫描");
    refresh.addEventListener("click", () => {
      $("source-root").value = root.path;
      $("include-docs").checked = Boolean(report.options?.include_docs);
      $("source-encoding").value = report.options?.encoding === "utf-8" ? "auto" : report.options?.encoding || "auto";
      $("index-form").requestSubmit();
    });
    const remove = text("button", "移除索引来源");
    remove.addEventListener("click", async () => { try { await api("/api/remove-root", {root: root.path}); notice("来源已移出索引，原文件和个人笔记保留。"); invalidatePreview(); await refreshStatus(); await search(); } catch (err) { notice(err.message, true); } });
    card.append(refresh, remove); $("source-list").append(card);
  }
  if (!data.roots.length) $("source-list").append(text("p", "尚未添加来源。输入资料目录后开始扫描。", "path"));
  if (!data.documents) notice("技能库还是空的。请在“资料来源”中添加本地目录。");
  return data;
}
async function search(reset = true) {
  const requiredTerms = $("required-terms").value.split(/[,，]/).map(value => value.trim()).filter(Boolean);
  const query = $("query").value.trim() || requiredTerms.join(" ");
  if (reset) { offset = 0; offsetHistory = []; if (!batchBusy) { picked.clear(); updatePicks(); } }
  if (controller) controller.abort(); controller = new AbortController();
  const serial = ++searchSerial;
  searchLoading = true; $("pick-page").disabled = true;
  $("result-meta").textContent = "正在检索…";
  document.querySelectorAll(".result").forEach(button => { button.disabled = true; });
  document.querySelectorAll(".bulk-pick").forEach(check => { check.disabled = true; });
  const params = new URLSearchParams({q: query, kind: $("kind").value, queue: $("queue").value, sort: $("catalog-sort").value, root: $("root-filter").value, project_type: $("project-type").value, state: $("state").value, tags: $("tag-filter").value, favorite: $("favorite-filter").checked, offset, limit: 10});
  if (requiredTerms.length) params.set("required_terms", requiredTerms.join(","));
  try {
    const data = await api((query ? "/api/search?" : "/api/browse?") + params, undefined, controller.signal);
    if (serial !== searchSerial) return;
    searchLoading = false; $("pick-page").disabled = batchBusy;
    if (!query && data.total > 0 && data.returned === 0 && offset > 0) { offset = offsetHistory.pop() ?? 0; return search(false); }
    $("results").replaceChildren(); nextOffset = data.next_offset; currentResults = data.results;
    displayedOffset = offset; displayedHistory = [...offsetHistory];
    $("result-meta").textContent = `${data.returned} 项${data.total === undefined ? "" : ` / 共 ${data.total} 条位置记录`} · ${data.elapsed_ms} ms`;
    $("queue-summary").textContent = data.counts ? `当前范围：未分类 ${data.counts.unclassified} · 待复核 ${data.counts.needs_review} · 有警告 ${data.counts.warnings} · 重复位置 ${data.counts.duplicates}。可直接选择条目设置标签和状态。` : "关键词检索按相关性排序；清空关键词和必含词可浏览并分拣全部条目。";
    $("catalog-sort").disabled = Boolean(query);
    $("previous").disabled = offset === 0; $("next").disabled = nextOffset === null;
    for (const item of data.results) {
      const row = text("div", "", "result-row"), check = document.createElement("input"); check.type = "checkbox"; check.className = "bulk-pick";
      check.dataset.id = item.id; check.checked = picked.has(item.id); check.disabled = batchBusy || !item.annotation_revision;
      check.setAttribute("aria-label", "选择 " + item.name + " " + (item.path || item.id));
      check.addEventListener("change", () => { if (check.checked && !picked.has(item.id) && picked.size >= 100) { check.checked = false; notice("最多选择 100 项。", true); return; } if (check.checked) picked.set(item.id, item); else picked.delete(item.id); updatePicks(); });
      const button = text("button", "", "result"); button.dataset.id = item.id;
      const head = text("div", "", "result-head"); head.append(text("h3", item.name), text("span", item.kind.toUpperCase(), "type"));
      button.append(head, text("p", item.description), text("p", item.evidence.text, "evidence"), text("div", `${item.favorite ? "★ · " : ""}${item.tags.join(" / ") || "未分类"}${item.duplicate_count ? ` · 另有 ${item.duplicate_count} 个相同内容` : ""}`, "result-foot"));
      button.addEventListener("click", () => select(item.id)); row.append(check, button); $("results").append(row);
    }
    if (!data.results.length) {
      const empty = text("div", "", "empty"); empty.append(text("h3", "暂时没有匹配结果"), text("p", "检查关键词、必含词和筛选条件，或确认资料来源是否已加入索引。")); $("results").append(empty);
    }
  } catch (err) { if (serial === searchSerial && err.name !== "AbortError") { searchLoading = false; offset = displayedOffset; offsetHistory = [...displayedHistory]; $("result-meta").textContent = "检索失败，仍显示上次结果"; document.querySelectorAll(".result").forEach(button => { button.disabled = false; }); updatePicks(); $("previous").disabled = true; $("next").disabled = true; notice(err.message, true); } }
}
$("search-form").addEventListener("submit", e => { e.preventDefault(); search(); });
for (const id of ["state", "favorite-filter", "tag-filter", "required-terms", "queue", "catalog-sort", "root-filter"]) $(id).addEventListener("change", () => search());
$("kind").addEventListener("change", () => { if ($("kind").value !== "project" && $("kind").value !== "all") $("project-type").value = ""; search(); });
$("project-type").addEventListener("change", () => { if ($("project-type").value) $("kind").value = "project"; search(); });
$("previous").addEventListener("click", () => { offset = offsetHistory.pop() ?? 0; search(false); });
$("next").addEventListener("click", () => { if (nextOffset !== null) { offsetHistory.push(offset); offset = nextOffset; search(false); } });
function updatePicks() {
  $("pick-count").textContent = `已选 ${picked.size} 项`;
  $("batch-apply").disabled = batchBusy || !picked.size;
  $("review-picks").disabled = batchBusy || !picked.size;
  $("pick-page").disabled = batchBusy || searchLoading;
  $("pick-list").replaceChildren();
  for (const item of picked.values()) {
    const card = text("div", "", "pick-item");
    card.append(text("strong", item.name), text("p", item.path || item.id, "path"),
      text("p", `标签：${item.tags?.join(", ") || "无"} · 状态：${stateNames[item.state || "unreviewed"]} · 收藏：${item.favorite ? "是" : "否"}`));
    const remove = text("button", "移出选择"); remove.disabled = batchBusy; remove.addEventListener("click", () => { picked.delete(item.id); updatePicks(); }); card.append(remove);
    $("pick-list").append(card);
  }
  document.querySelectorAll(".bulk-pick").forEach(check => { check.checked = picked.has(check.dataset.id); check.disabled = batchBusy || searchLoading; });
}
function setBatchBusy(busy) {
  batchBusy = busy;
  document.querySelectorAll("#batch-form input,#batch-form select,#pick-page,#clear-picks,#search-form input,#search-form button,.filters input,.filters select").forEach(el => { el.disabled = busy; });
  if (!busy) { $("catalog-sort").disabled = Boolean($("query").value.trim()); $("batch-tags").disabled = $("batch-tag-mode").value === "clear"; }
  updatePicks();
}
$("pick-page").addEventListener("click", () => {
  const next = new Map(picked);
  for (const item of currentResults) if (item.annotation_revision) next.set(item.id, picked.get(item.id) || item);
  if (next.size > 100) { notice("最多选择 100 项，请先减少已有选择。", true); return; }
  picked.clear(); for (const [id, item] of next) picked.set(id, item); updatePicks();
});
$("clear-picks").addEventListener("click", () => { picked.clear(); updatePicks(); });
$("batch-tag-mode").addEventListener("change", () => { $("batch-tags").disabled = $("batch-tag-mode").value === "clear"; });
$("review-picks").addEventListener("click", async () => {
  if (batchBusy || !picked.size) return;
  setBatchBusy(true);
  try {
    const data = await api("/api/annotations?" + new URLSearchParams({ids: [...picked.keys()].join(",")}));
    for (const item of data.entries) picked.set(item.id, {...picked.get(item.id), ...item});
    $("pick-details").open = true; notice("已读取选中位置的当前标签和状态。核对后可重新应用批量操作。");
  } catch (err) { notice(err.message, true); }
  finally { setBatchBusy(false); }
});
$("batch-form").addEventListener("submit", async e => {
  e.preventDefault(); if (batchBusy || !picked.size) return;
  const tags = $("batch-tags").value.split(/[,，]/).map(tag => tag.trim()).filter(Boolean), mode = $("batch-tag-mode").value;
  const payload = {ids: [...picked.keys()], tag_mode: mode, expected_revisions: Object.fromEntries([...picked].map(([id, item]) => [id, item.annotation_revision]))};
  if (mode === "clear") payload.tags = []; else if (tags.length) payload.tags = tags;
  if (mode === "replace" && !tags.length) { notice("替换标签需要输入内容；清空标签请选“清空标签”。", true); return; }
  if ($("batch-state").value) payload.state = $("batch-state").value;
  if ($("batch-favorite").value) payload.favorite = $("batch-favorite").value === "true";
  if (payload.tags === undefined && payload.state === undefined && payload.favorite === undefined) { notice("请先设置标签、状态或收藏操作。", true); return; }
  setBatchBusy(true); $("batch-apply").textContent = "正在应用…";
  try {
    const result = await api("/api/annotate-batch", payload);
    picked.clear();
    await search(false);
    if (selected && payload.ids.includes(selected.id)) { const notesOpen = !$("notes-panel").hidden; if (await select(selected.id)) { if (notesOpen) tab("notes"); } }
    notice(`批量整理完成：更新 ${result.updated} 项，未变化 ${result.unchanged} 项。个人笔记保留。`);
  } catch (err) { notice(err.message + " 选择和操作设置已保留，可先重新读取选中记录核对。", true); }
  finally { $("batch-apply").textContent = "应用到已选条目"; setBatchBusy(false); }
});
function tab(name) {
  desiredDetailTab = name;
  for (const key of ["content", "files", "notes"]) { $(key + "-panel").hidden = name !== key; $("tab-" + key).classList.toggle("active", name === key); }
}
for (const name of ["content", "files", "notes"]) $("tab-" + name).addEventListener("click", () => tab(name));
async function select(id, preferredDraftKey = null) {
  const serial = ++selectionSerial; ++resourceSerial;
  detailLoading = true; desiredDetailTab = "content"; updateNoteControls();
  try {
    const data = await api("/api/skill?" + new URLSearchParams({id}));
    if (serial !== selectionSerial) return;
    selected = data;
    $("detail-empty").hidden = true; $("detail").hidden = false;
    document.querySelectorAll(".result").forEach(el => el.classList.toggle("active", el.dataset.id === id));
    $("detail-name").textContent = data.name; $("detail-kind").textContent = data.kind.toUpperCase();
    $("detail-path").textContent = data.path; $("content").textContent = data.content;
    $("detail-warnings").textContent = (data.warnings || []).join(" · "); $("detail-warnings").hidden = !data.warnings?.length;
    $("stale-message").hidden = !data.stale;
    fillNotes(data.annotation);
    draftStore.reload(); draftStore.acknowledge(id, data.annotation);
    let draft = draftStore.get(preferredDraftKey) || draftStore.get(noteDrafts.get(id)?.key)
      || draftStore.all().find(record => record.id === id && record.base_revision === data.annotation_revision);
    if (draft && SklibDrafts.same(draft.values, data.annotation)) draft = null;
    if (draft) {
      noteDrafts.set(id, draft); $("note-tags").value = draft.values.tags; $("note-text").value = draft.values.note;
      $("note-state").value = draft.values.state; $("note-favorite").checked = draft.values.favorite;
      notice("已恢复浏览器草稿，请核对后保存到资料库。");
    } else noteDrafts.delete(id);
    updateDraftUi(); showNoteConflict();
    if (!draft && draftStore.all().some(record => record.id === id)) $("draft-status").textContent = "草稿箱有来自较早版本的副本，可打开恢复并与当前记录核对。";
    $("files").replaceChildren(); $("resource-content").textContent = ""; $("resource-label").textContent = ""; $("resource-more").hidden = true; $("resource-encoding").value = ""; resource = null;
    const categories = {source: "源代码 / 脚本", configuration: "配置", document: "文档", image: "图片", document_binary: "二进制文档", archive: "压缩包", executable: "程序 / 编译产物", media: "音视频", data_binary: "二进制数据", notebook: "Notebook", unknown: "其他"};
    const details = new Map((data.file_details || []).map(item => [item.path, item]));
    for (const path of data.files) {
      const info = details.get(path), button = text("button", path, "file-button");
      button.disabled = info?.text_readable === false;
      button.addEventListener("click", () => readResource(path)); $("files").append(button);
      if (info) $("files").append(text("p", `${categories[info.category] || info.category} · ${info.size_bytes} 字节${info.text_readable ? "" : " · 仅列出文件信息"}`, "path"));
    }
    if (data.file_list_truncated) $("files").append(text("p", "清单受数量、目录深度或访问权限限制，可能不完整。最多展示 256 项。", "path"));
    tab(desiredDetailTab);
    return true;
  } catch (err) { if (serial === selectionSerial) notice(err.message, true); return false; }
  finally { if (serial === selectionSerial) { detailLoading = false; updateNoteControls(); } }
}
async function readResource(path, more = false) {
  if (!selected) return;
  const serial = ++resourceSerial, id = selected.id;
  $("resource-more").hidden = true;
  try {
    const params = new URLSearchParams({id, path, start_line: more ? resource.next_start_line : 1});
    if (more) params.set("revision", resource.revision);
    if ($("resource-encoding").value) params.set("encoding", $("resource-encoding").value);
    const data = await api("/api/file?" + params);
    if (serial !== resourceSerial || selected.id !== id) return;
    $("resource-content").textContent = (more ? $("resource-content").textContent : "") + data.content;
    $("resource-label").textContent = `${path} · ${data.encoding} · 已读取至 ${data.end_line}/${data.total_lines} 行`;
    $("resource-more").hidden = data.next_start_line === null; resource = data;
  } catch (err) {
    if (serial === resourceSerial) {
      if (err.details?.code === "resource_changed") { resource = null; $("resource-content").textContent = ""; $("resource-label").textContent = "资源版本已变化，请选择文件从第 1 行重新读取。"; }
      else if (more && resource?.next_start_line) $("resource-more").hidden = false;
      notice(err.message, true);
    }
  }
}
$("resource-more").addEventListener("click", () => readResource(resource.relative_path, true));
$("resource-encoding").addEventListener("change", () => { if (resource) readResource(resource.relative_path); });
$("copy-path").addEventListener("click", async () => { if (selected) { try { await navigator.clipboard.writeText(selected.path); notice("路径已复制。"); } catch { notice(selected.path); } } });
$("notes-panel").addEventListener("submit", async e => {
  e.preventDefault(); if (!selected || noteSaving || detailLoading) return;
  const id = selected.id;
  const submitted = draftValues(), meta = {id, name: selected.name, path: selected.path};
  const base = noteDrafts.get(id)?.base_revision || selected.annotation_revision;
  const payload = {id, tags: submitted.tags.split(/[,，]/).map(t => t.trim()).filter(Boolean), note: submitted.note, favorite: submitted.favorite, state: submitted.state, expected_annotation_revision: base};
  noteSaving = true; updateNoteControls();
  try {
    const saved = await api("/api/annotate", payload);
    const pending = noteDrafts.get(id);
    draftStore.acknowledge(id, saved);
    const edited = selected?.id === id && !SklibDrafts.same(draftValues(), saved);
    if (edited) noteDrafts.set(id, draftStore.save(meta, draftValues(), saved.annotation_revision));
    else if (pending && !SklibDrafts.same(pending.values, saved)) noteDrafts.set(id, draftStore.save(meta, pending.values, saved.annotation_revision));
    else noteDrafts.delete(id);
    invalidatePreview();
    if (selected.id === id) {
      selected.annotation = {...saved, tags: JSON.stringify(saved.tags)};
      selected.annotation_revision = saved.annotation_revision;
      notice(edited ? "上次提交的记录已保存，当前修改尚未保存。" : "个人记录已保存。需要留存版本时，可前往“记录与版本”。");
    }
    updateDraftUi(); showNoteConflict();
    search(false);
  } catch (err) {
    notice(err.message, true);
    if (err.details?.code === "annotation_conflict" && selected?.id === id) {
      try { const latest = await api("/api/skill?" + new URLSearchParams({id})); if (selected?.id === id) { selected.annotation = latest.annotation; selected.annotation_revision = latest.annotation_revision; showNoteConflict(); } }
      catch (readError) { notice(err.message + " · " + readError.message, true); }
    }
  }
  finally { noteSaving = false; updateNoteControls(); }
});
$("index-form").addEventListener("submit", async e => {
  e.preventDefault(); const button = $("index-form").querySelector("button"); button.disabled = true; button.textContent = "正在加入队列…";
  try { const job = await api("/api/index-jobs", {root: $("source-root").value.trim(), include_docs: $("include-docs").checked, encoding: $("source-encoding").value, verify: $("verify-files").checked, request_id: crypto.randomUUID()}); trackedJobs.add(job.id); notice("扫描已加入后台队列，可继续检索资料或刷新页面查看进度。"); await refreshJobs(); }
  catch (err) { notice(err.message + " 可查看下方扫描任务，确认请求是否已经入队。", true); await refreshJobs(); }
  finally { button.disabled = false; button.textContent = "扫描并更新索引"; }
});
async function refreshJobs() {
  if (jobsLoading) { jobsRefreshRequested = true; return; }
  jobsLoading = true; clearTimeout(jobTimer);
  let active = false;
  try {
    const data = await api("/api/index-jobs");
    $("job-connection").hidden = true; $("index-jobs").replaceChildren();
    const finished = [];
    const labels = {queued: "排队中", running: "扫描中", cancelling: "正在取消，等待安全检查点", succeeded: "扫描完成", partial: "扫描部分完成", failed: "扫描失败", cancelled: "扫描已取消", interrupted: "服务中断，请检查扫描结果"};
    for (const job of data.jobs) {
      const running = ["queued", "running", "cancelling"].includes(job.state);
      active ||= running;
      const previous = observedJobs.get(job.id);
      if (!running && (trackedJobs.has(job.id) || previous && ["queued", "running", "cancelling"].includes(previous))) finished.push(job);
      if (running) trackedJobs.add(job.id); else trackedJobs.delete(job.id);
      observedJobs.set(job.id, job.state);
      const card = text("article", "", "source-card index-job"); card.dataset.jobId = job.id; card.dataset.state = job.state;
      card.append(text("h3", `${labels[job.state] || job.state} · ${job.root}`));
      const progress = job.progress || {};
      if (running) {
        const bar = document.createElement("progress"); bar.setAttribute("aria-label", "索引进度");
        if (progress.phase === "index" && progress.candidates > 0) { bar.max = progress.candidates; bar.value = progress.processed || 0; }
        card.append(bar, text("p", progress.phase === "index" ? `建立索引 ${progress.processed || 0} / ${progress.candidates || 0} 项；已检查 ${progress.files_examined || 0} 个文件。` : progress.phase === "queued" ? "等待前面的扫描完成。" : `正在发现资料，已检查 ${progress.files_examined || 0} 个文件。`));
        const cancel = text("button", job.state === "cancelling" ? "等待停止…" : "取消扫描"); cancel.disabled = job.state === "cancelling";
        cancel.addEventListener("click", async () => { cancel.disabled = true; try { await api("/api/index-jobs/cancel", {id: job.id}); } catch (err) { notice(err.message, true); } finally { await refreshJobs(); } });
        card.append(cancel);
      }
      if (job.report) card.append(text("p", `新增 ${job.report.added} · 更新 ${job.report.updated} · 未变化 ${job.report.unchanged} · 读取失败 ${job.report.failure_count || 0}${job.cancel_requested ? " · 取消请求晚于本轮提交，以此结果为准" : ""}`));
      if (job.error) card.append(text("p", `${job.error.error} · ${job.error.recovery}`));
      if (job.status_warning) card.append(text("p", job.status_warning.recovery));
      card.append(text("p", `${job.updated_at} · ${job.id}`, "path"));
      $("index-jobs").append(card);
    }
    if (!data.jobs.length) $("index-jobs").append(text("p", "还没有后台扫描任务。", "path"));
    if (finished.length) {
      invalidatePreview(); await refreshStatus(); await search();
      const job = finished[0];
      notice(job.report ? `扫描${job.report.complete ? "完成" : "部分完成"}：新增 ${job.report.added}，更新 ${job.report.updated}，未变化 ${job.report.unchanged}。` : `${labels[job.state]}。${job.error?.recovery || "请检查来源状态。"}`, !job.report && job.state !== "cancelled");
    }
  } catch (err) { $("job-connection").textContent = "任务状态暂时无法读取，保留上次显示。" + err.message; $("job-connection").hidden = false; active = true; }
  finally { jobsLoading = false; const delay = jobsRefreshRequested ? 0 : active || trackedJobs.size ? 1000 : 10000; jobsRefreshRequested = false; jobTimer = setTimeout(refreshJobs, delay); }
}
function trackIndexJob(id) { trackedJobs.add(id); return refreshJobs(); }
async function recordAction(action) {
  if (recordsBusy) return;
  recordsWorking(true);
  const serial = ++recordsSerial;
  previewToken = null; $("commit-button").disabled = true;
  notice(action === "preview" ? "正在生成记录快照和 Git 预览…" : "正在读取记录仓库…");
  try { const data = await api("/api/records/" + action, ["log", "status"].includes(action) ? undefined : {}); if (serial !== recordsSerial) return; $("records-output").textContent = action === "preview" ? `${data.repository}\n\n${data.diff || "记录内容没有变化。"}` : JSON.stringify(data, null, 2); previewToken = action === "preview" ? data.preview_token : null; $("commit-button").disabled = action !== "preview" || !data.pending_changes; notice(action === "preview" ? (data.pending_changes ? "预览已生成，请核对后提交。" : "记录内容没有变化。") : "记录仓库操作已完成。"); }
  catch (err) { if (serial === recordsSerial) notice(err.message, true); }
  finally { recordsWorking(false); }
}
for (const action of ["init", "preview", "log", "status"]) $("records-" + action).addEventListener("click", () => recordAction(action));
$("commit-form").addEventListener("submit", async e => {
  e.preventDefault(); if (recordsBusy) return; recordsWorking(true); const button = $("commit-button"); button.disabled = true;
  const serial = ++recordsSerial, submittedToken = previewToken; previewToken = null;
  notice("正在提交记录到本地 Git…");
  try { const data = await api("/api/records/commit", {message: $("commit-message").value.trim(), preview_token: submittedToken}); if (serial !== recordsSerial) return; $("records-output").textContent = JSON.stringify(data, null, 2); notice(data.committed ? (data.warnings?.length ? "记录已提交到本地 Git，但活动日志写入失败。保留提交号，无需重复提交。" : "记录已提交到本地 Git。") : "记录内容没有变化。"); loadHistory(); }
  catch (err) { if (serial === recordsSerial) notice(err.message, true); }
  finally { recordsWorking(false); }
});
async function loadHistory() {
  try { const data = await api("/api/history"); $("activity-list").replaceChildren(); for (const item of data) { const card = text("article", "", "activity"); card.append(text("strong", item.action), text("p", item.created_at)); $("activity-list").append(card); } }
  catch (err) { notice(err.message, true); }
}
document.addEventListener("keydown", e => { if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "k") { e.preventDefault(); showView("library"); $("query").focus(); } });
const initialStatus = refreshStatus();
initialStatus.then(() => search()).catch(err => notice(err.message, true));
refreshJobs();
