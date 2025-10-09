# 🚀 Быстрый старт - SARIF Parser

## 📦 Что создано

Парсер для отчетов SARIF 2.1.0 с полным набором функций для анализа результатов сканирования безопасности.

### Файлы

1. **`sarif_parser.py`** - основной модуль парсера (готов к использованию)
2. **`example_usage.py`** - 8 примеров использования
3. **`test_parser.py`** - скрипт для тестирования на ваших файлах
4. **`README_SARIF_PARSER.md`** - полная документация
5. **`QUICKSTART.md`** - этот файл

## ⚡ Быстрый запуск

### Вариант 1: Тестирование на ваших файлах

```bash
python test_parser.py
```

Этот скрипт автоматически:
- Найдет ваши SARIF файлы
- Распарсит их
- Покажет статистику
- Выведет топ уязвимостей

### Вариант 2: Базовое использование

```python
from sarif_parser import SarifParser, print_report_summary

# Парсинг файла
report = SarifParser.parse_file("path/to/your/report.sarif")

# Краткая информация
print_report_summary(report)

# Или работа с данными
print(f"Всего находок: {len(report.findings)}")
print(f"Инструмент: {report.tool.name}")

# Статистика
stats = report.get_statistics()
print(f"Ошибок: {stats['by_severity']['error']}")
```

### Вариант 3: Запуск примеров

```bash
python example_usage.py
```

Запустит все 8 примеров использования:
1. Базовый парсинг
2. Получение статистики
3. Фильтрация по серьезности
4. Фильтрация по типу уязвимости
5. Работа с правилами
6. Экспорт в CSV
7. Сравнение отчетов
8. Генерация HTML

## 📊 Основные возможности

### 1. Парсинг любых SARIF файлов

```python
from sarif_parser import SarifParser

report = SarifParser.parse_file("report.sarif")
```

### 2. Статистика

```python
stats = report.get_statistics()
# Возвращает: total_findings, by_severity, by_rule
```

### 3. Фильтрация

```python
from sarif_parser import SeverityLevel

# Только критические
critical = [f for f in report.findings if f.level == SeverityLevel.ERROR]

# По типу уязвимости
sqli = [f for f in report.findings if f.rule_id == "sqli"]
```

### 4. Экспорт

```python
# В CSV
import csv
with open("report.csv", 'w') as f:
    writer = csv.writer(f)
    for finding in report.findings:
        for location in finding.locations:
            writer.writerow([
                finding.rule_name,
                finding.level.value,
                location.file_path
            ])
```

## 🎯 Примеры для ваших файлов

### Анализ PT BlackBox (bbs1_ru.sarif, bbs2_ru.sarif)

```python
from sarif_parser import SarifParser

# Загружаем отчет
report = SarifParser.parse_file(r"C:\Users\ssinyakov\Downloads\bbs1_ru.sarif")

# Ищем SQL Injection
sqli = [f for f in report.findings if f.rule_id == "sqli"]
print(f"SQL Injection: {len(sqli)}")

# Ищем XSS
xss = [f for f in report.findings if f.rule_id == "xss"]
print(f"XSS: {len(xss)}")

# Файлы с уязвимостями
files = set()
for finding in report.findings:
    for loc in finding.locations:
        files.add(loc.file_path)
print(f"Уязвимых файлов: {len(files)}")
```

### Анализ PT Application Inspector (AI3.sarif)

```python
from sarif_parser import SarifParser, SeverityLevel

report = SarifParser.parse_file(r"C:\Users\ssinyakov\Downloads\AI3.sarif")

# Критические уязвимости
critical = [f for f in report.findings if f.level == SeverityLevel.ERROR]
print(f"Критических: {len(critical)}")

# Топ-5 типов уязвимостей
stats = report.get_statistics()
top5 = sorted(
    stats['by_rule'].items(),
    key=lambda x: x[1]['count'],
    reverse=True
)[:5]

for rule_id, info in top5:
    print(f"{info['name']}: {info['count']}")
```

## 🛠️ Структура данных

### Основные классы

```python
# Отчет
report.tool          # ToolInfo - информация об инструменте
report.rules         # Dict[str, Rule] - правила
report.findings      # List[Finding] - находки

# Находка
finding.rule_id      # str - ID правила
finding.rule_name    # str - название
finding.level        # SeverityLevel - уровень
finding.locations    # List[Location] - где найдено

# Локация
location.file_path   # str - путь к файлу
location.start_line  # int - строка начала
location.snippet     # str - фрагмент кода
```

## 📈 Интеграция в CI/CD

```python
from sarif_parser import SarifParser, SeverityLevel
import sys

report = SarifParser.parse_file("report.sarif")

# Подсчет критических
critical = sum(1 for f in report.findings if f.level == SeverityLevel.ERROR)

if critical > 0:
    print(f"❌ Найдено {critical} критических уязвимостей!")
    sys.exit(1)
else:
    print("✅ Критических уязвимостей не обнаружено")
    sys.exit(0)
```

## 🔧 Требования

- Python 3.7+
- Нет внешних зависимостей!

## 📝 Структура SARIF

Парсер поддерживает:
- ✅ SARIF 2.1.0 (стандарт)
- ✅ PT BlackBox отчеты
- ✅ PT Application Inspector отчеты
- ✅ Любые SARIF-совместимые инструменты

## 🎨 Вывод

Парсер предоставляет готовые функции для вывода:

```python
from sarif_parser import print_report_summary, print_detailed_findings

# Краткая сводка с графиками
print_report_summary(report)

# Детальный список находок
print_detailed_findings(report, max_findings=20)
```

## 💡 Полезные рецепты

### Найти все файлы с критическими уязвимостями

```python
critical_files = set()
for f in report.findings:
    if f.level == SeverityLevel.ERROR:
        for loc in f.locations:
            critical_files.add(loc.file_path)

print(f"Критичных файлов: {len(critical_files)}")
for file in sorted(critical_files):
    print(f"  - {file}")
```

### Группировка по файлам

```python
from collections import defaultdict

by_file = defaultdict(list)
for finding in report.findings:
    for location in finding.locations:
        by_file[location.file_path].append(finding)

# Топ-10 файлов
top_files = sorted(by_file.items(), key=lambda x: len(x[1]), reverse=True)[:10]
for file, findings in top_files:
    print(f"{file}: {len(findings)} проблем")
```

### Экспорт в JSON

```python
import json

data = {
    'tool': report.tool.name,
    'total': len(report.findings),
    'critical': sum(1 for f in report.findings if f.level == SeverityLevel.ERROR),
    'findings': [
        {
            'rule': f.rule_name,
            'severity': f.level.value,
            'files': [loc.file_path for loc in f.locations]
        }
        for f in report.findings
    ]
}

with open('summary.json', 'w') as f:
    json.dump(data, f, indent=2)
```

## 📚 Дополнительная информация

- Полная документация: `README_SARIF_PARSER.md`
- Примеры: `example_usage.py`
- Тесты: `test_parser.py`

## 🆘 Помощь

Если что-то не работает:

1. Проверьте, что файл - валидный JSON:
   ```python
   import json
   with open("report.sarif") as f:
       data = json.load(f)  # Должно работать без ошибок
   ```

2. Проверьте версию SARIF:
   ```python
   print(data.get("version"))  # Должно быть "2.1.0"
   ```

3. Запустите тестовый скрипт:
   ```bash
   python test_parser.py
   ```

## ✨ Готово к использованию!

Парсер полностью готов. Начните с запуска:

```bash
python test_parser.py
```

Или сразу используйте в своем коде! 🚀

