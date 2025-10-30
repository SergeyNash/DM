// SARIF Manager - Shared UI interactions

document.addEventListener('DOMContentLoaded', () => {
  try {
    setActiveSidebarItem();
    initFindingsSearch();
    initUploadInteractions();
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

function initUploadInteractions() {
  const fileInput = document.getElementById('file-input');
  const uploadedFiles = document.getElementById('uploaded-files');
  const uploadSummary = document.getElementById('upload-summary');
  const uploadArea = document.querySelector('.upload-area');

  if (!fileInput || !uploadArea) return;

  const handleFiles = (files) => {
    if (!files || !files.length) return;
    if (uploadedFiles) uploadedFiles.style.display = 'block';
    if (uploadSummary) uploadSummary.style.display = 'block';

    // Populate uploaded files list
    if (uploadedFiles) {
      // Clear demo items while keeping the section title
      const nodes = Array.from(uploadedFiles.children).slice(1);
      nodes.forEach((n) => n.remove());
      Array.from(files).forEach((file) => {
        const container = document.createElement('div');
        container.style.padding = 'var(--spacing-md)';
        container.style.border = '1px solid var(--border-color)';
        container.style.borderRadius = 'var(--border-radius)';
        container.style.marginBottom = 'var(--spacing-sm)';
        container.style.display = 'flex';
        container.style.alignItems = 'center';
        container.style.gap = 'var(--spacing-md)';
        container.innerHTML = `
          <div style="width: 40px; height: 40px; background: #eff6ff; border-radius: var(--border-radius); display: flex; align-items: center; justify-content: center; font-size: 20px;">📄</div>
          <div style="flex: 1;">
            <div style="font-weight: 500; margin-bottom: 2px;">${file.name}</div>
            <div class="text-xs text-muted">${formatFileSize(file.size)} • Pending</div>
          </div>
          <div style="display: flex; align-items: center; gap: 8px;">
            <span class="badge badge-info" style="font-size: 11px;">Queued</span>
          </div>
        `;
        uploadedFiles.appendChild(container);
      });
    }

    // Populate summary
    if (uploadSummary) {
      const statsGrid = uploadSummary.querySelector('[style*="grid-template-columns"]');
      if (statsGrid) {
        // Keep existing, but update counts
        const values = statsGrid.querySelectorAll('.text-bold');
        if (values[0]) values[0].textContent = String(files.length);
        if (values[1]) values[1].textContent = formatFileSize(Array.from(files).reduce((s, f) => s + (f.size || 0), 0));
        // Leave findings/tools numbers as placeholders for now
      }
    }
  };

  fileInput.addEventListener('change', (e) => handleFiles(e.target.files));

  uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.classList.remove('drag-over');
    handleFiles(e.dataTransfer.files);
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


