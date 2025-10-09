# SARIF Parser

Парсер для отчетов в формате SARIF 2.1.0 (Static Analysis Results Interchange Format).

## 📋 Описание

SARIF Parser - это Python библиотека для парсинга и анализа отчетов о безопасности в формате SARIF. Поддерживает отчеты от различных инструментов анализа кода.

### Поддерживаемые инструменты

- ✅ PT BlackBox (Positive Technologies)
- ✅ PT Application Inspector (Positive Technologies)
- ✅ Любые другие инструменты, использующие стандарт SARIF 2.1.0

## 🚀 Быстрый старт

### Установка

Парсер не требует дополнительных зависимостей, использует только стандартную библиотеку Python.

```bash
# Скопируйте файл sarif_parser.py в ваш проект
```

### Базовое использование

```python
from sarif_parser import SarifParser, print_report_summary

# Парсинг SARIF файла
report = SarifParser.parse_file("report.sarif")

# Вывод краткой информации
print_report_summary(report)

# Доступ к данным
print(f"Инструмент: {report.tool.name}")
print(f"Всего находок: {len(report.findings)}")
print(f"Всего правил: {len(report.rules)}")
```

## 📊 Основные возможности

### 1. Парсинг SARIF файлов

```python
from sarif_parser import SarifParser

# Из файла
report = SarifParser.parse_file("report.sarif")

# Из словаря (если уже загрузили JSON)
import json
with open("report.sarif") as f:
    data = json.load(f)
report = SarifParser.parse_dict(data)
```

### 2. Получение статистики

```python
stats = report.get_statistics()

print(f"Всего находок: {stats['total_findings']}")
print(f"Ошибки: {stats['by_severity']['error']}")
print(f"Предупреждения: {stats['by_severity']['warning']}")
print(f"Заметки: {stats['by_severity']['note']}")

# Статистика по правилам
for rule_id, info in stats['by_rule'].items():
    print(f"{info['name']}: {info['count']} находок")
```

### 3. Фильтрация находок

```python
from sarif_parser import SeverityLevel

# По уровню серьезности
critical = [f for f in report.findings if f.level == SeverityLevel.ERROR]
warnings = [f for f in report.findings if f.level == SeverityLevel.WARNING]

# По типу уязвимости
sql_injections = [f for f in report.findings if f.rule_id == "sqli"]

# По файлу
findings_in_file = [
    f for f in report.findings 
    if any("auth.js" in loc.file_path for loc in f.locations)
]
```

### 4. Работа с локациями

```python
for finding in report.findings:
    print(f"Уязвимость: {finding.rule_name}")
    
    for location in finding.locations:
        print(f"  Файл: {location.file_path}")
        if location.start_line:
            print(f"  Строка: {location.start_line}")
        if location.snippet:
            print(f"  Код: {location.snippet}")
```

### 5. Экспорт в CSV

```python
import csv

with open("report.csv", 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['Rule', 'Severity', 'File', 'Line'])
    writer.writeheader()
    
    for finding in report.findings:
        for location in finding.locations:
            writer.writerow({
                'Rule': finding.rule_name,
                'Severity': finding.level.value,
                'File': location.file_path,
                'Line': location.start_line or ''
            })
```

### 6. Генерация HTML отчета

```python
from sarif_parser import print_report_summary, print_detailed_findings

# Краткий отчет
print_report_summary(report)

# Детальный отчет (первые 20 находок)
print_detailed_findings(report, max_findings=20)
```

## 📚 Структура данных

### SarifReport

Главный объект отчета:

```python
class SarifReport:
    tool: ToolInfo              # Информация об инструменте
    rules: Dict[str, Rule]      # Словарь правил (по ID)
    findings: List[Finding]     # Список находок
    sarif_version: str          # Версия SARIF
```

### ToolInfo

Информация об инструменте сканирования:

```python
class ToolInfo:
    name: str                   # Название инструмента
    version: Optional[str]      # Версия
    organization: Optional[str] # Организация
    information_uri: Optional[str] # URL с информацией
```

### Rule

Правило (тип уязвимости):

```python
class Rule:
    id: str                     # ID правила
    name: str                   # Название
    description_text: str       # Описание (HTML)
    description_markdown: str   # Описание (Markdown)
    level: SeverityLevel        # Уровень серьезности
    enabled: bool               # Включено ли правило
```

### Finding

Находка (конкретная уязвимость):

```python
class Finding:
    rule_id: str                # ID правила
    rule_name: str              # Название правила
    message: str                # Сообщение
    level: SeverityLevel        # Уровень серьезности
    locations: List[Location]   # Список локаций
```

### Location

Локация находки в коде:

```python
class Location:
    file_path: str              # Путь к файлу
    snippet: str                # Фрагмент кода
    start_line: int             # Начальная строка
    end_line: int               # Конечная строка
    start_column: int           # Начальная колонка
    end_column: int             # Конечная колонка
```

### SeverityLevel

Уровни серьезности:

```python
class SeverityLevel(Enum):
    ERROR = "error"      # 🔴 Критическая ошибка
    WARNING = "warning"  # 🟡 Предупреждение
    NOTE = "note"        # 🔵 Заметка
    NONE = "none"        # ⚪ Не определено
```

## 💡 Примеры использования

### Пример 1: Анализ отчета PT BlackBox

```python
from sarif_parser import SarifParser, SeverityLevel

# Загружаем отчет
report = SarifParser.parse_file("blackbox_report.sarif")

# Находим все SQL Injection
sqli = [f for f in report.findings if "sql" in f.rule_id.lower()]
print(f"Найдено SQL Injection: {len(sqli)}")

# Находим все критические уязвимости
critical = [f for f in report.findings if f.level == SeverityLevel.ERROR]
print(f"Критических уязвимостей: {len(critical)}")

# Список уникальных файлов с уязвимостями
vulnerable_files = set()
for finding in report.findings:
    for location in finding.locations:
        vulnerable_files.add(location.file_path)

print(f"Уязвимых файлов: {len(vulnerable_files)}")
```

### Пример 2: Сравнение двух отчетов

```python
from sarif_parser import SarifParser

# Загружаем два отчета
report_old = SarifParser.parse_file("report_old.sarif")
report_new = SarifParser.parse_file("report_new.sarif")

# Сравниваем количество находок
old_count = len(report_old.findings)
new_count = len(report_new.findings)
diff = new_count - old_count

if diff > 0:
    print(f"❌ Появилось {diff} новых находок!")
elif diff < 0:
    print(f"✅ Исправлено {abs(diff)} находок!")
else:
    print("➖ Количество находок не изменилось")

# Сравниваем типы уязвимостей
old_rules = set(f.rule_id for f in report_old.findings)
new_rules = set(f.rule_id for f in report_new.findings)

new_types = new_rules - old_rules
if new_types:
    print(f"⚠️  Новые типы уязвимостей: {', '.join(new_types)}")
```

### Пример 3: Генерация отчета для CI/CD

```python
from sarif_parser import SarifParser, SeverityLevel
import sys

report = SarifParser.parse_file("report.sarif")

# Подсчитываем критические уязвимости
critical_count = sum(
    1 for f in report.findings 
    if f.level == SeverityLevel.ERROR
)

print(f"Критических уязвимостей: {critical_count}")

# Провал сборки при наличии критических уязвимостей
if critical_count > 0:
    print("❌ Сборка провалена из-за критических уязвимостей!")
    sys.exit(1)
else:
    print("✅ Критических уязвимостей не обнаружено")
    sys.exit(0)
```

### Пример 4: Группировка по файлам

```python
from collections import defaultdict
from sarif_parser import SarifParser

report = SarifParser.parse_file("report.sarif")

# Группируем находки по файлам
by_file = defaultdict(list)
for finding in report.findings:
    for location in finding.locations:
        by_file[location.file_path].append(finding)

# Топ-10 файлов с наибольшим количеством уязвимостей
sorted_files = sorted(
    by_file.items(), 
    key=lambda x: len(x[1]), 
    reverse=True
)

print("Топ-10 уязвимых файлов:")
for i, (file_path, findings) in enumerate(sorted_files[:10], 1):
    print(f"{i:2}. [{len(findings):3}] {file_path}")
```

## 🛠️ Использование из командной строки

```bash
# Базовый анализ
python sarif_parser.py report.sarif

# Запуск всех примеров
python example_usage.py
```

## 📖 Стандарт SARIF

SARIF (Static Analysis Results Interchange Format) - это стандартный формат для обмена результатами статического анализа кода.

- **Спецификация**: [OASIS SARIF 2.1.0](https://docs.oasis-open.org/sarif/sarif/v2.1.0/sarif-v2.1.0.html)
- **JSON Schema**: http://json.schemastore.org/sarif-2.1.0.json

## 🔧 Требования

- Python 3.7+
- Стандартная библиотека Python (нет внешних зависимостей)

## 📝 Лицензия

Этот парсер предоставляется "как есть" для использования в проектах анализа безопасности.

## 🤝 Поддержка

Если у вас возникли вопросы или предложения по улучшению парсера:

1. Проверьте, что ваш SARIF файл соответствует стандарту 2.1.0
2. Убедитесь, что файл содержит валидный JSON
3. Проверьте примеры использования в `example_usage.py`

## 📦 Файлы проекта

- `sarif_parser.py` - основной модуль парсера
- `example_usage.py` - примеры использования
- `README_SARIF_PARSER.md` - эта документация

## 🎯 Дорожная карта

Возможные улучшения:

- [ ] Поддержка множественных запусков (runs) в одном файле
- [ ] Экспорт в другие форматы (JSON, XML, Excel)
- [ ] Визуализация данных (графики, диаграммы)
- [ ] Интеграция с системами управления задачами (Jira, GitLab)
- [ ] CLI с расширенными возможностями фильтрации
- [ ] Веб-интерфейс для просмотра отчетов

## 🔍 Отладка

При возникновении проблем:

```python
from sarif_parser import SarifParser
import json

# Проверка структуры файла
with open("report.sarif") as f:
    data = json.load(f)
    print(f"SARIF версия: {data.get('version')}")
    print(f"Количество запусков: {len(data.get('runs', []))}")
    
# Парсинг с отладочной информацией
try:
    report = SarifParser.parse_file("report.sarif")
    print("✅ Парсинг успешен")
except Exception as e:
    print(f"❌ Ошибка: {e}")
    import traceback
    traceback.print_exc()
```

