# SARIF Manager UI Mockups - Files Overview

Полный список созданных файлов и их назначение.

## 📂 Структура проекта

```
ui-mockups/
├── 📄 index.html                           # Главная страница с обзором всех макетов
├── 📄 dashboard.html                       # Dashboard с метриками и статистикой
├── 📄 projects.html                        # Управление проектами
├── 📄 findings.html                        # Таблица находок с фильтрацией
├── 📄 finding-detail.html                  # Детальный просмотр уязвимости
├── 📄 upload.html                          # Загрузка SARIF файлов
│
├── 📁 assets/
│   ├── 📁 css/
│   │   └── 📄 styles.css                   # Единый CSS файл со всеми стилями
│   └── 📁 js/                              # (Пусто - для будущих скриптов)
│
├── 📁 components/
│   └── 📄 components-showcase.html         # Каталог UI компонентов
│
├── 📖 README.md                            # Основная документация проекта
├── 📖 USAGE_GUIDE.md                       # Руководство по использованию
└── 📖 FILES_OVERVIEW.md                    # Этот файл
```

## 📄 Описание файлов

### HTML Страницы (Макеты)

#### `index.html` (Главная страница)
**Размер:** ~10 KB  
**Назначение:** Точка входа в UI макеты, навигация по всем страницам  
**Содержит:**
- Обзор всех 5 страниц макетов
- Описание дизайн системы
- Список ключевых возможностей
- Информацию о tech stack
- Ссылки на документацию

**Ключевые секции:**
- Quick Start
- Pages Grid (карточки всех макетов)
- Design System Overview
- Features List
- Tech Stack

---

#### `dashboard.html` (Dashboard)
**Размер:** ~18 KB  
**Назначение:** Главная страница приложения с overview метриками  
**Содержит:**
- 4 Stat Cards (Total, Critical, High, Active Projects)
- Severity Distribution Chart (pie chart visualization)
- Tool Distribution (horizontal bars)
- Recent Critical & High Findings Table
- Projects Overview Grid

**UI Компоненты:**
- Stat Cards с трендами
- Pie chart (CSS conic-gradient)
- Progress bars для tool distribution
- Sortable table
- Project cards grid

**Интерактивность:**
- Hover эффекты на карточках проектов
- Кликабельные строки таблицы → finding-detail.html
- Navigation через sidebar

---

#### `projects.html` (Projects List)
**Размер:** ~15 KB  
**Назначение:** Управление проектами безопасности  
**Содержит:**
- Search bar с фильтрацией
- Grid карточек проектов (4 примера)
- Project metadata (название, описание, stats)
- Severity distribution bars
- Tools badges
- Empty state card для создания проекта
- Create Project Modal

**UI Компоненты:**
- Search box
- Project cards с hover эффектами
- Severity progress bars
- Modal dialog
- Form inputs

**Интерактивность:**
- Поиск по проектам
- Клик на карточку → findings.html
- Кнопка "New Project" → открывает modal
- Modal с формой создания проекта

---

#### `findings.html` (Findings Table)
**Размер:** ~20 KB  
**Назначение:** Таблица всех находок с расширенной фильтрацией  
**Содержит:**
- Quick Stats Bar (5 stat cards)
- Search box для текстового поиска
- Quick filter buttons (All, Critical & High, New, Confirmed)
- Advanced filters dropdowns (Severity, Status, Tool)
- Sortable findings table (10 примеров)
- Pagination controls

**UI Компоненты:**
- Compact stat cards
- Search box
- Filter buttons и dropdowns
- Table с checkboxes
- Severity и Status badges
- Pagination

**Интерактивность:**
- Текстовый поиск
- Фильтрация по severity/status/tool
- Сортировка колонок
- Checkbox для bulk actions
- Row click → finding-detail.html
- Pagination navigation

---

#### `finding-detail.html` (Finding Detail)
**Размер:** ~16 KB  
**Назначение:** Детальный просмотр одной уязвимости  
**Содержит:**

**Main Content (2/3 ширины):**
- Description с Security Impact
- Location (file, line, column)
- Code snippet с подсветкой уязвимой строки
- Recommended Fix example
- Collapsible SARIF raw JSON
- Comments section (2 примера + add form)

**Sidebar (1/3 ширины):**
- Metadata (Status, Severity, Tool, Project)
- Timestamps (Created, Updated)
- Source Report info
- CWE/CVE References
- History timeline

**UI Компоненты:**
- Code blocks с syntax highlighting
- Alert boxes (Security Impact)
- Success boxes (Fix Example)
- Comment cards
- Textarea для нового комментария
- Metadata cards
- Timeline

**Интерактивность:**
- Previous/Next navigation
- Change Status dropdown
- Toggle Raw JSON visibility
- Add Comment form
- Copy code snippets
- External links (CWE, OWASP)

---

#### `upload.html` (Upload SARIF)
**Размер:** ~14 KB  
**Назначение:** Загрузка SARIF отчетов в проект  
**Содержит:**
- Project selector dropdown
- Drag & Drop upload area
- File browser button
- Uploaded files list (3 примера с разными статусами)
- Upload Summary stats (hidden initially)
- Supported Tools showcase (SAST, DAST, SCA)

**UI Компоненты:**
- Select dropdown
- Upload area с drag & drop states
- File list items с progress bars
- Processing indicators
- Info cards
- Stats grid

**Интерактивность:**
- Drag & Drop файлов
- File input через browser
- Progress bars для обработки
- Remove uploaded files
- "Start Upload" button
- Toggle visibility uploaded files/summary

---

#### `components/components-showcase.html` (Components Catalog)
**Размер:** ~12 KB  
**Назначение:** Каталог всех переиспользуемых UI компонентов  
**Содержит:**
- Severity Badges (5 вариантов + code)
- Status Badges (4 варианта + code)
- Buttons (Primary, Secondary, Outline, Small, Icon + code)
- Cards (Basic, With Actions + code)
- Search Box (+ code)
- Stat Cards (3 примера + code)
- Form Elements (Input, Select, Textarea + code)
- Code Block examples
- Color Palette (Severity + Status colors)

**Назначение:**
- Reference для разработчиков
- Copy-paste code snippets
- Визуализация дизайн системы
- Примеры использования

---

### CSS Файлы

#### `assets/css/styles.css`
**Размер:** ~12 KB  
**Назначение:** Единый файл стилей для всех макетов  
**Содержит:**

**CSS Variables:**
- Primary colors
- Severity colors (5)
- Status colors (4)
- Neutral colors (Gray scale)
- Spacing system
- Border radius
- Shadows

**Component Styles:**
- Layout (sidebar, main-content)
- Navigation
- Cards
- Buttons (3 типа + размеры)
- Badges (severity + status)
- Tables
- Forms
- Search box
- Stat cards
- Modal
- Code blocks
- Upload area
- Empty states
- Loading spinner

**Utilities:**
- Flexbox helpers
- Typography
- Spacing
- Colors

**Responsive:**
- Desktop breakpoint (> 1024px)
- Tablet breakpoint (768-1024px)
- Mobile breakpoint (< 768px)

---

### Документация

#### `README.md`
**Размер:** ~8 KB  
**Содержит:**
- Структура проекта
- Описание всех 5 страниц
- Дизайн система (colors, typography, spacing)
- Основные компоненты с code examples
- Responsive design strategy
- Инструкции по запуску макетов
- UX Patterns
- Следующие шаги для реализации
- Заметки и рекомендации

---

#### `USAGE_GUIDE.md`
**Размер:** ~6 KB  
**Содержит:**
- Начало работы (как открыть макеты)
- Использование каждого компонента
- Best practices для каждого компонента
- Работа с цветами
- Layout patterns
- User flows (примеры)
- Responsive breakpoints
- Migration guide (HTML → Angular)
- Checklist перед реализацией
- Полезные ссылки

---

#### `FILES_OVERVIEW.md` (Этот файл)
**Размер:** ~4 KB  
**Содержит:**
- Структура проекта
- Описание каждого файла
- Размеры и назначение
- Краткая справка

---

## 📊 Статистика

### Файлы по типам:
- **HTML страницы:** 6 файлов (index + 5 макетов + 1 showcase)
- **CSS:** 1 файл (unified styles)
- **Документация:** 3 файла (README, USAGE_GUIDE, FILES_OVERVIEW)
- **Всего:** 11 файлов

### Размеры (примерно):
- **HTML:** ~110 KB total
- **CSS:** ~12 KB
- **Markdown:** ~18 KB
- **Всего:** ~140 KB

### Компоненты:
- **Severity Badges:** 5 вариантов
- **Status Badges:** 4 варианта
- **Button Styles:** 3 типа + размеры
- **Card Types:** 3 типа (card, stat-card, project-card)
- **Form Elements:** 3 типа (input, select, textarea)
- **Tables:** 1 общий стиль
- **Utilities:** 20+ utility classes

### Цветовая палитра:
- **Severity Colors:** 5 (Critical, High, Medium, Low, Info)
- **Status Colors:** 4 (New, Confirmed, False Positive, Fixed)
- **UI Colors:** Primary Blue + Gray scale

## 🎯 Что дальше?

1. **Просмотреть макеты:**
   - Откройте `index.html` в браузере
   - Изучите каждую страницу
   - Проверьте responsive поведение

2. **Изучить компоненты:**
   - Откройте `components/components-showcase.html`
   - Ознакомьтесь с code examples
   - Скопируйте нужные snippets

3. **Прочитать документацию:**
   - `README.md` - overview проекта
   - `USAGE_GUIDE.md` - практическое руководство

4. **Начать реализацию:**
   - Настроить Angular проект
   - Портировать компоненты
   - Интегрировать с backend API

## 🔗 Навигация между файлами

```
index.html (Start Here)
    ├── dashboard.html (Main App Page)
    │   └── finding-detail.html (Click on table row)
    ├── projects.html
    │   └── findings.html (Click on project card)
    │       └── finding-detail.html
    ├── upload.html
    └── components/components-showcase.html (Reference)
```

## ✅ Quality Checklist

- [x] Все страницы созданы
- [x] Единый CSS файл
- [x] Responsive design
- [x] Component showcase
- [x] Документация (README)
- [x] Usage guide
- [x] Files overview
- [x] Навигация между страницами
- [x] Code examples
- [x] Mock данные

---

**Готово к использованию!** 🚀

Откройте `index.html` для начала.

