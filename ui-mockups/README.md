# SARIF Manager - UI Mockups

Статические HTML/CSS макеты для визуализации дизайна и UX системы SARIF Manager.

## 📁 Структура файлов

```
ui-mockups/
├── assets/
│   ├── css/
│   │   └── styles.css          # Единый файл стилей для всех макетов
│   └── js/                     # Placeholder для будущих скриптов
├── components/
│   └── components-showcase.html # Каталог переиспользуемых компонентов
├── dashboard.html              # Главная страница с метриками
├── projects.html               # Список проектов
├── findings.html               # Таблица находок с фильтрацией
├── finding-detail.html         # Детальный просмотр одной находки
├── upload.html                 # Загрузка SARIF файлов
└── README.md                   # Этот файл
```

## 🎨 Страницы

### 1. Dashboard (`dashboard.html`)
**Назначение:** Главная страница с overview метриками и статистикой

**Ключевые элементы:**
- Stat Cards - карточки с ключевыми метриками (Total, Critical, High, Active Projects)
- Severity Distribution Chart - визуализация распределения по уровням серьезности
- Tool Distribution - статистика по инструментам сканирования
- Recent Findings Table - последние критические и важные находки
- Projects Overview - краткий обзор проектов

**Интерактивность:**
- Клик по карточкам проектов → переход на `findings.html`
- Клик по строкам таблицы → переход на `finding-detail.html`

### 2. Projects (`projects.html`)
**Назначение:** Управление проектами безопасности

**Ключевые элементы:**
- Search bar с фильтрацией
- Grid карточек проектов с:
  - Основной информацией (название, описание)
  - Статистикой (Total Findings, Critical/High, Reports)
  - Severity Distribution bar
  - Метаданными (последнее обновление, инструменты)
- Empty state card для создания нового проекта
- Modal для создания проекта

**Интерактивность:**
- Hover эффекты на карточках
- Клик по карточке → переход на `findings.html`
- Кнопка "New Project" → открывает modal

### 3. Findings (`findings.html`)
**Назначение:** Таблица всех находок проекта с расширенной фильтрацией

**Ключевые элементы:**
- Quick stats bar (Total, Critical, High, Medium, New)
- Search box для текстового поиска
- Quick filter buttons (All, Critical & High, New, Confirmed)
- Advanced filters (Severity, Status, Tool)
- Sortable table columns
- Severity и Status badges
- Pagination

**Интерактивность:**
- Checkbox для bulk actions
- Клик по строке → переход на `finding-detail.html`
- Dropdown меню для фильтров
- Сортировка по колонкам

### 4. Finding Detail (`finding-detail.html`)
**Назначение:** Детальный просмотр одной уязвимости

**Ключевые элементы:**
- Full description с Security Impact
- Recommended Fix
- Location information (File, Line, Column)
- Code snippet с подсветкой уязвимой строки
- Fix example
- SARIF raw JSON data (collapsible)
- Comments section
- Sidebar с метаданными:
  - Status, Severity, Tool
  - Project, Created, Updated
  - CWE/CVE references
  - History timeline

**Интерактивность:**
- Navigation (← → Previous/Next)
- Change Status dropdown
- Toggle Raw JSON visibility
- Add Comment form
- Copy code snippets

### 5. Upload (`upload.html`)
**Назначение:** Загрузка SARIF отчетов в проект

**Ключевые элементы:**
- Project selector dropdown
- Drag & Drop upload area
- File browser button
- Uploaded files list с:
  - Filename, size, tool
  - Processing status/progress
  - Remove button
- Upload Summary stats
- Supported Tools showcase (SAST, DAST, SCA)

**Интерактивность:**
- Drag & Drop файлов
- File input через browser
- Progress bars для обработки
- Remove uploaded files
- "Start Upload" button

### 6. Components Showcase (`components/components-showcase.html`)
**Назначение:** Каталог переиспользуемых UI компонентов

**Компоненты:**
- Severity Badges (Critical, High, Medium, Low, Info)
- Status Badges (New, Confirmed, False Positive, Fixed)
- Buttons (Primary, Secondary, Outline, Small, Icon)
- Cards (Basic, With Actions)
- Search Box
- Stat Cards
- Form Elements (Input, Select, Textarea)
- Code Blocks
- Color Palette

## 🎨 Дизайн система

### Цвета

#### Severity Colors
```css
--severity-critical: #dc2626  /* Red 600 */
--severity-high: #ea580c      /* Orange 600 */
--severity-medium: #f59e0b    /* Amber 500 */
--severity-low: #84cc16       /* Lime 500 */
--severity-info: #06b6d4      /* Cyan 500 */
```

#### Status Colors
```css
--status-new: #8b5cf6         /* Purple 500 */
--status-confirmed: #f97316   /* Orange 500 */
--status-false-positive: #64748b /* Slate 500 */
--status-fixed: #10b981       /* Emerald 500 */
```

#### Neutral Colors
```css
--gray-50 to --gray-900       /* Tailwind Gray scale */
```

### Typography
- **Font Family:** System fonts (-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto')
- **Base Font Size:** 14px
- **Headings:** 
  - Page Title: 24px, 700 weight
  - Card Title: 16px, 600 weight
  - Section Title: 11px, 600 weight, uppercase

### Spacing
```css
--spacing-xs: 0.25rem   (4px)
--spacing-sm: 0.5rem    (8px)
--spacing-md: 1rem      (16px)
--spacing-lg: 1.5rem    (24px)
--spacing-xl: 2rem      (32px)
--spacing-2xl: 3rem     (48px)
```

### Border Radius
```css
--border-radius: 8px
--border-radius-sm: 4px
--border-radius-lg: 12px
```

### Shadows
```css
--shadow-sm: 0 1px 2px rgba(0,0,0,0.05)
--shadow-md: 0 4px 6px rgba(0,0,0,0.1)
--shadow-lg: 0 10px 15px rgba(0,0,0,0.1)
--shadow-xl: 0 20px 25px rgba(0,0,0,0.1)
```

## 🧩 Основные компоненты

### Badges
```html
<!-- Severity -->
<span class="badge badge-critical">Critical</span>
<span class="badge badge-high">High</span>
<span class="badge badge-medium">Medium</span>
<span class="badge badge-low">Low</span>
<span class="badge badge-info">Info</span>

<!-- Status -->
<span class="badge badge-new">New</span>
<span class="badge badge-confirmed">Confirmed</span>
<span class="badge badge-false-positive">False Positive</span>
<span class="badge badge-fixed">Fixed</span>
```

### Buttons
```html
<button class="btn btn-primary">Primary</button>
<button class="btn btn-secondary">Secondary</button>
<button class="btn btn-outline">Outline</button>
<button class="btn btn-primary btn-sm">Small</button>
<button class="btn btn-primary btn-icon">🔍</button>
```

### Cards
```html
<div class="card">
  <div class="card-header">
    <h3 class="card-title">Card Title</h3>
  </div>
  <div class="card-body">
    <!-- Content -->
  </div>
</div>
```

### Stat Cards
```html
<div class="stat-card">
  <div class="stat-card-header">
    <div>
      <div class="stat-label">Label</div>
      <div class="stat-value">1,247</div>
    </div>
    <div class="stat-icon">🔍</div>
  </div>
  <div class="stat-trend positive">
    <span>↓</span>
    <span>12% decrease</span>
  </div>
</div>
```

### Search Box
```html
<div class="search-box">
  <span>🔍</span>
  <input type="text" placeholder="Search..." />
</div>
```

### Tables
```html
<div class="table-container">
  <table class="table">
    <thead>
      <tr>
        <th>Column 1</th>
        <th>Column 2</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>Data 1</td>
        <td>Data 2</td>
      </tr>
    </tbody>
  </table>
</div>
```

## 📱 Responsive Design

### Breakpoints
- **Desktop:** > 1024px - полная функциональность
- **Tablet:** 768px - 1024px - адаптированная grid система
- **Mobile:** < 768px - скрытый sidebar, 1 колонка

### Mobile Adaptations
- Sidebar превращается в drawer (скрыт по умолчанию)
- Stats grid: Desktop (4 columns) → Tablet (2 columns) → Mobile (1 column)
- Tables: горизонтальный scroll
- Filters: collapse в dropdown

## 🚀 Запуск макетов

### Локальный просмотр
1. Откройте любой HTML файл в браузере
2. Навигация между страницами работает через ссылки

### С Live Server (VS Code)
```bash
# Установите расширение Live Server
# Щелкните правой кнопкой на dashboard.html
# Выберите "Open with Live Server"
```

### С Python HTTP Server
```bash
cd ui-mockups
python -m http.server 8000
# Откройте http://localhost:8000/dashboard.html
```

## 🎯 UX Patterns

### Progressive Disclosure
- Детали скрыты за кликами (SARIF JSON, dropdown меню)
- Фильтры сворачиваются/разворачиваются
- Comments section внизу detail page

### Visual Hierarchy
1. **Critical Information First:** Severity badges, stat cards
2. **Contextual Actions:** Кнопки рядом с контентом
3. **Color Coding:** Красный (Critical) → Желтый (Medium) → Зеленый (Low/Fixed)

### Quick Actions
- One-click status change (dropdown)
- Bulk operations (checkbox selection)
- Quick filters (preset buttons)
- Keyboard shortcuts friendly (можно добавить в реализации)

### Feedback
- Hover states на всех интерактивных элементах
- Active states для выбранных items
- Progress bars для loading
- Empty states для отсутствия данных

## 🔄 Следующие шаги

### Переход к реализации:
1. **Backend:** Реализовать API согласно контрактам из `ARCHITECTURE.md`
2. **Frontend:** Портировать макеты в Angular компоненты
3. **Integration:** Подключить real data вместо mock данных
4. **Interactivity:** Добавить реальную фильтрацию, сортировку, AJAX
5. **Charts:** Интегрировать Chart.js для visualizations

## 📝 Заметки

- Макеты используют emoji иконки для наглядности. В реальной реализации использовать иконочные шрифты (Material Icons, Font Awesome) или SVG
- Mock данные hardcoded для демонстрации. В production заменить на API calls
- JavaScript functionality минимальна (только для демонстрации модалов и dropdowns)
- Accessibility (a11y) не полностью реализована в макетах - добавить в реализации:
  - ARIA labels
  - Keyboard navigation
  - Screen reader support
  - Focus management

## 🎨 Дизайн вдохновение

UI дизайн вдохновлен современными Application Security Orchestration and Correlation (ASOC) решениями:
- GitHub Advanced Security
- Snyk
- Checkmarx One
- Veracode

**Ключевые принципы:**
- Clean, minimal design
- Focus on data density без clutter
- Strong visual hierarchy
- Consistent color language для severity/status
- Quick actions и shortcuts

---

**Автор:** AI Assistant  
**Дата:** October 2025  
**Версия:** 1.0

