// SARIF Manager - Shared UI interactions

document.addEventListener('DOMContentLoaded', () => {
  try {
    setActiveSidebarItem();
    initFindingsSearch();
    initUploadInteractions();
    // Initialize page features based on element presence (robust to pretty URLs)
    if (document.getElementById('dashboard-content')) loadDashboard();
    if (document.getElementById('projects-grid')) { loadProjects(); initCreateProjectModal(); }
    if (document.getElementById('findings-tbody')) loadFindings();
  } catch (e) {
    // noop
  }
});

function setActiveSidebarItem() {
  const path = (location.pathname.split('/').pop() || '').toLowerCase();
  const items = document.querySelectorAll('.sidebar .nav-item');
  items.forEach((a) => a.classList.remove('active'));
  if (!items.length) return;
  let matched = false;
  items.forEach((a) => {
    const href = (a.getAttribute('href') || '').toLowerCase();
    if (href && path && href === path) {
      a.classList.add('active');
      matched = true;
    }
  });
  // Fallback to dashboard
  if (!matched) {
    const dashboard = Array.from(items).find((a) => (a.getAttribute('href') || '').toLowerCase() === 'dashboard.html');
    if (dashboard) dashboard.classList.add('active');
  }
}

function initFindingsSearch() {
  const searchBox = document.querySelector('.page-content .search-box input');
  const table = document.querySelector('.page-content table.table');
  if (!searchBox || !table) return;
  const tbody = table.querySelector('tbody');
  if (!tbody) return;
  const rows = Array.from(tbody.querySelectorAll('tr'));
  searchBox.addEventListener('input', () => {
    const q = searchBox.value.trim().toLowerCase();
    rows.forEach((tr) => {
      const text = tr.innerText.toLowerCase();
      tr.style.display = text.includes(q) ? '' : 'none';
    });
  });
}

// In Netlify static deploy, we run serverless: store data in localStorage
const LS_KEY = 'sarifDb';
function loadLocalDb() {
  try { return JSON.parse(localStorage.getItem(LS_KEY) || '{"projects":[]}'); } catch { return { projects: [] }; }
}
function saveLocalDb(db) { localStorage.setItem(LS_KEY, JSON.stringify(db)); }
function upsertLocalProject(db, name, description='') {
  let p = db.projects.find(x => x.name === name);
  if (!p) { p = { id: crypto.randomUUID ? crypto.randomUUID() : String(Date.now()), name, description, findings: [], tools: [], updated_at: new Date().toISOString() }; db.projects.push(p); }
  return p;
}
function mapSeverity(level) {
  const l = String(level || '').toLowerCase();
  if (l === 'error') return 'high';
  if (l === 'warning') return 'medium';
  if (l === 'note') return 'low';
  return 'info';
}
function processSarifToProject(db, sarifObj, projectName) {
  const runs = sarifObj && Array.isArray(sarifObj.runs) ? sarifObj.runs : null; if (!runs || !runs[0]) return { total_findings: 0, tools: [] };
  const run = runs[0];
  const tool = ((run.tool||{}).driver||{}).name || 'Unknown';
  const results = Array.isArray(run.results) ? run.results : [];
  const rulesArr = (((run.tool||{}).driver||{}).rules) || [];
  const rulesMap = {}; rulesArr.forEach(r => { rulesMap[r.id] = r; });
  const prj = upsertLocalProject(db, projectName || 'Default Project');
  let total = 0; const tools = new Set(prj.tools || []);
  for (const res of results) {
    total += 1;
    const ruleId = res.ruleId || '';
    const rule = rulesMap[ruleId] || {};
    const level = (rule.defaultConfiguration && rule.defaultConfiguration.level) || 'note';
    const message = (res.message && res.message.text) || (rule.name || ruleId);
    const loc = Array.isArray(res.locations) && res.locations[0] ? res.locations[0] : {};
    const phys = (loc.physicalLocation || {});
    const file = ((phys.artifactLocation || {}).uri) || '';
    prj.findings.push({
      severity: mapSeverity(level),
      ruleId: ruleId,
      message: message,
      file: file,
      tool: tool,
      status: 'new',
      projectName: prj.name,
      created_at: new Date().toISOString(),
    });
  }
  if (tool) tools.add(tool);
  prj.tools = Array.from(tools);
  prj.updated_at = new Date().toISOString();
  return { total_findings: total, tools: prj.tools };
}

// --- UPLOAD LOGIC ---
function initUploadInteractions() {
  const fileInput = document.getElementById('file-input');
  const uploadedFiles = document.getElementById('uploaded-files');
  const uploadSummary = document.getElementById('upload-summary');
  const uploadArea = document.getElementById('upload-area') || document.querySelector('.upload-area');
  const startBtn = document.getElementById('btn-start-upload');
  const cancelBtn = document.getElementById('btn-cancel-upload');
  const dashboardBtn = document.getElementById('btn-upload-from-dashboard');

  if (dashboardBtn) {
    dashboardBtn.addEventListener('click', () => { window.location.href = 'upload.html'; });
  }

  if (cancelBtn) {
    cancelBtn.addEventListener('click', () => { window.location.href = 'projects.html'; });
  }

  if (!fileInput || !uploadArea) return;

  async function handleFiles(files) {
    if (!files || !files.length) return;
    if (uploadedFiles) uploadedFiles.style.display = 'block';
    // Показываем loader
    uploadedFiles.innerHTML = '<div class="spinner" style="margin:32px auto;"></div>';
    const projectSelect = document.getElementById('project-select');
    const projectName = projectSelect && projectSelect.value && projectSelect.value !== 'Select a project...' ? projectSelect.value : 'Default Project';
    // Client-side parse SARIF
    let total_findings = 0; let total_size = 0; const tools = new Set();
    const db = loadLocalDb();
    for (const f of Array.from(files)) {
      const text = await f.text(); total_size += f.size || 0;
      try {
        const obj = JSON.parse(text);
        const res = processSarifToProject(db, obj, projectName);
        total_findings += res.total_findings; res.tools.forEach(t => tools.add(t));
      } catch (e) {
        uploadedFiles.innerHTML = '<div class="empty-state-text" style="color:red">Ошибка парсинга '+(f.name||'')+': '+String(e)+'</div>';
        return;
      }
    }
    saveLocalDb(db);
    const summaryData = { total_files: files.length, total_findings, size_mb: (total_size/(1024*1024)).toFixed(2), tools: Array.from(tools), projects: db.projects.map(p=>({id:p.id,name:p.name})) };
    // Показываем имена файлов и summary
    renderUploadedFiles(Array.from(files), summaryData);
    renderUploadSummary(summaryData);
  }

  function renderUploadedFiles(files, summary) {
    uploadedFiles.innerHTML = '';
    const title = document.createElement('h4');
    title.textContent = 'Uploaded Files';
    title.style.fontSize = '14px'; title.style.fontWeight = '600';
    title.style.marginBottom = 'var(--spacing-md)';
    uploadedFiles.appendChild(title);
    files.forEach(file => {
      const container = document.createElement('div');
      container.style.padding = 'var(--spacing-md)';
      container.style.border = '1px solid var(--border-color)';
      container.style.borderRadius = 'var(--border-radius)';
      container.style.marginBottom = 'var(--spacing-sm)';
      container.style.display = 'flex';
      container.style.alignItems = 'center';
      container.style.gap = 'var(--spacing-md)';
      const icon = document.createElement('div');
      icon.textContent = '📄';
      icon.style.width = '40px'; icon.style.height = '40px';
      icon.style.background = '#eff6ff';
      icon.style.borderRadius = 'var(--border-radius)';
      icon.style.display = 'flex';
      icon.style.alignItems = 'center';
      icon.style.justifyContent = 'center';
      icon.style.fontSize = '20px';
      const info = document.createElement('div'); info.style.flex = '1';
      const nameEl = document.createElement('div'); nameEl.style.fontWeight = '500'; nameEl.style.marginBottom = '2px'; nameEl.textContent = file.name;
      const metaEl = document.createElement('div'); metaEl.className = 'text-xs text-muted'; metaEl.textContent = formatFileSize(file.size) + ' • Uploaded & parsed';
      info.appendChild(nameEl); info.appendChild(metaEl);
      const right = document.createElement('div'); right.style.display = 'flex'; right.style.alignItems = 'center'; right.style.gap = '8px';
      const badge = document.createElement('span'); badge.className = 'badge badge-fixed'; badge.style.fontSize = '11px'; badge.textContent = 'Processed';
      right.appendChild(badge);
      container.appendChild(icon); container.appendChild(info); container.appendChild(right);
      uploadedFiles.appendChild(container);
    });
  }

  function renderUploadSummary(summary) {
    if (!uploadSummary) return;
    uploadSummary.style.display = 'block';
    const div = uploadSummary.querySelector('#upload-summary-stats');
    if (!div) return;
    div.innerHTML = '';
    if (!summary) return;
    // Пример: summary: { total_files, total_findings, size_mb, tools:[], projects:[] }
    const grid = document.createElement('div');
    grid.style.display = 'grid';
    grid.style.gridTemplateColumns = 'repeat(4,1fr)';
    grid.style.gap = 'var(--spacing-lg)';
    grid.style.marginBottom = 'var(--spacing-lg)';
    const cells = [
      [`Файлов`, summary.total_files || '—'],
      [`Всего Findings`, summary.total_findings || '—'],
      [`Размер`, summary.size_mb ? summary.size_mb+' MB':'—'],
      [`Инструментов`, (summary.tools || []).length]
    ];
    for (const [lab,val] of cells) {
      const c = document.createElement('div'); c.innerHTML = `<div class='text-sm text-muted' style='margin-bottom:4px;'>${lab}</div> <div class='text-bold' style='font-size:24px;'>${val}</div>`;
      grid.appendChild(c);
    }
    div.appendChild(grid);
    // Детали можно дополнить при необходимости
  }

  fileInput.addEventListener('change', (e) => handleFiles(e.target.files));
  uploadArea.addEventListener('dragover', (e) => { e.preventDefault(); uploadArea.classList.add('drag-over'); });
  uploadArea.addEventListener('dragleave', () => { uploadArea.classList.remove('drag-over'); });
  uploadArea.addEventListener('drop', (e) => {
    e.preventDefault(); uploadArea.classList.remove('drag-over'); handleFiles(e.dataTransfer.files);
  });

  if (startBtn) {
    startBtn.addEventListener('click', () => {
      if (fileInput && fileInput.files && fileInput.files.length) {
        handleFiles(fileInput.files);
      }
    });
  }
}

function formatFileSize(bytes) {
  if (!bytes && bytes !== 0) return '';
  const units = ['B', 'KB', 'MB', 'GB'];
  let size = bytes;
  let i = 0;
  while (size >= 1024 && i < units.length - 1) {
    size /= 1024;
    i++;
  }
  return `${size.toFixed(size < 10 && i > 0 ? 1 : 0)} ${units[i]}`;
}

// --- DASHBOARD, PROJECTS, FINDINGS ---

function initCreateProjectModal() {
  const submitBtn = document.getElementById('create-project-submit');
  const openBtn = document.getElementById('btn-open-create-project-modal');
  const closeBtn = document.getElementById('btn-close-create-project-modal');
  const cancelBtn = document.getElementById('btn-cancel-create-project-modal');
  const overlay = document.getElementById('createProjectModal');

  if (openBtn && overlay) openBtn.addEventListener('click', () => { overlay.style.display = 'flex'; });
  if (closeBtn && overlay) closeBtn.addEventListener('click', () => { overlay.style.display = 'none'; });
  if (cancelBtn && overlay) cancelBtn.addEventListener('click', () => { overlay.style.display = 'none'; });
  if (overlay) overlay.addEventListener('click', (e) => { if (e.target === overlay) overlay.style.display = 'none'; });

  if (!submitBtn) return;
  submitBtn.addEventListener('click', async () => {
    const nameEl = document.getElementById('create-project-name');
    const descEl = document.getElementById('create-project-desc');
    const name = nameEl ? nameEl.value : '';
    const desc = descEl ? descEl.value : '';
    if (!name.trim()) { alert('Project name is required'); return; }
    submitBtn.disabled = true;
    try {
      // Local create
      const db = loadLocalDb();
      const p = upsertLocalProject(db, name.trim(), desc.trim());
      saveLocalDb(db);
      const modal = document.getElementById('createProjectModal');
      if (modal) modal.style.display = 'none';
      await loadProjects();
    } catch (e) {
      alert('Failed to create project: ' + String(e));
    } finally {
      submitBtn.disabled = false;
    }
  });
}

async function loadDashboard() {
  const cont = document.getElementById('dashboard-content');
  if (!cont) return;
  cont.innerHTML = '<div class="spinner" style="margin:64px auto"></div>';
  const db = loadLocalDb();
  let total_findings = 0; db.projects.forEach(p => total_findings += (p.findings||[]).length);
  const stats = { summary: { total_findings, total_projects: db.projects.length, total_files: 0, size_mb: null } };
  if (!stats || !stats.summary || (db.projects.length===0)) {
    cont.innerHTML = `<div class="empty-state">
      <div class="empty-state-icon">📊</div>
      <div class="empty-state-title">Нет данных</div>
      <div class="empty-state-text">Загрузите отчеты, чтобы увидеть метрики и графики.</div>
    </div>`;
    return;
  }
  // Простейший рендер — stats.summary (можно расширить)
  cont.innerHTML = `<div class="card">
    <div class="card-header">
      <h3 class="card-title">Общая статистика</h3>
    </div>
    <div class="card-body">
      <div style='display:grid;grid-template-columns:repeat(4,1fr);gap:var(--spacing-lg);'>
        <div><div class='text-muted'>Всего находок</div><div class='text-bold' style='font-size:24px'>${stats.summary.total_findings ?? 0}</div></div>
        <div><div class='text-muted'>Проектов</div><div class='text-bold' style='font-size:24px'>${stats.summary.total_projects ?? 0}</div></div>
        <div><div class='text-muted'>Загружено файлов</div><div class='text-bold' style='font-size:24px'>${stats.summary.total_files ?? 0}</div></div>
        <div><div class='text-muted'>Размер</div><div class='text-bold' style='font-size:24px'>${stats.summary.size_mb ?? "-"} MB</div></div>
      </div>
    </div>
  </div>`;
}

async function loadProjects() {
  const grid = document.getElementById('projects-grid');
  if (!grid) return;
  grid.innerHTML = '<div class="spinner" style="margin:64px auto"></div>';
  const db = loadLocalDb();
  const projects = db.projects || [];
  if (!Array.isArray(projects) || projects.length === 0) {
    grid.innerHTML = `<div class="empty-state" style="grid-column:1/-1"><div class="empty-state-icon">📁</div><div class="empty-state-title">Нет проектов</div></div>`;
    return;
  }
  grid.innerHTML = '';
  for (const prj of projects) {
    // карточка проекта
    const card = document.createElement('div');
    card.className = 'card';
    card.style.cursor = 'pointer';
    card.onclick = () => window.location.href = 'findings.html?project_id=' + encodeURIComponent(prj.id);
    card.innerHTML = `<div class="card-body">
      <div style="margin-bottom:var(--spacing-lg)"><h3 style="font-size:16px;font-weight:600">${prj.name}</h3></div>
      <div style="margin-bottom:var(--spacing-md)">${prj.description || ''}</div>
      <div><span class="badge badge-info">${prj.total_findings ?? 0} findings</span></div>
      <div style="margin-top:var(--spacing-md);text-align:right"><span class="text-xs text-muted">${prj.updated_at ? 'Updated ' + prj.updated_at : ''}</span></div>
    </div>`;
    grid.appendChild(card);
  }
}

async function loadFindings() {
  const tbody = document.getElementById('findings-tbody');
  if (!tbody) return;
  tbody.innerHTML = '<tr><td colspan="8"><div class="spinner"></div></td></tr>';
  const urlParams = new URLSearchParams(window.location.search);
  const projectId = urlParams.get('project_id');
  const db = loadLocalDb();
  let findings = [];
  db.projects.forEach(p => { if (!projectId || p.id === projectId) findings = findings.concat(p.findings||[]); });
  if (!Array.isArray(findings) || findings.length === 0) {
    tbody.innerHTML = '<tr><td colspan="8" style="color:var(--text-tertiary)">Нет данных по находкам.</td></tr>';
    return;
  }
  tbody.innerHTML = '';
  for (const finding of findings) {
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td><span class="badge badge-${finding.severity}">${finding.severity || ''}</span></td>
      <td><code>${finding.ruleId || ''}</code></td>
      <td>${finding.message || ''}</td>
      <td><code>${finding.file || ''}</code></td>
      <td>${finding.tool || ''}</td>
      <td><span class="badge badge-${finding.status}">${finding.status || ''}</span></td>
      <td>${finding.projectName || ''}</td>
      <td>${finding.created_at || ''}</td>`;
    tbody.appendChild(tr);
  }
}


