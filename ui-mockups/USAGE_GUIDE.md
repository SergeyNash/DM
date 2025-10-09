# SARIF Manager - Usage Guide

Практическое руководство по использованию UI компонентов и паттернов.

## 🎯 Начало работы

### Просмотр макетов

1. **Локально в браузере:**
   ```
   Откройте ui-mockups/index.html в браузере
   ```

2. **С локальным сервером (рекомендуется):**
   ```bash
   cd ui-mockups
   python -m http.server 8000
   # или
   npx serve .
   ```
   Затем откройте: http://localhost:8000

### Навигация

- **Главная страница:** `index.html` - обзор всех макетов
- **Dashboard:** `dashboard.html` - начальная точка UX flow
- **Component Showcase:** `components/components-showcase.html` - каталог компонентов

## 📋 Использование компонентов

### Severity Badges

**Назначение:** Визуализация уровня серьезности уязвимости

**Использование:**
```html
<span class="badge badge-critical">Critical</span>
<span class="badge badge-high">High</span>
<span class="badge badge-medium">Medium</span>
<span class="badge badge-low">Low</span>
<span class="badge badge-info">Info</span>
```

**Когда использовать:**
- В таблицах находок
- В карточках проектов
- В детальном просмотре
- В фильтрах

**Best Practices:**
- Всегда используйте правильный color class
- Не изменяйте цвета вручную
- Добавляйте title attribute для accessibility

### Status Badges

**Назначение:** Индикация статуса в жизненном цикле находки

**Использование:**
```html
<span class="badge badge-new">New</span>
<span class="badge badge-confirmed">Confirmed</span>
<span class="badge badge-false-positive">False Positive</span>
<span class="badge badge-fixed">Fixed</span>
```

**Когда использовать:**
- В таблицах для quick status view
- В sidebar detail page
- В фильтрах и группировках

**Best Practices:**
- Сделайте кликабельными для быстрого изменения статуса
- Добавьте tooltip с дополнительной информацией
- Используйте consistent naming

### Buttons

**Типы кнопок:**

1. **Primary** - основное действие на странице
   ```html
   <button class="btn btn-primary">Save Changes</button>
   ```

2. **Secondary** - вторичные действия
   ```html
   <button class="btn btn-secondary">Cancel</button>
   ```

3. **Outline** - менее важные действия
   ```html
   <button class="btn btn-outline">Export</button>
   ```

**Best Practices:**
- Одна primary кнопка на секцию/форму
- Используйте иконки для улучшения понимания
- Добавляйте loading states для async actions
- Disabled state для недоступных действий

### Cards

**Базовая структура:**
```html
<div class="card">
  <div class="card-header">
    <h3 class="card-title">Card Title</h3>
    <button class="btn btn-sm btn-outline">Action</button>
  </div>
  <div class="card-body">
    <!-- Content -->
  </div>
</div>
```

**Best Practices:**
- Используйте consistent padding
- Header опционален для простых cards
- Группируйте связанный контент

### Stat Cards

**Использование:**
```html
<div class="stat-card">
  <div class="stat-card-header">
    <div>
      <div class="stat-label">Total Findings</div>
      <div class="stat-value">1,247</div>
    </div>
    <div class="stat-icon" style="background: #eff6ff; color: #2563eb;">
      🔍
    </div>
  </div>
  <div class="stat-trend positive">
    <span>↓</span>
    <span>12% from last week</span>
  </div>
</div>
```

**Best Practices:**
- Icon color должен соответствовать метрике
- Trend опционален
- Используйте понятные units (K для thousands, M для millions)

### Tables

**Базовая структура:**
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

**Best Practices:**
- Используйте table-container для scroll
- Добавляйте trackBy для performance
- Сортируемые колонки должны иметь visual indicator
- Row hover для лучшего UX

### Search Box

**Использование:**
```html
<div class="search-box">
  <span>🔍</span>
  <input type="text" placeholder="Search..." />
</div>
```

**Best Practices:**
- Добавьте debounce (300ms) для live search
- Показывайте clear button когда есть текст
- Loading indicator при поиске
- Показывайте результаты count

### Forms

**Input Field:**
```html
<div class="form-group">
  <label class="form-label">Field Label *</label>
  <input type="text" class="form-input" placeholder="Enter..." required />
</div>
```

**Select:**
```html
<div class="form-group">
  <label class="form-label">Select Option</label>
  <select class="form-input">
    <option>Option 1</option>
    <option>Option 2</option>
  </select>
</div>
```

**Textarea:**
```html
<div class="form-group">
  <label class="form-label">Description</label>
  <textarea class="form-input form-textarea" rows="4"></textarea>
</div>
```

**Best Practices:**
- Обязательные поля отмечайте *
- Используйте placeholder для примеров
- Validation messages под полем
- Focus state должен быть заметен

## 🎨 Работа с цветами

### Severity Colors

**Применение:**
```css
/* В CSS */
color: var(--severity-critical);
background: var(--severity-high);

/* Inline стили */
style="color: var(--severity-critical);"
```

**Mapping уровней:**
- `error` → Critical
- `warning` → Medium/High (зависит от контекста)
- `note` → Low
- `none` → Info

### Status Colors

**Workflow цветов:**
- **Purple (New)** → Новая находка, требует review
- **Orange (Confirmed)** → Подтверждена, требует fix
- **Gray (False Positive)** → Ложное срабатывание, закрыта
- **Green (Fixed)** → Исправлена, resolved

## 📊 Layout Patterns

### Dashboard Layout

**Структура:**
1. Stats Grid (4 columns)
2. Charts Row (2 columns)
3. Recent Findings Table
4. Projects Overview Grid

**Best Practices:**
- Stats всегда наверху для quick overview
- Critical information first
- Actionable items в видимой области

### List/Table Layout

**Структура:**
1. Search and Filters bar
2. Quick filters (preset buttons)
3. Main table
4. Pagination

**Best Practices:**
- Filters collapsible на mobile
- Sticky header для больших таблиц
- Virtual scroll для > 100 rows

### Detail Layout

**Структура:**
- Main content (2/3 width)
- Sidebar с metadata (1/3 width)
- Sticky sidebar при scroll

**Best Practices:**
- Progressive disclosure (collapsible sections)
- Related actions в sidebar
- Breadcrumbs для navigation

## 🔄 User Flows

### Finding Investigation Flow

1. **Dashboard** → Видим Critical findings count
2. **Click на stat** → Переход на Findings с фильтром Critical
3. **Click на finding** → Detail page
4. **Review & Change Status** → Confirmed/False Positive/Fixed
5. **Add Comment** → Документация решения
6. **Back to Findings** → Continue review

### Upload Flow

1. **Upload Page** → Select project
2. **Drag & Drop** SARIF files
3. **Review Summary** → Total findings, tools detected
4. **Start Upload** → Processing в background
5. **Navigate to Project** → View results

## 🎯 Responsive Breakpoints

### Desktop (> 1024px)
- Full sidebar visible
- 4 column stats grid
- 2 column charts layout
- Full table visible

### Tablet (768px - 1024px)
- Full sidebar
- 2 column stats grid
- 1-2 column charts
- Horizontal scroll tables

### Mobile (< 768px)
- Hidden sidebar (drawer)
- 1 column stats grid
- Stacked charts
- Simplified table (cards?)

## 🚀 Migration to Angular

### Component Mapping

**HTML Mockup → Angular Component**

```
dashboard.html → DashboardComponent
  - stats grid → StatCardComponent (reusable)
  - charts → ChartComponent
  - table → FindingsTableComponent

projects.html → ProjectsComponent
  - project cards → ProjectCardComponent
  - modal → CreateProjectDialogComponent

findings.html → FindingsComponent
  - filter bar → FindingsFilterComponent
  - table → FindingsTableComponent (shared)
  
finding-detail.html → FindingDetailComponent
  - code block → CodeSnippetComponent
  - comments → CommentsComponent
  - sidebar → FindingMetadataComponent

upload.html → UploadComponent
  - dropzone → FileDropzoneComponent
  - file list → UploadedFilesListComponent
```

### CSS → SCSS

Конвертация CSS Variables в SCSS:
```scss
// _variables.scss
$primary-blue: #2563eb;
$severity-critical: #dc2626;
// ...

// или используйте CSS Variables как есть
:root {
  --primary-blue: #2563eb;
}
```

### Static → Dynamic

**Замена mock данных:**
```typescript
// Before (static)
<span class="badge badge-critical">Critical</span>

// After (dynamic)
<span [class]="'badge badge-' + finding.severity.toLowerCase()">
  {{ finding.severity }}
</span>
```

## 📝 Checklist перед реализацией

- [ ] Изучить все 5 страниц макетов
- [ ] Просмотреть Component Showcase
- [ ] Понять color system (severity/status)
- [ ] Проверить responsive behavior
- [ ] Определить shared components
- [ ] Спланировать Angular structure
- [ ] Подготовить icon library (заменить emoji)
- [ ] Настроить Tailwind/Material theme
- [ ] Создать service для API calls
- [ ] Реализовать state management

## 🔗 Полезные ссылки

- **SARIF Format:** https://sarifweb.azurewebsites.net/
- **OWASP Top 10:** https://owasp.org/www-project-top-ten/
- **CWE Database:** https://cwe.mitre.org/
- **Angular Material:** https://material.angular.io/
- **Tailwind CSS:** https://tailwindcss.com/

---

**Вопросы?** Обратитесь к README.md и ARCHITECTURE.md для дополнительной информации.

