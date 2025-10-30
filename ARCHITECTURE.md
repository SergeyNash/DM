# Архитектура системы SARIF Manager

## 1. Общая архитектура

### 1.1 Высокоуровневая диаграмма

```
┌──────────────────────────────────────────────────────────────┐
│                     Client Browser                           │
│  ┌────────────────────────────────────────────────────────┐  │
│  │         Angular 17+ SPA (Port 4200)                    │  │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐  │  │
│  │  │Dashboard │ │Projects  │ │Findings  │ │Upload    │  │  │
│  │  │ Module   │ │ Module   │ │ Module   │ │ Module   │  │  │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘  │  │
│  │  ┌──────────────────────────────────────────────────┐  │  │
│  │  │   Shared Services & Components Layer            │  │  │
│  │  └──────────────────────────────────────────────────┘  │  │
│  └────────────────────────────────────────────────────────┘  │
└───────────────────────┬──────────────────────────────────────┘
                        │ HTTP/REST (JSON)
┌───────────────────────▼──────────────────────────────────────┐
│          ASP.NET Core Web API (Port 5000)                    │
│  ┌────────────────────────────────────────────────────────┐  │
│  │                 API Layer                              │  │
│  │  [Controllers] → [DTOs] → [Validation]                │  │
│  └───────────────────────┬────────────────────────────────┘  │
│  ┌───────────────────────▼────────────────────────────────┐  │
│  │              Application Layer                         │  │
│  │  [Services] → [Business Logic] → [Interfaces]         │  │
│  └───────────────────────┬────────────────────────────────┘  │
│  ┌───────────────────────▼────────────────────────────────┐  │
│  │                Domain Layer                            │  │
│  │  [Entities] → [Value Objects] → [Enums]               │  │
│  └───────────────────────┬────────────────────────────────┘  │
│  ┌───────────────────────▼────────────────────────────────┐  │
│  │            Infrastructure Layer                        │  │
│  │  [Repositories] → [EF Core] → [File Storage]          │  │
│  └────────────────────────────────────────────────────────┘  │
└───────────────────────┬──────────────────────────────────────┘
                        │
┌───────────────────────▼──────────────────────────────────────┐
│              SQLite Database (sarif-manager.db)              │
│  [Projects] [SarifReports] [Findings] [Comments]            │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│                File System Storage                           │
│  /uploads/{projectId}/{reportId}/original.sarif              │
└──────────────────────────────────────────────────────────────┘
```

### 1.2 Архитектурные принципы

- **Separation of Concerns**: четкое разделение слоев и ответственностей
- **Dependency Inversion**: зависимость от абстракций, а не конкретных реализаций
- **Single Responsibility**: каждый класс/компонент отвечает за одну задачу
- **DRY (Don't Repeat Yourself)**: переиспользование кода через shared модули
- **KISS (Keep It Simple)**: простота решений, избегание overengineering

---

## 2. Backend Architecture (Clean Architecture)

### 2.1 Структура проекта

```
SarifManager/
├── src/
│   ├── SarifManager.Api/                    # API Layer
│   │   ├── Controllers/
│   │   │   ├── ProjectsController.cs
│   │   │   ├── FindingsController.cs
│   │   │   ├── UploadController.cs
│   │   │   └── AnalyticsController.cs
│   │   ├── DTOs/
│   │   │   ├── Requests/
│   │   │   │   ├── CreateProjectRequest.cs
│   │   │   │   ├── UpdateFindingStatusRequest.cs
│   │   │   │   └── GetFindingsRequest.cs
│   │   │   └── Responses/
│   │   │       ├── ProjectDto.cs
│   │   │       ├── FindingDto.cs
│   │   │       ├── FindingDetailDto.cs
│   │   │       └── DashboardMetricsDto.cs
│   │   ├── Filters/
│   │   │   └── ValidationFilter.cs
│   │   ├── Middleware/
│   │   │   ├── ErrorHandlingMiddleware.cs
│   │   │   └── LoggingMiddleware.cs
│   │   ├── Validators/
│   │   │   ├── CreateProjectValidator.cs
│   │   │   └── UploadSarifValidator.cs
│   │   ├── Mappers/
│   │   │   └── MappingProfile.cs          # AutoMapper
│   │   ├── Program.cs
│   │   └── appsettings.json
│   │
│   ├── SarifManager.Application/            # Application Layer
│   │   ├── Services/
│   │   │   ├── ProjectService.cs
│   │   │   ├── FindingService.cs
│   │   │   ├── SarifParsingService.cs
│   │   │   ├── AnalyticsService.cs
│   │   │   └── FileStorageService.cs
│   │   ├── Interfaces/
│   │   │   ├── IProjectService.cs
│   │   │   ├── IFindingService.cs
│   │   │   ├── ISarifParsingService.cs
│   │   │   ├── IAnalyticsService.cs
│   │   │   └── IFileStorageService.cs
│   │   ├── Models/
│   │   │   ├── FindingsFilter.cs
│   │   │   ├── PaginationParams.cs
│   │   │   └── SarifParseResult.cs
│   │   └── Exceptions/
│   │       ├── NotFoundException.cs
│   │       ├── ValidationException.cs
│   │       └── SarifParsingException.cs
│   │
│   ├── SarifManager.Domain/                 # Domain Layer
│   │   ├── Entities/
│   │   │   ├── Project.cs
│   │   │   ├── SarifReport.cs
│   │   │   ├── Finding.cs
│   │   │   └── FindingComment.cs
│   │   ├── Enums/
│   │   │   ├── NormalizedSeverity.cs
│   │   │   └── FindingStatus.cs
│   │   └── ValueObjects/
│   │       └── Location.cs
│   │
│   └── SarifManager.Infrastructure/         # Infrastructure Layer
│       ├── Data/
│       │   ├── ApplicationDbContext.cs
│       │   ├── Configurations/
│       │   │   ├── ProjectConfiguration.cs
│       │   │   ├── SarifReportConfiguration.cs
│       │   │   ├── FindingConfiguration.cs
│       │   │   └── FindingCommentConfiguration.cs
│       │   └── Migrations/
│       ├── Repositories/
│       │   ├── ProjectRepository.cs
│       │   ├── FindingRepository.cs
│       │   ├── SarifReportRepository.cs
│       │   └── Interfaces/
│       │       ├── IProjectRepository.cs
│       │       ├── IFindingRepository.cs
│       │       └── ISarifReportRepository.cs
│       └── Storage/
│           └── LocalFileStorage.cs
│
└── tests/
    ├── SarifManager.UnitTests/
    ├── SarifManager.IntegrationTests/
    └── SarifManager.Api.Tests/
```

### 2.2 Слои и их ответственности

#### API Layer (Presentation)
**Задачи:**
- HTTP endpoints (Controllers)
- Валидация входных данных (FluentValidation)
- Сериализация/десериализация JSON
- Middleware для обработки ошибок, логирования
- Маппинг Entity ↔ DTO (AutoMapper)

**Зависимости:** Application Layer

```csharp
// ProjectsController.cs
[ApiController]
[Route("api/[controller]")]
public class ProjectsController : ControllerBase
{
    private readonly IProjectService _projectService;
    private readonly IMapper _mapper;
    private readonly ILogger<ProjectsController> _logger;

    public ProjectsController(
        IProjectService projectService,
        IMapper mapper,
        ILogger<ProjectsController> logger)
    {
        _projectService = projectService;
        _mapper = mapper;
        _logger = logger;
    }

    [HttpGet]
    public async Task<ActionResult<ApiResponse<List<ProjectDto>>>> GetAll(
        [FromQuery] string? search,
        CancellationToken ct)
    {
        var projects = await _projectService.GetAllAsync(search, ct);
        var dtos = _mapper.Map<List<ProjectDto>>(projects);
        return Ok(new ApiResponse<List<ProjectDto>> { Data = dtos });
    }

    [HttpPost]
    public async Task<ActionResult<ApiResponse<ProjectDto>>> Create(
        [FromBody] CreateProjectRequest request,
        CancellationToken ct)
    {
        var project = await _projectService.CreateAsync(request.Name, request.Description, ct);
        var dto = _mapper.Map<ProjectDto>(project);
        return CreatedAtAction(nameof(GetById), new { id = dto.Id }, 
            new ApiResponse<ProjectDto> { Data = dto });
    }
}
```

#### Application Layer (Business Logic)
**Задачи:**
- Бизнес-логика
- Координация между репозиториями
- Транзакции
- Преобразование данных
- Работа с доменными сущностями

**Зависимости:** Domain Layer, Infrastructure Interfaces

```csharp
// SarifParsingService.cs
public class SarifParsingService : ISarifParsingService
{
    private readonly ILogger<SarifParsingService> _logger;

    public async Task<SarifParseResult> ParseAsync(
        Stream sarifStream, 
        CancellationToken ct)
    {
        try
        {
            var sarif = await JsonSerializer.DeserializeAsync<SarifLog>(
                sarifStream, 
                cancellationToken: ct);

            if (sarif?.Runs == null || sarif.Runs.Length == 0)
                throw new SarifParsingException("No runs found in SARIF file");

            var findings = new List<Finding>();
            
            foreach (var run in sarif.Runs)
            {
                var toolName = run.Tool.Driver.Name;
                var toolVersion = run.Tool.Driver.Version ?? "unknown";

                foreach (var result in run.Results ?? [])
                {
                    var finding = MapToFinding(result, toolName);
                    findings.Add(finding);
                }
            }

            return new SarifParseResult
            {
                ToolName = sarif.Runs[0].Tool.Driver.Name,
                ToolVersion = sarif.Runs[0].Tool.Driver.Version,
                Findings = findings
            };
        }
        catch (JsonException ex)
        {
            _logger.LogError(ex, "Failed to parse SARIF JSON");
            throw new SarifParsingException("Invalid SARIF format", ex);
        }
    }

    private Finding MapToFinding(Result sarifResult, string toolName)
    {
        var location = sarifResult.Locations?.FirstOrDefault();
        var artifactLocation = location?.PhysicalLocation?.ArtifactLocation;
        var region = location?.PhysicalLocation?.Region;

        return new Finding
        {
            RuleId = sarifResult.RuleId ?? "unknown",
            Message = sarifResult.Message.Text ?? sarifResult.Message.Markdown ?? "",
            FilePath = artifactLocation?.Uri ?? artifactLocation?.UriBaseId,
            StartLine = region?.StartLine,
            StartColumn = region?.StartColumn,
            Level = sarifResult.Level?.ToString() ?? "warning",
            Severity = NormalizeSeverity(sarifResult.Level),
            Status = FindingStatus.New,
            CreatedAt = DateTime.UtcNow,
            UpdatedAt = DateTime.UtcNow,
            RawSarifJson = JsonSerializer.Serialize(sarifResult)
        };
    }

    private NormalizedSeverity NormalizeSeverity(ResultLevel? level)
    {
        return level switch
        {
            ResultLevel.Error => NormalizedSeverity.High,
            ResultLevel.Warning => NormalizedSeverity.Medium,
            ResultLevel.Note => NormalizedSeverity.Low,
            _ => NormalizedSeverity.Info
        };
    }
}
```

#### Domain Layer (Core)
**Задачи:**
- Доменные сущности (entities)
- Бизнес-правила на уровне сущностей
- Enums, Value Objects
- Независимость от технологий

**Зависимости:** Нет (чистый C#)

```csharp
// Finding.cs (Domain Entity)
public class Finding
{
    public int Id { get; set; }
    public int ProjectId { get; set; }
    public int ReportId { get; set; }
    
    // SARIF fields
    public string RuleId { get; set; } = string.Empty;
    public string Message { get; set; } = string.Empty;
    public string? FilePath { get; set; }
    public int? StartLine { get; set; }
    public int? StartColumn { get; set; }
    public string Level { get; set; } = string.Empty;
    
    // Normalized fields
    public NormalizedSeverity Severity { get; set; }
    public FindingStatus Status { get; set; }
    
    public DateTime CreatedAt { get; set; }
    public DateTime UpdatedAt { get; set; }
    
    public string? RawSarifJson { get; set; }
    
    // Navigation properties
    public Project Project { get; set; } = null!;
    public SarifReport Report { get; set; } = null!;
    public ICollection<FindingComment> Comments { get; set; } = [];

    // Business logic methods
    public bool CanTransitionTo(FindingStatus newStatus)
    {
        // Бизнес-правила для переходов статусов
        return (Status, newStatus) switch
        {
            (FindingStatus.New, FindingStatus.Confirmed) => true,
            (FindingStatus.New, FindingStatus.FalsePositive) => true,
            (FindingStatus.Confirmed, FindingStatus.Fixed) => true,
            (FindingStatus.Confirmed, FindingStatus.FalsePositive) => true,
            (_, FindingStatus.New) => true, // Можно вернуть в New из любого статуса
            _ => false
        };
    }

    public void UpdateStatus(FindingStatus newStatus)
    {
        if (!CanTransitionTo(newStatus))
            throw new InvalidOperationException(
                $"Cannot transition from {Status} to {newStatus}");

        Status = newStatus;
        UpdatedAt = DateTime.UtcNow;
    }
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

#### Infrastructure Layer
**Задачи:**
- Реализация репозиториев
- Entity Framework Core конфигурация
- Миграции БД
- Внешние сервисы (файловое хранилище)

**Зависимости:** Domain Layer, EF Core, SQLite

```csharp
// ApplicationDbContext.cs
public class ApplicationDbContext : DbContext
{
    public DbSet<Project> Projects => Set<Project>();
    public DbSet<SarifReport> SarifReports => Set<SarifReport>();
    public DbSet<Finding> Findings => Set<Finding>();
    public DbSet<FindingComment> FindingComments => Set<FindingComment>();

    public ApplicationDbContext(DbContextOptions<ApplicationDbContext> options)
        : base(options)
    {
    }

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        base.OnModelCreating(modelBuilder);
        
        // Apply configurations
        modelBuilder.ApplyConfiguration(new ProjectConfiguration());
        modelBuilder.ApplyConfiguration(new SarifReportConfiguration());
        modelBuilder.ApplyConfiguration(new FindingConfiguration());
        modelBuilder.ApplyConfiguration(new FindingCommentConfiguration());
    }
}

// FindingConfiguration.cs
public class FindingConfiguration : IEntityTypeConfiguration<Finding>
{
    public void Configure(EntityTypeBuilder<Finding> builder)
    {
        builder.ToTable("Findings");
        
        builder.HasKey(f => f.Id);
        
        builder.Property(f => f.RuleId)
            .IsRequired()
            .HasMaxLength(200);
        
        builder.Property(f => f.Message)
            .IsRequired()
            .HasMaxLength(2000);
        
        builder.Property(f => f.FilePath)
            .HasMaxLength(500);
        
        builder.Property(f => f.Severity)
            .HasConversion<string>()
            .HasMaxLength(20);
        
        builder.Property(f => f.Status)
            .HasConversion<string>()
            .HasMaxLength(20);
        
        // Relationships
        builder.HasOne(f => f.Project)
            .WithMany(p => p.Findings)
            .HasForeignKey(f => f.ProjectId)
            .OnDelete(DeleteBehavior.Cascade);
        
        builder.HasOne(f => f.Report)
            .WithMany(r => r.Findings)
            .HasForeignKey(f => f.ReportId)
            .OnDelete(DeleteBehavior.Cascade);
        
        // Indexes
        builder.HasIndex(f => f.ProjectId);
        builder.HasIndex(f => f.ReportId);
        builder.HasIndex(f => f.Severity);
        builder.HasIndex(f => f.Status);
        builder.HasIndex(f => f.RuleId);
    }
}

// FindingRepository.cs
public class FindingRepository : IFindingRepository
{
    private readonly ApplicationDbContext _context;

    public FindingRepository(ApplicationDbContext context)
    {
        _context = context;
    }

    public async Task<Finding?> GetByIdAsync(int id, CancellationToken ct = default)
    {
        return await _context.Findings
            .Include(f => f.Report)
            .Include(f => f.Comments)
            .FirstOrDefaultAsync(f => f.Id == id, ct);
    }

    public async Task<(List<Finding> Items, int TotalCount)> GetFilteredAsync(
        FindingsFilter filter,
        PaginationParams pagination,
        CancellationToken ct = default)
    {
        var query = _context.Findings
            .AsNoTracking()
            .Include(f => f.Report)
            .AsQueryable();

        // Apply filters
        if (filter.ProjectId.HasValue)
            query = query.Where(f => f.ProjectId == filter.ProjectId.Value);

        if (filter.Severities?.Any() == true)
            query = query.Where(f => filter.Severities.Contains(f.Severity));

        if (filter.Statuses?.Any() == true)
            query = query.Where(f => filter.Statuses.Contains(f.Status));

        if (!string.IsNullOrWhiteSpace(filter.SearchText))
        {
            var search = filter.SearchText.ToLower();
            query = query.Where(f =>
                f.RuleId.ToLower().Contains(search) ||
                f.Message.ToLower().Contains(search) ||
                (f.FilePath != null && f.FilePath.ToLower().Contains(search)));
        }

        var totalCount = await query.CountAsync(ct);

        // Apply pagination and ordering
        var items = await query
            .OrderByDescending(f => f.Severity)
            .ThenByDescending(f => f.CreatedAt)
            .Skip((pagination.Page - 1) * pagination.PageSize)
            .Take(pagination.PageSize)
            .ToListAsync(ct);

        return (items, totalCount);
    }

    public async Task<Finding> CreateAsync(Finding finding, CancellationToken ct = default)
    {
        _context.Findings.Add(finding);
        await _context.SaveChangesAsync(ct);
        return finding;
    }

    public async Task UpdateAsync(Finding finding, CancellationToken ct = default)
    {
        _context.Findings.Update(finding);
        await _context.SaveChangesAsync(ct);
    }
}
```

---

## 3. Frontend Architecture (Angular)

### 3.1 Структура проекта

```
frontend/
├── src/
│   ├── app/
│   │   ├── core/                           # Singleton сервисы, глобальные утилиты
│   │   │   ├── services/
│   │   │   │   ├── api/
│   │   │   │   │   ├── project-api.service.ts
│   │   │   │   │   ├── finding-api.service.ts
│   │   │   │   │   └── analytics-api.service.ts
│   │   │   │   ├── state/
│   │   │   │   │   ├── project-state.service.ts
│   │   │   │   │   └── finding-state.service.ts
│   │   │   │   ├── toast.service.ts
│   │   │   │   └── loading.service.ts
│   │   │   ├── guards/
│   │   │   │   └── data-loaded.guard.ts
│   │   │   ├── interceptors/
│   │   │   │   ├── error.interceptor.ts
│   │   │   │   ├── loading.interceptor.ts
│   │   │   │   └── base-url.interceptor.ts
│   │   │   └── index.ts
│   │   │
│   │   ├── shared/                         # Переиспользуемые компоненты
│   │   │   ├── components/
│   │   │   │   ├── severity-badge/
│   │   │   │   │   ├── severity-badge.component.ts
│   │   │   │   │   ├── severity-badge.component.html
│   │   │   │   │   └── severity-badge.component.scss
│   │   │   │   ├── status-badge/
│   │   │   │   ├── confirm-dialog/
│   │   │   │   ├── loading-spinner/
│   │   │   │   └── error-message/
│   │   │   ├── pipes/
│   │   │   │   ├── date-format.pipe.ts
│   │   │   │   ├── file-size.pipe.ts
│   │   │   │   └── highlight-search.pipe.ts
│   │   │   ├── directives/
│   │   │   │   └── auto-focus.directive.ts
│   │   │   └── index.ts
│   │   │
│   │   ├── features/                       # Feature-модули
│   │   │   ├── projects/
│   │   │   │   ├── components/
│   │   │   │   │   ├── project-list/
│   │   │   │   │   │   ├── project-list.component.ts
│   │   │   │   │   │   ├── project-list.component.html
│   │   │   │   │   │   └── project-list.component.scss
│   │   │   │   │   ├── project-card/
│   │   │   │   │   ├── create-project-dialog/
│   │   │   │   │   └── edit-project-dialog/
│   │   │   │   ├── projects.component.ts
│   │   │   │   └── projects.routes.ts
│   │   │   │
│   │   │   ├── findings/
│   │   │   │   ├── components/
│   │   │   │   │   ├── findings-table/
│   │   │   │   │   │   ├── findings-table.component.ts
│   │   │   │   │   │   ├── findings-table.component.html
│   │   │   │   │   │   └── findings-table.component.scss
│   │   │   │   │   ├── findings-filter/
│   │   │   │   │   ├── finding-detail/
│   │   │   │   │   └── finding-comments/
│   │   │   │   ├── findings.component.ts
│   │   │   │   └── findings.routes.ts
│   │   │   │
│   │   │   ├── dashboard/
│   │   │   │   ├── components/
│   │   │   │   │   ├── metrics-overview/
│   │   │   │   │   ├── severity-chart/
│   │   │   │   │   ├── tool-distribution-chart/
│   │   │   │   │   └── timeline-chart/
│   │   │   │   ├── dashboard.component.ts
│   │   │   │   └── dashboard.routes.ts
│   │   │   │
│   │   │   └── upload/
│   │   │       ├── components/
│   │   │       │   ├── file-dropzone/
│   │   │       │   ├── upload-progress/
│   │   │       │   └── uploaded-files-list/
│   │   │       ├── upload.component.ts
│   │   │       └── upload.routes.ts
│   │   │
│   │   ├── models/                         # Типы и интерфейсы
│   │   │   ├── project.model.ts
│   │   │   ├── finding.model.ts
│   │   │   ├── sarif-report.model.ts
│   │   │   ├── filters.model.ts
│   │   │   ├── pagination.model.ts
│   │   │   ├── api-response.model.ts
│   │   │   └── index.ts
│   │   │
│   │   ├── layout/                         # Layout компоненты
│   │   │   ├── main-layout/
│   │   │   ├── header/
│   │   │   ├── sidebar/
│   │   │   └── footer/
│   │   │
│   │   ├── app.component.ts
│   │   ├── app.config.ts                   # Application config (standalone)
│   │   └── app.routes.ts                   # Routing
│   │
│   ├── environments/
│   │   ├── environment.ts
│   │   └── environment.prod.ts
│   │
│   ├── assets/
│   │   ├── icons/
│   │   └── images/
│   │
│   ├── styles/
│   │   ├── _variables.scss
│   │   ├── _mixins.scss
│   │   └── styles.scss
│   │
│   ├── index.html
│   └── main.ts
│
├── angular.json
├── package.json
├── tsconfig.json
└── tailwind.config.js
```

### 3.2 Core модули и сервисы

#### API Services (HTTP Communication)

```typescript
// core/services/api/finding-api.service.ts

import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { 
  Finding, 
  FindingDetail, 
  FindingsFilter, 
  PaginatedResponse,
  ApiResponse 
} from '@/models';

@Injectable({
  providedIn: 'root'
})
export class FindingApiService {
  private http = inject(HttpClient);
  private readonly apiUrl = '/api/findings';

  getById(id: number): Observable<FindingDetail> {
    return this.http
      .get<ApiResponse<FindingDetail>>(`${this.apiUrl}/${id}`)
      .pipe(map(response => response.data));
  }

  getByProject(
    projectId: number,
    filter?: FindingsFilter,
    page: number = 1,
    pageSize: number = 50
  ): Observable<PaginatedResponse<Finding>> {
    let params = new HttpParams()
      .set('page', page.toString())
      .set('pageSize', pageSize.toString());

    if (filter) {
      if (filter.severities?.length) {
        params = params.set('severities', filter.severities.join(','));
      }
      if (filter.statuses?.length) {
        params = params.set('statuses', filter.statuses.join(','));
      }
      if (filter.searchText) {
        params = params.set('search', filter.searchText);
      }
    }

    return this.http.get<PaginatedResponse<Finding>>(
      `/api/projects/${projectId}/findings`,
      { params }
    );
  }

  updateStatus(id: number, status: FindingStatus): Observable<void> {
    return this.http
      .patch<void>(`${this.apiUrl}/${id}/status`, { status });
  }

  addComment(id: number, text: string): Observable<void> {
    return this.http
      .post<void>(`${this.apiUrl}/${id}/comments`, { text });
  }
}
```

#### State Management (Simple State Service)

```typescript
// core/services/state/finding-state.service.ts

import { Injectable, inject, signal, computed } from '@angular/core';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { BehaviorSubject, Observable, combineLatest } from 'rxjs';
import { map, switchMap, tap } from 'rxjs/operators';
import { FindingApiService } from '../api/finding-api.service';
import { Finding, FindingsFilter } from '@/models';

@Injectable({
  providedIn: 'root'
})
export class FindingStateService {
  private findingApi = inject(FindingApiService);

  // Signals для реактивного состояния
  private _findings = signal<Finding[]>([]);
  private _selectedFinding = signal<Finding | null>(null);
  private _isLoading = signal(false);

  // Public readonly signals
  readonly findings = this._findings.asReadonly();
  readonly selectedFinding = this._selectedFinding.asReadonly();
  readonly isLoading = this._isLoading.asReadonly();

  // Computed values
  readonly criticalFindings = computed(() =>
    this._findings().filter(f => f.severity === 'Critical')
  );

  readonly newFindings = computed(() =>
    this._findings().filter(f => f.status === 'New')
  );

  // Subjects для фильтрации
  private projectId$ = new BehaviorSubject<number | null>(null);
  private filter$ = new BehaviorSubject<FindingsFilter>({});
  private page$ = new BehaviorSubject<number>(1);

  // Observable для автоматической загрузки при изменении фильтров
  readonly findings$ = combineLatest([
    this.projectId$,
    this.filter$,
    this.page$
  ]).pipe(
    switchMap(([projectId, filter, page]) => {
      if (!projectId) return [];
      
      this._isLoading.set(true);
      return this.findingApi.getByProject(projectId, filter, page)
        .pipe(
          tap(response => {
            this._findings.set(response.data);
            this._isLoading.set(false);
          }),
          map(response => response.data)
        );
    }),
    takeUntilDestroyed()
  );

  setProjectId(projectId: number): void {
    this.projectId$.next(projectId);
  }

  setFilter(filter: FindingsFilter): void {
    this.filter$.next(filter);
    this.page$.next(1); // Reset to first page
  }

  setPage(page: number): void {
    this.page$.next(page);
  }

  selectFinding(finding: Finding): void {
    this._selectedFinding.set(finding);
  }

  async updateStatus(id: number, status: FindingStatus): Promise<void> {
    await this.findingApi.updateStatus(id, status).toPromise();
    
    // Обновляем локальное состояние
    this._findings.update(findings =>
      findings.map(f => f.id === id ? { ...f, status } : f)
    );
  }
}
```

#### HTTP Interceptors

```typescript
// core/interceptors/error.interceptor.ts

import { HttpInterceptorFn, HttpErrorResponse } from '@angular/common/http';
import { inject } from '@angular/core';
import { catchError, throwError } from 'rxjs';
import { ToastService } from '../services/toast.service';
import { Router } from '@angular/router';

export const errorInterceptor: HttpInterceptorFn = (req, next) => {
  const toast = inject(ToastService);
  const router = inject(Router);

  return next(req).pipe(
    catchError((error: HttpErrorResponse) => {
      let errorMessage = 'An error occurred';

      if (error.error instanceof ErrorEvent) {
        // Client-side error
        errorMessage = `Error: ${error.error.message}`;
      } else {
        // Server-side error
        switch (error.status) {
          case 400:
            errorMessage = error.error?.error?.message || 'Invalid request';
            break;
          case 404:
            errorMessage = 'Resource not found';
            break;
          case 500:
            errorMessage = 'Internal server error';
            break;
          default:
            errorMessage = `Error ${error.status}: ${error.message}`;
        }
      }

      toast.error(errorMessage);
      
      console.error('HTTP Error:', {
        status: error.status,
        message: errorMessage,
        url: req.url,
        error: error.error
      });

      return throwError(() => error);
    })
  );
};

// core/interceptors/loading.interceptor.ts

import { HttpInterceptorFn } from '@angular/common/http';
import { inject } from '@angular/core';
import { finalize } from 'rxjs/operators';
import { LoadingService } from '../services/loading.service';

export const loadingInterceptor: HttpInterceptorFn = (req, next) => {
  const loadingService = inject(LoadingService);
  
  // Показываем loader только для не-GET запросов
  if (req.method !== 'GET') {
    loadingService.show();
  }

  return next(req).pipe(
    finalize(() => loadingService.hide())
  );
};
```

### 3.3 Feature Modules

#### Findings Module

```typescript
// features/findings/components/findings-table/findings-table.component.ts

import { Component, Input, Output, EventEmitter, OnInit, inject, ChangeDetectionStrategy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatTableModule } from '@angular/material/table';
import { MatSortModule } from '@angular/material/sort';
import { MatPaginatorModule } from '@angular/material/paginator';
import { CdkVirtualScrollViewport, ScrollingModule } from '@angular/cdk/scrolling';
import { Finding, FindingStatus } from '@/models';
import { SeverityBadgeComponent } from '@/shared/components/severity-badge';
import { StatusBadgeComponent } from '@/shared/components/status-badge';

@Component({
  selector: 'app-findings-table',
  standalone: true,
  imports: [
    CommonModule,
    MatTableModule,
    MatSortModule,
    MatPaginatorModule,
    ScrollingModule,
    SeverityBadgeComponent,
    StatusBadgeComponent
  ],
  templateUrl: './findings-table.component.html',
  styleUrls: ['./findings-table.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class FindingsTableComponent {
  @Input({ required: true }) findings: Finding[] = [];
  @Input() isLoading = false;
  
  @Output() selectFinding = new EventEmitter<Finding>();
  @Output() changeStatus = new EventEmitter<{ id: number; status: FindingStatus }>();

  displayedColumns: string[] = [
    'severity',
    'ruleId',
    'message',
    'filePath',
    'tool',
    'status',
    'createdAt',
    'actions'
  ];

  selectedId: number | null = null;

  onSelectFinding(finding: Finding): void {
    this.selectedId = finding.id;
    this.selectFinding.emit(finding);
  }

  onChangeStatus(id: number, status: FindingStatus): void {
    this.changeStatus.emit({ id, status });
  }

  trackByFindingId(index: number, finding: Finding): number {
    return finding.id;
  }

  getSeverityClass(severity: string): string {
    return `severity-${severity.toLowerCase()}`;
  }
}
```

```html
<!-- findings-table.component.html -->

<div class="findings-table-container">
  <div *ngIf="isLoading" class="loading-overlay">
    <mat-spinner></mat-spinner>
  </div>

  <table mat-table 
         [dataSource]="findings" 
         matSort 
         class="findings-table"
         [trackBy]="trackByFindingId">

    <!-- Severity Column -->
    <ng-container matColumnDef="severity">
      <th mat-header-cell *matHeaderCellDef mat-sort-header>Severity</th>
      <td mat-cell *matCellDef="let finding">
        <app-severity-badge [severity]="finding.severity"></app-severity-badge>
      </td>
    </ng-container>

    <!-- Rule ID Column -->
    <ng-container matColumnDef="ruleId">
      <th mat-header-cell *matHeaderCellDef mat-sort-header>Rule</th>
      <td mat-cell *matCellDef="let finding">
        <span class="rule-id">{{ finding.ruleId }}</span>
      </td>
    </ng-container>

    <!-- Message Column -->
    <ng-container matColumnDef="message">
      <th mat-header-cell *matHeaderCellDef>Message</th>
      <td mat-cell *matCellDef="let finding" class="message-cell">
        <span class="message-text" [title]="finding.message">
          {{ finding.message | slice:0:100 }}
          <span *ngIf="finding.message.length > 100">...</span>
        </span>
      </td>
    </ng-container>

    <!-- File Path Column -->
    <ng-container matColumnDef="filePath">
      <th mat-header-cell *matHeaderCellDef mat-sort-header>File</th>
      <td mat-cell *matCellDef="let finding">
        <code *ngIf="finding.filePath" class="file-path">
          {{ finding.filePath }}
          <span *ngIf="finding.startLine" class="line-number">
            :{{ finding.startLine }}
          </span>
        </code>
      </td>
    </ng-container>

    <!-- Tool Column -->
    <ng-container matColumnDef="tool">
      <th mat-header-cell *matHeaderCellDef mat-sort-header>Tool</th>
      <td mat-cell *matCellDef="let finding">
        {{ finding.report?.toolName }}
      </td>
    </ng-container>

    <!-- Status Column -->
    <ng-container matColumnDef="status">
      <th mat-header-cell *matHeaderCellDef mat-sort-header>Status</th>
      <td mat-cell *matCellDef="let finding">
        <app-status-badge 
          [status]="finding.status"
          [clickable]="true"
          (statusChange)="onChangeStatus(finding.id, $event)">
        </app-status-badge>
      </td>
    </ng-container>

    <!-- Created At Column -->
    <ng-container matColumnDef="createdAt">
      <th mat-header-cell *matHeaderCellDef mat-sort-header>Created</th>
      <td mat-cell *matCellDef="let finding">
        {{ finding.createdAt | date:'short' }}
      </td>
    </ng-container>

    <!-- Actions Column -->
    <ng-container matColumnDef="actions">
      <th mat-header-cell *matHeaderCellDef>Actions</th>
      <td mat-cell *matCellDef="let finding">
        <button mat-icon-button 
                (click)="onSelectFinding(finding)"
                [class.selected]="selectedId === finding.id">
          <mat-icon>visibility</mat-icon>
        </button>
      </td>
    </ng-container>

    <tr mat-header-row *matHeaderRowDef="displayedColumns"></tr>
    <tr mat-row 
        *matRowDef="let row; columns: displayedColumns;"
        [class.selected-row]="selectedId === row.id"
        (click)="onSelectFinding(row)">
    </tr>

    <!-- No data row -->
    <tr class="mat-row" *matNoDataRow>
      <td class="mat-cell no-data-cell" [attr.colspan]="displayedColumns.length">
        No findings found
      </td>
    </tr>
  </table>

  <mat-paginator 
    [length]="findings.length"
    [pageSize]="50"
    [pageSizeOptions]="[25, 50, 100, 200]">
  </mat-paginator>
</div>
```

### 3.4 Routing Configuration

```typescript
// app.routes.ts

import { Routes } from '@angular/router';

export const routes: Routes = [
  {
    path: '',
    redirectTo: '/dashboard',
    pathMatch: 'full'
  },
  {
    path: 'dashboard',
    loadComponent: () => import('./features/dashboard/dashboard.component')
      .then(m => m.DashboardComponent),
    title: 'Dashboard - SARIF Manager'
  },
  {
    path: 'projects',
    loadComponent: () => import('./features/projects/projects.component')
      .then(m => m.ProjectsComponent),
    title: 'Projects - SARIF Manager',
    children: [
      {
        path: ':id/findings',
        loadComponent: () => import('./features/findings/findings.component')
          .then(m => m.FindingsComponent),
        title: 'Findings - SARIF Manager'
      }
    ]
  },
  {
    path: 'upload',
    loadComponent: () => import('./features/upload/upload.component')
      .then(m => m.UploadComponent),
    title: 'Upload SARIF - SARIF Manager'
  },
  {
    path: '**',
    redirectTo: '/dashboard'
  }
];
```

---

## 4. Data Flow Architecture

### 4.1 Upload SARIF Flow

```
┌─────────────┐
│   Angular   │
│  Component  │
└──────┬──────┘
       │ 1. User uploads SARIF file(s)
       │
┌──────▼──────┐
│   Upload    │
│  Service    │
└──────┬──────┘
       │ 2. HTTP POST /api/projects/{id}/upload
       │
┌──────▼──────┐
│   Upload    │
│ Controller  │
└──────┬──────┘
       │ 3. Validate file size/format
       │
┌──────▼────────────┐
│ File Storage      │
│ Service           │
└──────┬────────────┘
       │ 4. Save file to /uploads/{projectId}/{reportId}/
       │
┌──────▼────────────┐
│ SARIF Parsing     │
│ Service           │
└──────┬────────────┘
       │ 5. Parse SARIF JSON
       │ 6. Extract findings
       │
┌──────▼────────────┐
│ Finding Service   │
└──────┬────────────┘
       │ 7. Normalize severity
       │ 8. Create Finding entities
       │
┌──────▼────────────┐
│ Finding Repository│
└──────┬────────────┘
       │ 9. Bulk insert findings
       │
┌──────▼────────────┐
│   SQLite DB       │
└───────────────────┘
```

### 4.2 Findings Display Flow

```
┌─────────────┐
│   Angular   │
│  Component  │
└──────┬──────┘
       │ 1. ngOnInit / Filter change
       │
┌──────▼────────────┐
│ Finding State     │
│ Service (Signal)  │
└──────┬────────────┘
       │ 2. Get findings with filters
       │
┌──────▼────────────┐
│ Finding API       │
│ Service           │
└──────┬────────────┘
       │ 3. HTTP GET /api/projects/{id}/findings?filters...
       │
┌──────▼────────────┐
│ Findings          │
│ Controller        │
└──────┬────────────┘
       │ 4. Call service
       │
┌──────▼────────────┐
│ Finding Service   │
└──────┬────────────┘
       │ 5. Build query with filters
       │
┌──────▼────────────┐
│ Finding Repository│
└──────┬────────────┘
       │ 6. EF Core query with Include()
       │
┌──────▼────────────┐
│   SQLite DB       │
└──────┬────────────┘
       │ 7. Return results
       │
┌──────▼────────────┐
│ AutoMapper        │
└──────┬────────────┘
       │ 8. Map Entity → DTO
       │
┌──────▼────────────┐
│ Angular Component │
│ (Table display)   │
└───────────────────┘
```

### 4.3 Status Update Flow

```
┌─────────────┐
│   User      │
│  Action     │
└──────┬──────┘
       │ 1. Click status badge
       │
┌──────▼────────────┐
│ Status Badge      │
│ Component         │
└──────┬────────────┘
       │ 2. Emit statusChange event
       │
┌──────▼────────────┐
│ Findings Table    │
│ Component         │
└──────┬────────────┘
       │ 3. Call stateService.updateStatus()
       │
┌──────▼────────────┐
│ Finding State     │
│ Service           │
└──────┬────────────┘
       │ 4. HTTP PATCH /api/findings/{id}/status
       │
┌──────▼────────────┐
│ Findings          │
│ Controller        │
└──────┬────────────┘
       │ 5. Call service
       │
┌──────▼────────────┐
│ Finding Service   │
└──────┬────────────┘
       │ 6. Get finding by ID
       │ 7. Call finding.UpdateStatus() (domain logic)
       │
┌──────▼────────────┐
│ Finding Entity    │
│ (Domain Model)    │
└──────┬────────────┘
       │ 8. Validate status transition
       │ 9. Update status + timestamp
       │
┌──────▼────────────┐
│ Finding Repository│
└──────┬────────────┘
       │ 10. Save to DB
       │
┌──────▼────────────┐
│   SQLite DB       │
└──────┬────────────┘
       │ 11. Success response
       │
┌──────▼────────────┐
│ Finding State     │
│ Service           │
└──────┬────────────┘
       │ 12. Update local signal state
       │
┌──────▼────────────┐
│ UI Updates        │
│ (OnPush + Signal) │
└───────────────────┘
```

---

## 5. Database Schema

```sql
-- Projects table
CREATE TABLE Projects (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL,
    Description TEXT,
    CreatedAt TEXT NOT NULL,
    UpdatedAt TEXT NOT NULL
);

CREATE INDEX IX_Projects_Name ON Projects(Name);

-- SarifReports table
CREATE TABLE SarifReports (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    ProjectId INTEGER NOT NULL,
    ToolName TEXT NOT NULL,
    ToolVersion TEXT NOT NULL,
    FileName TEXT NOT NULL,
    FilePath TEXT NOT NULL,
    FileSizeBytes INTEGER NOT NULL,
    UploadedAt TEXT NOT NULL,
    
    FOREIGN KEY (ProjectId) REFERENCES Projects(Id) ON DELETE CASCADE
);

CREATE INDEX IX_SarifReports_ProjectId ON SarifReports(ProjectId);
CREATE INDEX IX_SarifReports_ToolName ON SarifReports(ToolName);

-- Findings table
CREATE TABLE Findings (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    ProjectId INTEGER NOT NULL,
    ReportId INTEGER NOT NULL,
    
    RuleId TEXT NOT NULL,
    Message TEXT NOT NULL,
    FilePath TEXT,
    StartLine INTEGER,
    StartColumn INTEGER,
    Level TEXT NOT NULL,
    
    Severity TEXT NOT NULL,  -- Critical, High, Medium, Low, Info
    Status TEXT NOT NULL,    -- New, Confirmed, FalsePositive, Fixed
    
    CreatedAt TEXT NOT NULL,
    UpdatedAt TEXT NOT NULL,
    
    RawSarifJson TEXT,
    
    FOREIGN KEY (ProjectId) REFERENCES Projects(Id) ON DELETE CASCADE,
    FOREIGN KEY (ReportId) REFERENCES SarifReports(Id) ON DELETE CASCADE
);

CREATE INDEX IX_Findings_ProjectId ON Findings(ProjectId);
CREATE INDEX IX_Findings_ReportId ON Findings(ReportId);
CREATE INDEX IX_Findings_Severity ON Findings(Severity);
CREATE INDEX IX_Findings_Status ON Findings(Status);
CREATE INDEX IX_Findings_RuleId ON Findings(RuleId);

-- FindingComments table
CREATE TABLE FindingComments (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    FindingId INTEGER NOT NULL,
    Text TEXT NOT NULL,
    CreatedAt TEXT NOT NULL,
    
    FOREIGN KEY (FindingId) REFERENCES Findings(Id) ON DELETE CASCADE
);

CREATE INDEX IX_FindingComments_FindingId ON FindingComments(FindingId);
```

---

## 6. Key Architectural Decisions (ADRs)

### ADR-001: Clean Architecture для Backend

**Решение:** Использовать Clean Architecture с разделением на 4 слоя

**Обоснование:**
- Четкое разделение ответственностей
- Независимость бизнес-логики от технологий
- Упрощение тестирования
- Возможность замены Infrastructure (например, SQLite → PostgreSQL)

**Последствия:**
- Больше файлов и структуры
- Требуется больше boilerplate кода
- Easier maintenance и расширение функциональности

### ADR-002: Angular Signals для State Management

**Решение:** Использовать Angular Signals вместо сложных state management решений (NgRx)

**Обоснование:**
- PoC проект не требует сложного state management
- Signals — нативное решение Angular 17+
- Меньше boilerplate по сравнению с NgRx
- Отличная производительность (fine-grained reactivity)

**Последствия:**
- Проще в изучении и поддержке
- Для масштабирования в будущем может потребоваться NgRx
- Локальный state в services, а не глобальный store

### ADR-003: Standalone Components в Angular

**Решение:** Использовать standalone компоненты вместо NgModules

**Обоснование:**
- Современный подход Angular 17+
- Упрощение структуры (меньше модулей)
- Лучше tree-shaking
- Проще lazy loading

**Последствия:**
- Некоторые библиотеки могут не поддерживать (редко)
- Необходимо явно указывать imports в каждом компоненте

### ADR-004: SQLite для PoC

**Решение:** SQLite вместо PostgreSQL/MySQL

**Обоснование:**
- PoC не требует масштабируемости
- Zero-configuration (нет отдельного DB server)
- Простота развертывания
- Достаточная производительность для тестирования

**Последствия:**
- Ограничения по concurrency (write lock)
- Для production нужна миграция на PostgreSQL/SQL Server
- Легкая миграция благодаря EF Core

### ADR-005: AutoMapper для DTO маппинга

**Решение:** Использовать AutoMapper вместо ручного маппинга

**Обоснование:**
- Меньше boilerplate кода
- Конвенции по умолчанию работают для простых случаев
- Centralized конфигурация маппинга

**Последствия:**
- Немного магии (неявное поведение)
- Performance overhead (незначительный)
- Необходимо настроить profiles для сложных маппингов

---

## 7. Performance Considerations

### 7.1 Backend Optimizations

1. **Database Queries:**
   - `AsNoTracking()` для read-only операций
   - Eager loading с `Include()` для избежания N+1
   - Индексы на часто фильтруемые колонки (Severity, Status, RuleId)
   - Пагинация по умолчанию (50 элементов)

2. **File Processing:**
   - Background job для парсинга больших SARIF файлов (> 10MB)
   - Streaming парсинг JSON для экономии памяти
   - Ограничение размера файла (50MB)

3. **Caching:**
   - In-memory cache для редко меняющихся данных (project list)
   - Response caching для analytics endpoints

### 7.2 Frontend Optimizations

1. **Change Detection:**
   - OnPush strategy для всех компонентов
   - Signals для fine-grained reactivity

2. **Rendering:**
   - Virtual scrolling для таблиц > 100 элементов (CDK Virtual Scroll)
   - TrackBy functions для *ngFor
   - Lazy loading routes

3. **Network:**
   - Debounce на search inputs (300ms)
   - HTTP request caching для справочных данных
   - Pagination вместо загрузки всех данных

---

## 8. Security Architecture

### 8.1 PoC Limitations
- ⚠️ No authentication/authorization
- ⚠️ Single user model
- ⚠️ CORS открыт для localhost

### 8.2 Security Measures

1. **Input Validation:**
   - FluentValidation на backend
   - Reactive Forms validation на frontend
   - File size/type validation для uploads

2. **SQL Injection Protection:**
   - EF Core параметризованные запросы
   - No raw SQL queries

3. **XSS Protection:**
   - Angular auto-escaping в templates
   - Sanitization для user-generated content

4. **Rate Limiting:**
   - Request throttling для upload API
   - Max file size enforcement

5. **Error Handling:**
   - No sensitive info в error messages
   - Structured logging без credentials

---

## 9. Deployment Architecture (Fullstack Publish)

### Монорепозиторий: структура и сборка

repo-root/
├── frontend/   # Angular 17+
├── backend/    # ASP.NET Core Web API (.NET 8, wwwroot статичные)

### Инструкция по деплою (publish)

1. Перейдите в папку frontend и соберите Angular:
   ```bash
   cd frontend
   npm install
   npm run build -- --output-path=../backend/wwwroot --configuration production
   ```
   Все статики Angular будут в backend/wwwroot

2. Сборка и запуск backend:
   ```bash
   cd ../backend
   dotnet build
   dotnet run   # или dotnet publish и запуск собранного
   ```

3. Теперь SPA и API доступны на одном адресе/сервере.

- Для крупного деплоя: используйте dotnet publish (Release), можно завернуть в Docker или развернуть на любом VPS или Windows/IIS.

### Пример Startup (.NET 8+)

```csharp
app.UseDefaultFiles();
app.UseStaticFiles(); // (отдаёт SPA)
app.UseRouting();
app.MapControllers();
app.MapFallbackToFile("index.html"); // SPA fallback (Angular роутинг)
```

### Почему не Netlify/Vercel/etc только для фронта?
- Fullstack publish удобнее: нет CORS, нет необходимости раздельного деплоя и настройки внешнего API.
- Любой хостинг с .NET Core (Linux/Windows/IP виртуалка, облако, Heroku, Azure и др.)

## 10. Testing Strategy

### 10.1 Backend Testing

```
├── Unit Tests
│   ├── Services (mock dependencies)
│   ├── Domain logic (entities, value objects)
│   └── Validators
│
├── Integration Tests
│   ├── Repositories (in-memory DB)
│   ├── SARIF parsing (sample files)
│   └── API endpoints (WebApplicationFactory)
│
└── E2E Tests (optional)
    └── Full flow tests
```

### 10.2 Frontend Testing

```
├── Unit Tests
│   ├── Services (mock HttpClient)
│   ├── Pipes
│   └── Utilities
│
├── Component Tests
│   ├── Isolated component logic
│   ├── Template rendering
│   └── User interactions
│
└── E2E Tests (Playwright/Cypress)
    ├── Upload flow
    ├── Filter/search
    └── Status management
```

---

**Архитектурный документ v1.0**  
*Последнее обновление: October 2025*

