# Требования и правила разработки

> **📖 Детальная архитектура системы описана в [ARCHITECTURE.md](./ARCHITECTURE.md)**

## 1. Архитектурные принципы

### 1.1 Краткий обзор архитектуры

**Backend:** Clean Architecture (.NET 8 + EF Core + SQLite)
- API Layer → Application Layer → Domain Layer → Infrastructure Layer

**Frontend:** Angular 17+ Standalone Components
- Core Services → Shared Components → Feature Modules

**Для полного описания архитектуры, диаграмм потоков данных, примеров кода и ADRs см. [ARCHITECTURE.md](./ARCHITECTURE.md)**

## 2. Технологический стек

### 2.1 Backend
- **.NET 8.0** - LTS версия
- **ASP.NET Core Web API** - REST API
- **Entity Framework Core 8.0** - ORM
- **SQLite** - База данных для PoC
- **FluentValidation** - Валидация
- **AutoMapper** - Маппинг DTO ↔ Entity
- **Serilog** - Логирование

### 2.2 Frontend
- **Angular 17+** - Standalone компоненты
- **TypeScript 5+** - Строгая типизация
- **RxJS** - Реактивное программирование
- **Angular Material** - UI компоненты
- **Tailwind CSS** - Utility-first стилизация
- **Angular CDK** - Виртуализация, drag-and-drop
- **Angular Reactive Forms** - Формы с валидацией
- **Chart.js / ng2-charts** - Визуализация данных
- **HttpClient** - HTTP запросы с interceptors

## 3. Соглашения по коду

### 3.1 Backend (C#)

#### Именование
```csharp
// PascalCase для классов, методов, свойств
public class FindingService { }
public void ProcessSarifReport() { }
public string RuleId { get; set; }

// camelCase для приватных полей с _
private readonly IRepository _repository;

// UPPER_CASE для констант
public const int MAX_FILE_SIZE_MB = 50;

// Интерфейсы с префиксом I
public interface IFindingService { }
```

#### Структура классов
```csharp
public class FindingService : IFindingService
{
    // 1. Константы
    private const int DEFAULT_PAGE_SIZE = 50;
    
    // 2. Приватные поля
    private readonly IFindingRepository _repository;
    private readonly ILogger<FindingService> _logger;
    
    // 3. Конструктор
    public FindingService(
        IFindingRepository repository,
        ILogger<FindingService> logger)
    {
        _repository = repository;
        _logger = logger;
    }
    
    // 4. Публичные методы
    public async Task<FindingDto> GetByIdAsync(int id) { }
    
    // 5. Приватные методы
    private void ValidateInput() { }
}
```

#### Async/Await правила
- Все I/O операции асинхронные
- Методы заканчиваются на `Async`
- Используем `CancellationToken` где возможно
- Избегаем `.Result` и `.Wait()`

```csharp
// ✅ Правильно
public async Task<List<Finding>> GetFindingsAsync(
    int projectId, 
    CancellationToken ct = default)
{
    return await _repository.GetByProjectAsync(projectId, ct);
}

// ❌ Неправильно
public List<Finding> GetFindings(int projectId)
{
    return _repository.GetByProjectAsync(projectId).Result;
}
```

### 3.2 Frontend (TypeScript/Angular)

#### Именование
```typescript
// PascalCase для компонентов и классов
export class FindingsListComponent { }
export class FindingService { }
export interface FindingDto { }
export type FindingsFilter = { };

// camelCase для методов, свойства, переменные
private fetchFindings(): void { }
public isLoading = true;

// UPPER_SNAKE_CASE для констант
export const MAX_FILE_SIZE_MB = 50;
export const API_BASE_URL = '/api';

// Суффиксы для Angular сущностей
// Component: .component.ts
// Service: .service.ts
// Directive: .directive.ts
// Pipe: .pipe.ts
// Guard: .guard.ts
```

#### Структура компонента
```typescript
// findings-list.component.ts

// 1. Импорты (группировка)
import { Component, Input, Output, EventEmitter, OnInit, OnDestroy } from '@angular/core';  // Angular core
import { CommonModule } from '@angular/common';  // Angular common
import { MatTableModule } from '@angular/material/table';  // Material
import { Observable, Subject, takeUntil } from 'rxjs';  // RxJS
import { FindingService } from '@/core/services';  // Services
import { Finding } from '@/models';  // Models

// 2. Component декоратор
@Component({
  selector: 'app-findings-list',
  standalone: true,
  imports: [CommonModule, MatTableModule],
  templateUrl: './findings-list.component.html',
  styleUrls: ['./findings-list.component.scss']
})
export class FindingsListComponent implements OnInit, OnDestroy {
  // 3. Inputs/Outputs
  @Input() projectId!: number;
  @Output() selectFinding = new EventEmitter<Finding>();
  
  // 4. Public свойства (для template)
  findings$!: Observable<Finding[]>;
  isLoading = false;
  selectedId: number | null = null;
  
  // 5. Private свойства
  private destroy$ = new Subject<void>();
  
  // 6. Constructor (DI)
  constructor(private findingService: FindingService) {}
  
  // 7. Lifecycle hooks
  ngOnInit(): void {
    this.loadFindings();
  }
  
  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }
  
  // 8. Public методы (для template)
  onSelect(finding: Finding): void {
    this.selectedId = finding.id;
    this.selectFinding.emit(finding);
  }
  
  // 9. Private методы
  private loadFindings(): void {
    this.findings$ = this.findingService
      .getByProject(this.projectId)
      .pipe(takeUntil(this.destroy$));
  }
}
```

#### Angular правила
- **Standalone компоненты** (Angular 17+) - избегаем NgModules где возможно
- **OnPush change detection** для оптимизации
- **RxJS patterns**: используем async pipe в template, избегаем subscribe в компонентах
- **Unsubscribe**: takeUntil pattern для очистки subscriptions
- **Dependency Injection**: все через constructor
- **Типизация**: строгая типизация везде

```typescript
// ✅ Правильно - async pipe + OnPush
@Component({
  selector: 'app-finding-card',
  standalone: true,
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `
    <div *ngIf="finding$ | async as finding">
      {{ finding.title }}
    </div>
  `
})
export class FindingCardComponent {
  @Input() findingId!: number;
  finding$!: Observable<Finding>;
  
  constructor(private service: FindingService) {}
  
  ngOnInit(): void {
    this.finding$ = this.service.getById(this.findingId);
  }
}

// ❌ Неправильно - manual subscribe + memory leak
export class FindingCardComponent {
  finding: Finding;
  
  ngOnInit() {
    this.service.getById(this.findingId).subscribe(f => {
      this.finding = f;  // Memory leak!
    });
  }
}
```

#### Структура сервиса
```typescript
// finding.service.ts

import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map, catchError } from 'rxjs/operators';
import { Finding } from '@/models';

@Injectable({
  providedIn: 'root'  // Singleton service
})
export class FindingService {
  private readonly apiUrl = '/api/findings';
  
  constructor(private http: HttpClient) {}
  
  getById(id: number): Observable<Finding> {
    return this.http.get<{ data: Finding }>(`${this.apiUrl}/${id}`)
      .pipe(
        map(response => response.data),
        catchError(this.handleError)
      );
  }
  
  private handleError(error: any): Observable<never> {
    console.error('API Error:', error);
    throw error;
  }
}
```

## 4. API контракты

### 4.1 REST принципы
- **Ресурсо-ориентированные URL**: `/api/projects/{id}/findings`
- **HTTP методы**: GET (чтение), POST (создание), PUT (обновление), DELETE (удаление)
- **Статус коды**: 200 (OK), 201 (Created), 204 (No Content), 400 (Bad Request), 404 (Not Found), 500 (Internal Error)
- **JSON формат** для request/response

### 4.2 Структура эндпоинтов
```
GET    /api/projects                    - Список проектов
POST   /api/projects                    - Создать проект
GET    /api/projects/{id}               - Получить проект
PUT    /api/projects/{id}               - Обновить проект
DELETE /api/projects/{id}               - Удалить проект

POST   /api/projects/{id}/upload        - Загрузить SARIF
GET    /api/projects/{id}/findings      - Получить находки (с фильтрами)
GET    /api/findings/{id}               - Детали находки
PATCH  /api/findings/{id}/status        - Изменить статус
POST   /api/findings/{id}/comments      - Добавить комментарий

GET    /api/analytics/dashboard         - Метрики дашборда
GET    /api/analytics/export            - Экспорт CSV/JSON
```

### 4.3 Формат ответов

#### Успешный ответ (один объект)
```json
{
  "data": {
    "id": 1,
    "name": "Project Alpha"
  }
}
```

#### Успешный ответ (список с пагинацией)
```json
{
  "data": [...],
  "pagination": {
    "page": 1,
    "pageSize": 50,
    "totalCount": 1234,
    "totalPages": 25
  }
}
```

#### Ошибка
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input",
    "details": [
      {
        "field": "name",
        "message": "Name is required"
      }
    ]
  }
}
```

## 5. Модель данных

### 5.1 Основные сущности

```csharp
// Project - Проект
public class Project
{
    public int Id { get; set; }
    public string Name { get; set; } = string.Empty;
    public string? Description { get; set; }
    public DateTime CreatedAt { get; set; }
    public DateTime UpdatedAt { get; set; }
    
    // Navigation
    public ICollection<SarifReport> Reports { get; set; } = [];
    public ICollection<Finding> Findings { get; set; } = [];
}

// SarifReport - Загруженный отчет
public class SarifReport
{
    public int Id { get; set; }
    public int ProjectId { get; set; }
    public string ToolName { get; set; } = string.Empty;
    public string ToolVersion { get; set; } = string.Empty;
    public string FileName { get; set; } = string.Empty;
    public string FilePath { get; set; } = string.Empty;
    public long FileSizeBytes { get; set; }
    public DateTime UploadedAt { get; set; }
    
    // Navigation
    public Project Project { get; set; } = null!;
    public ICollection<Finding> Findings { get; set; } = [];
}

// Finding - Уязвимость/находка
public class Finding
{
    public int Id { get; set; }
    public int ProjectId { get; set; }
    public int ReportId { get; set; }
    
    // SARIF поля
    public string RuleId { get; set; } = string.Empty;
    public string Message { get; set; } = string.Empty;
    public string? FilePath { get; set; }
    public int? StartLine { get; set; }
    public int? StartColumn { get; set; }
    public string Level { get; set; } = string.Empty; // error, warning, note
    
    // Нормализованные поля
    public NormalizedSeverity Severity { get; set; }
    public FindingStatus Status { get; set; }
    
    public DateTime CreatedAt { get; set; }
    public DateTime UpdatedAt { get; set; }
    
    // Raw SARIF
    public string? RawSarifJson { get; set; }
    
    // Navigation
    public Project Project { get; set; } = null!;
    public SarifReport Report { get; set; } = null!;
    public ICollection<FindingComment> Comments { get; set; } = [];
}

// FindingComment - Комментарий
public class FindingComment
{
    public int Id { get; set; }
    public int FindingId { get; set; }
    public string Text { get; set; } = string.Empty;
    public DateTime CreatedAt { get; set; }
    
    // Navigation
    public Finding Finding { get; set; } = null!;
}

// Enums
public enum NormalizedSeverity
{
    Info = 0,
    Low = 1,
    Medium = 2,
    High = 3,
    Critical = 4
}

public enum FindingStatus
{
    New = 0,
    Confirmed = 1,
    FalsePositive = 2,
    Fixed = 3
}
```

## 6. Git workflow

### 6.1 Ветки
- `main` - production-ready код
- `develop` - разработка (базовая ветка)
- `feature/*` - новые фичи
- `bugfix/*` - исправления багов
- `hotfix/*` - срочные исправления в main

### 6.2 Commit messages
Формат: `<type>(<scope>): <subject>`

**Types:**
- `feat`: новая функциональность
- `fix`: исправление бага
- `refactor`: рефакторинг без изменения функциональности
- `docs`: документация
- `style`: форматирование, отступы
- `test`: добавление тестов
- `chore`: обновление зависимостей, конфигурация

**Примеры:**
```
feat(findings): add status change functionality
fix(upload): handle large SARIF files correctly
refactor(api): extract validation logic to separate service
docs(readme): update setup instructions
```

## 7. Тестирование

### 7.1 Backend
- **Unit тесты**: xUnit + Moq + FluentAssertions
- **Integration тесты**: WebApplicationFactory
- Минимум 70% code coverage для critical paths
- Тесты в отдельном проекте: `SarifManager.Tests`

```csharp
public class FindingServiceTests
{
    [Fact]
    public async Task GetByIdAsync_ExistingId_ReturnsFindig()
    {
        // Arrange
        var mockRepo = new Mock<IFindingRepository>();
        var service = new FindingService(mockRepo.Object);
        
        // Act
        var result = await service.GetByIdAsync(1);
        
        // Assert
        result.Should().NotBeNull();
    }
}
```

### 7.2 Frontend
- **Unit тесты**: Jasmine + Karma / Jest (рекомендуется)
- **Component тесты**: Angular Testing Library / TestBed
- **E2E тесты**: Playwright / Cypress (опционально для PoC)
- Тестируем поведение, а не implementation details

```typescript
// finding-list.component.spec.ts
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { of } from 'rxjs';
import { FindingsListComponent } from './findings-list.component';
import { FindingService } from '@/core/services';

describe('FindingsListComponent', () => {
  let component: FindingsListComponent;
  let fixture: ComponentFixture<FindingsListComponent>;
  let mockService: jasmine.SpyObj<FindingService>;
  
  beforeEach(async () => {
    mockService = jasmine.createSpyObj('FindingService', ['getByProject']);
    
    await TestBed.configureTestingModule({
      imports: [FindingsListComponent],
      providers: [
        { provide: FindingService, useValue: mockService }
      ]
    }).compileComponents();
    
    fixture = TestBed.createComponent(FindingsListComponent);
    component = fixture.componentInstance;
  });
  
  it('should display findings when loaded', () => {
    const mockFindings = [{ id: 1, title: 'SQL Injection' }];
    mockService.getByProject.and.returnValue(of(mockFindings));
    
    component.projectId = 1;
    fixture.detectChanges();
    
    expect(fixture.nativeElement.textContent).toContain('SQL Injection');
  });
});
```

## 8. Обработка ошибок

### 8.1 Backend
```csharp
// Custom exceptions
public class NotFoundException : Exception { }
public class ValidationException : Exception { }
public class SarifParsingException : Exception { }

// Global error handler middleware
app.UseMiddleware<ErrorHandlingMiddleware>();
```

### 8.2 Frontend
```typescript
// HTTP Interceptor для глобальной обработки ошибок
import { HttpInterceptorFn } from '@angular/common/http';
import { inject } from '@angular/core';
import { catchError, throwError } from 'rxjs';
import { ToastService } from '@/core/services';

export const errorInterceptor: HttpInterceptorFn = (req, next) => {
  const toast = inject(ToastService);
  
  return next(req).pipe(
    catchError((error) => {
      // Глобальная обработка ошибок
      if (error.status === 404) {
        toast.error('Resource not found');
      } else if (error.status >= 500) {
        toast.error('Server error. Please try again later.');
      }
      return throwError(() => error);
    })
  );
};

// В компоненте - локальная обработка
export class FindingsComponent {
  loadFindings(): void {
    this.findingService.getAll()
      .pipe(
        catchError((error) => {
          console.error('Failed to load findings', error);
          this.errorMessage = 'Failed to load findings';
          return of([]);  // Fallback значение
        })
      )
      .subscribe();
  }
}

// Global error handler
import { ErrorHandler, Injectable } from '@angular/core';

@Injectable()
export class GlobalErrorHandler implements ErrorHandler {
  handleError(error: Error): void {
    console.error('Global error:', error);
    // Отправка в логирование/мониторинг
  }
}
```

## 9. Производительность

### 9.1 Backend оптимизации
- Использовать `AsNoTracking()` для read-only запросов
- Eager loading с `Include()` для избежания N+1
- Пагинация для больших наборов данных
- Background tasks для тяжелых операций (SARIF parsing)

```csharp
// ✅ Правильно
var findings = await _context.Findings
    .AsNoTracking()
    .Include(f => f.Report)
    .Where(f => f.ProjectId == projectId)
    .Skip((page - 1) * pageSize)
    .Take(pageSize)
    .ToListAsync();
```

### 9.2 Frontend оптимизации
- **OnPush change detection** для всех компонентов
- **TrackBy** функции для *ngFor
- **Виртуализация** для списков > 100 элементов (CDK Virtual Scroll)
- **Debounce** для поиска и фильтров
- **Lazy loading** модулей через роутинг
- **Мемоизация** сложных pipe вычислений

```typescript
// OnPush change detection
@Component({
  selector: 'app-findings-list',
  changeDetection: ChangeDetectionStrategy.OnPush
})

// TrackBy для оптимизации *ngFor
export class FindingsListComponent {
  trackByFindingId(index: number, finding: Finding): number {
    return finding.id;
  }
}

// Template
<div *ngFor="let finding of findings; trackBy: trackByFindingId">
  {{ finding.title }}
</div>

// Virtual scrolling с CDK
import { CdkVirtualScrollViewport } from '@angular/cdk/scrolling';

<cdk-virtual-scroll-viewport itemSize="50" class="viewport">
  <div *cdkVirtualFor="let finding of findings">
    {{ finding.title }}
  </div>
</cdk-virtual-scroll-viewport>

// Debounced search с RxJS
import { debounceTime, distinctUntilChanged } from 'rxjs/operators';

searchControl = new FormControl('');

ngOnInit(): void {
  this.searchControl.valueChanges
    .pipe(
      debounceTime(300),
      distinctUntilChanged(),
      takeUntil(this.destroy$)
    )
    .subscribe(searchTerm => {
      this.performSearch(searchTerm);
    });
}

// Lazy loading через роутинг
const routes: Routes = [
  {
    path: 'findings',
    loadComponent: () => import('./features/findings/findings.component')
      .then(m => m.FindingsComponent)
  }
];
```

## 10. Безопасность

### 10.1 PoC ограничения
- ⚠️ No authentication/authorization
- ⚠️ CORS настройки для локальной разработки
- ⚠️ Базовая валидация входных данных

### 10.2 Обязательные меры
- Валидация всех входных данных
- Проверка размера загружаемых файлов
- SQL injection защита (параметризованные запросы EF)
- XSS защита (React auto-escaping)
- Ограничение rate limit для upload API

```csharp
// Валидация размера файла
[RequestSizeLimit(52_428_800)] // 50 MB
[HttpPost("upload")]
public async Task<IActionResult> Upload(IFormFile file) { }
```

## 11. Логирование

### 11.1 Backend (Serilog)
```csharp
Log.Information("Processing SARIF report {FileName} for project {ProjectId}", 
    fileName, projectId);
    
Log.Warning("Large file uploaded: {FileSize}MB", fileSizeMb);

Log.Error(ex, "Failed to parse SARIF report {FileName}", fileName);
```

### 11.2 Уровни логирования
- **Debug**: детальная информация для отладки
- **Information**: общий flow приложения
- **Warning**: неожиданные ситуации, но работа продолжается
- **Error**: ошибки с exception

## 12. Документация

### 12.1 Код документация
- XML comments для публичных API в C#
- JSDoc для сложных утилит в TypeScript
- README в каждом feature-модуле

### 12.2 API документация
- Swagger/OpenAPI для backend API
- Автогенерация из контроллеров

```csharp
/// <summary>
/// Retrieves a finding by its identifier
/// </summary>
/// <param name="id">The finding identifier</param>
/// <returns>The finding details</returns>
/// <response code="200">Finding found</response>
/// <response code="404">Finding not found</response>
[HttpGet("{id}")]
[ProducesResponseType(typeof(FindingDto), StatusCodes.Status200OK)]
[ProducesResponseType(StatusCodes.Status404NotFound)]
public async Task<IActionResult> GetById(int id) { }
```

## 13. Чеклист перед коммитом

- [ ] Код компилируется без ошибок
- [ ] Все тесты проходят
- [ ] Нет warning'ов компилятора (если можно избежать)
- [ ] Код отформатирован (Prettier для TS, встроенный formatter для C#)
- [ ] Добавлены необходимые типы/интерфейсы
- [ ] Обработаны edge cases и ошибки
- [ ] Обновлена документация (если нужно)

## 14. IDE настройки

### 14.1 Visual Studio / Rider
- EditorConfig для консистентного форматирования
- ReSharper code style (если используется)

### 14.2 VS Code / WebStorm
- **Расширения (VS Code)**: 
  - C# Dev Kit (backend)
  - Angular Language Service
  - ESLint
  - Prettier
  - Tailwind CSS IntelliSense
  - Angular Snippets
- **WebStorm**: отличная встроенная поддержка Angular из коробки
- Format on save включен
- TSLint/ESLint настроен согласно Angular Style Guide

---

**Готовы к разработке!** 🚀

*Документ может дополняться в процессе разработки.*

## Деплой и запуск

### Пошаговая инструкция

1. Соберите фронтенд и скопируйте сборку Angular в backend/wwwroot:

   ```bash
   cd frontend
   npm install
   npm run build -- --output-path=../backend/wwwroot --configuration production
   ```

2. Сборка и запуск backend:

   ```bash
   cd ../backend
   dotnet build
   dotnet run
   ```
   
   Теперь single-page frontend и API отдаются одним процессом (port 5000 или другой по настройке)

3. Продакшен деплой (если требуется):

   - Выполнить `dotnet publish -c Release` и развернуть артефакт на сервере или в Docker.

---

