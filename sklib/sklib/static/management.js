/* Source monitoring and previewed annotation restore share the existing API. */
(() => {
  "use strict";
  const sourcePanel = $("source-monitor-tools"), restorePanel = $("restore-tools");
  $("index-form").after(sourcePanel); sourcePanel.hidden = false;
  $("view-records").append(restorePanel); restorePanel.hidden = false;
  let roots = [], monitorTimer, monitorLoading = false, monitorSerial = 0, monitorBusy = false, lastReports = "";
  const stateLabels = {clean: "未检测到变化", changed: "需要刷新", attention: "检查未完成"};
  const automaticJobs = new Set();
  function renderMonitor(data) {
    $("source-auto-check").checked = data.enabled;
    $("source-auto-refresh").checked = data.auto_refresh;
    $("source-auto-refresh").disabled = !data.enabled || monitorBusy;
    if (document.activeElement !== $("source-check-interval")) $("source-check-interval").value = data.interval_seconds;
    $("source-check-status").textContent = data.error ? `检测失败：${data.error.error} · ${data.error.recovery}` : data.running ? "正在检测来源…" : data.enabled ? "定时检测已启用。" : "定时检测未启用，可手动检测。";
    const reports = JSON.stringify(data.reports); if (reports === lastReports) return; lastReports = reports;
    $("source-check-results").replaceChildren();
    for (const report of data.reports) {
      const card = text("article", "", "source-card");
      card.append(text("h3", report.root), text("strong", stateLabels[report.state] || report.state),
        text("p", `新增 ${report.added} · 修改 ${report.modified} · 删除 ${report.removed} · 检查文件 ${report.files_examined}`), text("p", report.checked_at, "path"));
      if (!report.complete) card.append(text("p", "检查不完整，未将未见条目认定为删除。", "warning"));
      if (report.requires_reindex) card.append(text("p", "上次扫描不完整或解析器已更新，需要重新扫描。"));
      for (const failure of report.failures.slice(0, 3)) card.append(text("p", `${failure.path} · ${failure.error} · ${failure.recovery}`, "warning"));
      if (report.refresh_job) {
        card.append(text("p", "已安排自动刷新，最新结果见扫描任务列表。"));
        if (!automaticJobs.has(report.refresh_job)) {
          automaticJobs.add(report.refresh_job); refreshJobs();
          refreshStatus().then(() => search()).catch(error => notice(error.message, true));
        }
      }
      if (report.refresh_suppressed) card.append(text("p", "相同的来源变化已尝试刷新，本次不重复入队。请检查扫描结果；修正文件后会再次检测，也可手动刷新。", "warning"));
      if (report.refresh_error) card.append(text("p", report.refresh_error.recovery, "warning"));
      if (report.state === "changed") {
        const refresh = text("button", "刷新这个来源");
        refresh.addEventListener("click", async () => {
          refresh.disabled = true;
          try { const job = await api("/api/index-jobs", {root: report.root, request_id: crypto.randomUUID()}); trackIndexJob(job.id); notice("已加入扫描队列。"); }
          catch (error) { notice(error.message, true); refresh.disabled = false; }
        });
        card.append(refresh);
      }
      $("source-check-results").append(card);
    }
  }
  async function refreshMonitor() {
    if (monitorLoading) return;
    monitorLoading = true; const serial = monitorSerial; let delay = 10000;
    try { const data = await api("/api/source-monitor"); if (serial === monitorSerial) renderMonitor(data); if (data.enabled || data.running || !$("view-sources").hidden) delay = 2000; }
    catch (error) { $("source-check-status").textContent = "检测状态暂时无法读取。" + error.message; }
    finally { monitorLoading = false; clearTimeout(monitorTimer); monitorTimer = setTimeout(refreshMonitor, delay); }
  }
  async function configureMonitor(checkNow = false) {
    if (monitorBusy) return;
    const parameters = {enabled: $("source-auto-check").checked, auto_refresh: $("source-auto-refresh").checked,
      interval_seconds: Number($("source-check-interval").value), check_now: checkNow};
    monitorBusy = true; ++monitorSerial;
    for (const element of sourcePanel.querySelectorAll("input,button")) element.disabled = true;
    try { renderMonitor(await api("/api/source-monitor", parameters)); if (checkNow) $("source-check-status").textContent = "检测已安排，正在读取来源…"; }
    catch (error) { notice(error.message, true); }
    finally { monitorBusy = false; for (const element of sourcePanel.querySelectorAll("input,button")) element.disabled = false;
      $("source-auto-refresh").disabled = !$("source-auto-check").checked; clearTimeout(monitorTimer); monitorTimer = setTimeout(refreshMonitor, 300); }
  }
  $("source-check").addEventListener("click", () => configureMonitor(true));
  for (const button of document.querySelectorAll(".nav")) button.addEventListener("click", () => { if (button.dataset.view === "sources") refreshMonitor(); });
  for (const id of ["source-auto-check", "source-auto-refresh", "source-check-interval"]) $(id).addEventListener("change", () => configureMonitor());

  let snapshot = null, mode = "import", rootMaps = {}, entryMap = {}, resolutions = {};
  let restoreToken = null, restoreNext = null, restoreBusy = false, restoreSerial = 0, updateCount = 0, fileSerial = 0;
  function invalidateRestore(message) {
    ++restoreSerial; restoreToken = null; $("restore-apply").disabled = true; $("restore-more").hidden = true;
    if (message) $("restore-summary").textContent = message;
  }
  function updateRoots(data) {
    const changed = JSON.stringify(roots.map(root => root.path)) !== JSON.stringify(data.roots.map(root => root.path));
    roots = data.roots;
    for (const id of ["migration-from", "migration-to"]) {
      const previous = $(id).value;
      $(id).replaceChildren(...roots.map(root => new Option(root.path, root.path)));
      if (roots.some(root => root.path === previous)) $(id).value = previous;
    }
    if ($("migration-from").value === $("migration-to").value && roots.length > 1) $("migration-to").value = roots[1].path;
    if (changed) renderRootMappings();
    if (changed) invalidateRestore("来源列表已更新，请重新预览恢复操作。");
  }
  document.addEventListener("sklib-status", event => updateRoots(event.detail));
  function renderRootMappings() {
    $("restore-root-mappings").replaceChildren();
    const originals = [...new Set((snapshot?.entries || []).map(entry => entry.root).filter(value => typeof value === "string"))];
    for (const original of originals) {
      const label = text("label", "来源映射：" + original), select = document.createElement("select");
      select.append(new Option("按原路径匹配", ""), ...roots.map(root => new Option(root.path, root.path)));
      select.value = rootMaps[original] || "";
      select.addEventListener("change", () => { if (select.value) rootMaps[original] = select.value; else delete rootMaps[original]; invalidateRestore("来源映射已修改，请重新预览。"); });
      label.append(select); $("restore-root-mappings").append(label);
    }
  }
  function working(busy) {
    restoreBusy = busy;
    for (const element of restorePanel.querySelectorAll("input,select,textarea,button")) element.disabled = busy;
    $("restore-apply").disabled = busy || !restoreToken || !updateCount;
  }
  function parameters() {
    const common = {policy: $("restore-policy").value, match_content: $("restore-match-content").checked, entry_map: entryMap, resolutions};
    return mode === "import" ? {...common, snapshot, root_map: rootMaps} : {...common, from_root: $("migration-from").value, to_root: $("migration-to").value};
  }
  function switchMode(next) { if (mode !== next) { mode = next; entryMap = {}; resolutions = {}; invalidateRestore(); } }
  $("restore-file").addEventListener("change", async () => {
    const serial = ++fileSerial;
    invalidateRestore(); snapshot = null; rootMaps = {}; entryMap = {}; resolutions = {}; $("restore-entries").replaceChildren();
    const file = $("restore-file").files[0]; if (!file) return;
    try {
      if (file.size > 16 * 1024 * 1024) throw new Error("快照超过 16 MiB。");
      const bytes = new Uint8Array(await file.arrayBuffer());
      const encoding = bytes[0] === 255 && bytes[1] === 254 ? "utf-16le" : bytes[0] === 254 && bytes[1] === 255 ? "utf-16be" : "utf-8";
      const parsed = JSON.parse(new TextDecoder(encoding, {fatal: true}).decode(bytes));
      if (serial !== fileSerial) return;
      if (!parsed || !Array.isArray(parsed.entries)) throw new Error("请选择 SKLIB 整理快照。");
      snapshot = parsed; switchMode("import"); renderRootMappings(); $("restore-summary").textContent = "快照已读取，选择来源映射与冲突处理后预览。";
    } catch (error) { if (serial === fileSerial) notice(error.message, true); }
  });
  for (const id of ["restore-policy", "restore-match-content", "migration-from", "migration-to"]) $(id).addEventListener("change", () => invalidateRestore("选项已修改，请重新预览。"));
  const actionLabels = {insert: "将新增记录", replace: "将覆盖已有记录", conflict: "保留已有记录（存在冲突）", unchanged: "内容相同，无需修改"};
  function valuePanel(label, value) {
    const panel = document.createElement("div"); panel.append(text("strong", label));
    if (value) {
      panel.append(text("p", `标签：${value.tags.join("、") || "无"} · 状态：${stateNames[value.state] || value.state} · 收藏：${value.favorite ? "是" : "否"}`));
      const note = document.createElement("textarea"); note.readOnly = true; note.rows = 3; note.value = value.note; note.setAttribute("aria-label", label + "笔记"); panel.append(note);
    } else panel.append(text("p", "尚无整理记录"));
    return panel;
  }
  function renderEntry(entry) {
    const card = text("article", "", "source-card restore-entry");
    card.append(text("h3", entry.name), text("strong", actionLabels[entry.action]),
      text("p", `${entry.source_root || "待关联记录"} / ${entry.source_relative_path || entry.source_id} → ${entry.target_path || "待关联记录"}`, "path"));
    if (entry.orphan) card.append(text("p", entry.reason === "ambiguous_content" ? "存在多个相同内容的目标，尚未自动选择。可指定目标，或先保留待关联记录。" : "尚未找到目标，导入后会保留为待关联记录。", "warning"));
    const values = text("div", "", "restore-values"); values.append(valuePanel("当前", entry.before), valuePanel("导入", entry.incoming)); card.append(values);
    if (entry.before && entry.action !== "unchanged") {
      const label = text("label", "此条记录的处理方式"), select = document.createElement("select");
      select.append(new Option("保留已有记录", "keep"), new Option("使用导入记录覆盖", "replace")); select.value = entry.policy;
      select.addEventListener("change", () => { resolutions[entry.source_id] = select.value; invalidateRestore("单条冲突处理已修改，请重新预览。"); }); label.append(select); card.append(label);
    }
    const details = document.createElement("details"); details.append(text("summary", "为此记录指定目标条目"));
    const input = document.createElement("input"); input.placeholder = "输入目标名称或关键词"; input.maxLength = 2048; input.setAttribute("aria-label", "查找目标条目");
    const find = text("button", "查找目标"), choices = document.createElement("select"), choose = text("button", "指定此目标");
    choices.setAttribute("aria-label", "目标条目"); choices.append(new Option("请先查找目标", ""));
    find.addEventListener("click", async () => { try {
      if (!input.value.trim()) throw new Error("先输入目标名称或关键词。");
      const data = await api("/api/search?" + new URLSearchParams({q: input.value, kind: "all", limit: 10}));
      choices.replaceChildren(new Option("选择目标", ""), ...data.results.map(item => new Option(`${item.name} · ${item.path || item.id}`, item.id)));
    } catch (error) { notice(error.message, true); } });
    choose.addEventListener("click", () => { if (!choices.value) return; entryMap[entry.source_id] = choices.value; invalidateRestore("目标已指定，请重新预览。"); });
    details.append(input, find, choices, choose); card.append(details); return card;
  }
  async function preview(offset = 0) {
    if (restoreBusy) return;
    if (mode === "import" && !snapshot) { notice("先选择整理快照。", true); return; }
    if (mode === "migrate" && $("migration-from").value === $("migration-to").value) { notice("请选择不同的原来源和新来源。", true); return; }
    const prior = restoreToken, serial = ++restoreSerial; working(true); restoreToken = null;
    if (!offset) $("restore-entries").replaceChildren();
    try {
      const data = await api(`/api/records/${mode}-preview`, {...parameters(), offset, limit: 20});
      if (serial !== restoreSerial) return;
      if (offset && data.preview_token !== prior) throw new Error("预览期间记录已变化，请重新从头预览。");
      restoreToken = data.preview_token; restoreNext = data.next_offset; updateCount = data.counts.insert + data.counts.replace;
      $("restore-summary").textContent = `共 ${data.counts.total} 项：新增 ${data.counts.insert}，覆盖 ${data.counts.replace}，保留冲突 ${data.counts.conflict}，相同 ${data.counts.unchanged}，待关联 ${data.counts.orphans}。`;
      for (const entry of data.entries) $("restore-entries").append(renderEntry(entry));
      $("restore-more").hidden = restoreNext === null;
      $("restore-apply").textContent = `应用 ${updateCount} 项修改`;
    } catch (error) { notice(error.message, true); }
    finally { working(false); }
  }
  $("restore-form").addEventListener("submit", event => { event.preventDefault(); switchMode("import"); preview(); });
  $("migration-form").addEventListener("submit", event => { event.preventDefault(); switchMode("migrate"); preview(); });
  $("restore-more").addEventListener("click", () => preview(restoreNext));
  $("restore-apply").addEventListener("click", async () => {
    if (restoreBusy || !restoreToken) return;
    const submitted = restoreToken; restoreToken = null; working(true);
    try {
      const result = await api(`/api/records/${mode}-apply`, {...parameters(), preview_token: submitted});
      $("restore-summary").textContent = `已保存 ${result.updated} 项修改，保留冲突 ${result.counts.conflict} 项。原位置的整理记录仍保留。`;
      notice("整理记录已导入。再次操作前请重新预览。"); await refreshStatus(); await search(); loadHistory();
    } catch (error) { notice(error.message, true); }
    finally { $("restore-more").hidden = true; working(false); }
  });
  $("snapshot-download").addEventListener("click", async () => {
    const button = $("snapshot-download"); button.disabled = true;
    try {
      const data = await api("/api/records/snapshot"), blob = new Blob([JSON.stringify(data, null, 2)], {type: "application/json"});
      if (blob.size > 16 * 1024 * 1024) throw new Error("快照超过 16 MiB，请通过命令行按来源或 offset/limit 分批导出，现有资料仍保留。");
      const url = URL.createObjectURL(blob);
      const link = document.createElement("a"); link.href = url; link.download = "sklib-records.json"; link.click(); setTimeout(() => URL.revokeObjectURL(url), 1000);
    } catch (error) { notice(error.message, true); }
    finally { button.disabled = false; }
  });
  initialStatus.then(updateRoots).catch(error => notice(error.message, true));
  refreshMonitor();
})();
