// SARIF Manager - Shared UI interactions

document.addEventListener('DOMContentLoaded', () => {
  try {
    setActiveSidebarItem();
    initFindingsSearch();
    initUploadInteractions();
    const loc = location.pathname.split('/').pop() || '';
    if (loc === 'dashboard.html') loadDashboard();
    if (loc === 'projects.html') loadProjects();
    if (loc === 'findings.html') loadFindings();
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

async function fetchApi(url, options={}) {
  const resp = await fetch(url, options);
  if (!resp.ok) throw new Error(await resp.text());
  return await resp.json();
}

// --- UPLOAD LOGIC ---
function initUploadInteractions() {
  const fileInput = document.getElementById('file-input');
  const uploadedFiles = document.getElementById('uploaded-files');
  const uploadSummary = document.getElementById('upload-summary');
  const uploadArea = document.querySelector('.upload-area');

  if (!fileInput || !uploadArea) return;

  async function handleFiles(files) {
    if (!files || !files.length) return;
    if (uploadedFiles) uploadedFiles.style.display = 'block';
    // Показываем loader
    uploadedFiles.innerHTML = '<div class="spinner" style="margin:32px auto;"></div>';
    let summaryData;
    try {
      const fd = new FormData();
      Array.from(files).forEach(f => fd.append('file', f));
      const projectSelect = document.getElementById('project-select');
      if (projectSelect && projectSelect.value && projectSelect.value !== 'Select a project...') {
        fd.append('project_name', projectSelect.value);
      }
      summaryData = await fetchApi('/api/upload', {method:'POST', body: fd});
    } catch (e) {
      uploadedFiles.innerHTML = '<div class="empty-state-text" style="color:red">Ошибка загрузки: '+String(e)+'</div>';
      return;
    }
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
  uploadArea.addEventListener('drop', (e) => {
    e.preventDefault(); uploadArea.classList.remove('drag-over'); handleFiles(e.dataTransfer.files);
  });
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

async function loadDashboard() {
  const cont = document.getElementById('dashboard-content');
  if (!cont) return;
  cont.innerHTML = '<div class="spinner" style="margin:64px auto"></div>';
  let stats;
  try {
    stats = await fetchApi('/api/statistics');
  } catch (e) {
    cont.innerHTML = '<div class="empty-state-text" style="color:red">Ошибка загрузки статистики</div>';
    return;
  }
  if (!stats || !stats.summary) {
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
  let projects;
  try {
    projects = await fetchApi('/api/projects');
  } catch {
    grid.innerHTML = '<div class="empty-state-text" style="color:red">Ошибка загрузки проектов</div>';
    return;
  }
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
  let findings;
  try {
    findings = await fetchApi('/api/findings' + (projectId ? ('?project_id=' + encodeURIComponent(projectId)) : ''));
  } catch {
    tbody.innerHTML = '<tr><td colspan="8" style="color:red">Ошибка загрузки данных</td></tr>';
    return;
  }
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


