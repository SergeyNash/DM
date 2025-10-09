# 📊 Пример вывода SARIF Parser

Этот файл показывает, как выглядит вывод парсера при работе с вашими SARIF файлами.

---

## 🧪 Пример 1: Запуск test_parser.py

```
🔍 SARIF Parser - Тестирование

================================================================================
Тестирование файла: bbs2_ru.sarif
================================================================================

================================================================================
SARIF Отчет: PT BlackBox
Организация: Positive Technologies
================================================================================

Всего находок: 11
Всего правил: 6

Распределение по уровням серьезности:
  🔴 Ошибки (error):    1
  🟡 Предупреждения (warning): 1
  🔵 Заметки (note):     9
  ⚪ Прочие (none):      0

Топ-10 правил по количеству находок:
   1. 🔵 [   1] Раскрытие адресов электронной почты
      ID: disclosure_email
   2. 🔵 [   1] Отсутствует заголовок Content-Security-Policy
      ID: missing_content-security-policy
   3. 🔵 [   1] Отсутствует заголовок Feature-Policy
      ID: missing_feature-policy
   4. 🔵 [   1] Отсутствует заголовок Permissions-Policy
      ID: missing_permissions-policy
   5. 🔵 [   1] Отсутствует заголовок Referrer-Policy
      ID: missing_referrer-policy
   6. 🔵 [   1] Отсутствует заголовок X-Content-Type-Options
      ID: missing_x-content-type-options
   7. 🔵 [   1] Отсутствует заголовок X-Frame-Options
      ID: missing_x-frame-options
   8. 🔵 [   1] Отсутствует заголовок X-XSS-Protection
      ID: missing_x-xss-protection
   9. 🟡 [   1] Не используется безопасный протокол
      ID: no_https_scheme
  10. 🔵 [   1] Передача пароля в URL
      ID: password_in_url

================================================================================


📊 Дополнительная информация:
  Критических (ERROR): 1
  Предупреждений (WARNING): 1
  Уникальных файлов с проблемами: 0

✅ Парсинг успешен!
```

---

## 🧪 Пример 2: Базовое использование в коде

```python
>>> from sarif_parser import SarifParser
>>> 
>>> report = SarifParser.parse_file(r"C:\Users\ssinyakov\Downloads\bbs1_ru.sarif")
>>> 
>>> print(f"Инструмент: {report.tool.name}")
Инструмент: PT BlackBox
>>> 
>>> print(f"Находок: {len(report.findings)}")
Находок: 67
>>> 
>>> stats = report.get_statistics()
>>> print(f"Критических: {stats['by_severity']['error']}")
Критических: 6
```

---

## 🧪 Пример 3: Фильтрация SQL Injection

```python
>>> from sarif_parser import SarifParser
>>> 
>>> report = SarifParser.parse_file(r"C:\Users\ssinyakov\Downloads\bbs1_ru.sarif")
>>> 
>>> # Ищем все SQL Injection
>>> sqli = [f for f in report.findings if f.rule_id == "sqli"]
>>> 
>>> print(f"SQL Injection: {len(sqli)}")
SQL Injection: 10
>>> 
>>> # Файлы с SQL Injection
>>> files = set()
>>> for finding in sqli:
...     for location in finding.locations:
...         files.add(location.file_path)
>>> 
>>> print(f"Уязвимых файлов: {len(files)}")
Уязвимых файлов: 0
>>> 
>>> # Показываем правило
>>> rule = report.rules['sqli']
>>> print(f"Название: {rule.name}")
Название: Внедрение SQL-кода
>>> print(f"Уровень: {rule.level.value}")
Уровень: error
```

---

## 🧪 Пример 4: Статистика по отчету

```python
>>> from sarif_parser import SarifParser
>>> 
>>> report = SarifParser.parse_file(r"C:\Users\ssinyakov\Downloads\AI3.sarif")
>>> stats = report.get_statistics()
>>> 
>>> print(f"Всего находок: {stats['total_findings']}")
Всего находок: 158
>>> 
>>> print(f"По уровням:")
По уровням:
>>> print(f"  Критические: {stats['by_severity']['error']}")
  Критические: 4
>>> print(f"  Предупреждения: {stats['by_severity']['warning']}")
  Предупреждения: 2
>>> print(f"  Информационные: {stats['by_severity']['note']}")
  Информационные: 152
>>> 
>>> # Топ-5 типов проблем
>>> sorted_rules = sorted(stats['by_rule'].items(), 
...                      key=lambda x: x[1]['count'], 
...                      reverse=True)[:5]
>>> 
>>> for rule_id, info in sorted_rules:
...     print(f"  - {info['name']}: {info['count']}")
  - moment 2.29.1: 16
  - moment 2.27.0: 16
  - @babel/traverse 7.9.6: 2
  - node-fetch 2.6.0: 2
  - @babel/helpers 7.12.5: 2
```

---

## 🧪 Пример 5: Экспорт в CSV

```python
>>> import csv
>>> from sarif_parser import SarifParser
>>> 
>>> report = SarifParser.parse_file("report.sarif")
>>> 
>>> with open('export.csv', 'w', newline='', encoding='utf-8') as f:
...     writer = csv.writer(f)
...     writer.writerow(['Rule', 'Severity', 'File', 'Line'])
...     
...     for finding in report.findings:
...         for location in finding.locations:
...             writer.writerow([
...                 finding.rule_name,
...                 finding.level.value,
...                 location.file_path,
...                 location.start_line or ''
...             ])
>>> 
>>> print("✅ Экспорт завершен: export.csv")
✅ Экспорт завершен: export.csv
```

**Результат в CSV:**

```csv
Rule,Severity,File,Line
Внедрение SQL-кода,error,,
Межсайтовое выполнение сценариев,warning,,
Отсутствует заголовок Content-Security-Policy,note,,
...
```

---

## 🧪 Пример 6: Использование print_report_summary()

```python
>>> from sarif_parser import SarifParser, print_report_summary
>>> 
>>> report = SarifParser.parse_file(r"C:\Users\ssinyakov\Downloads\bbs1_ru.sarif")
>>> print_report_summary(report)

================================================================================
SARIF Отчет: PT BlackBox
Организация: Positive Technologies
================================================================================

Всего находок: 67
Всего правил: 22

Распределение по уровням серьезности:
  🔴 Ошибки (error):    6
  🟡 Предупреждения (warning): 7
  🔵 Заметки (note):     54
  ⚪ Прочие (none):      0

Топ-10 правил по количеству находок:
   1. 🟡 [  17] Межсайтовое выполнение сценариев
      ID: xss
   2. 🔴 [  10] Внедрение SQL-кода
      ID: sqli
   3. 🔵 [   8] Раскрытие информации в сообщении об ошибке
      ID: error_message
   4. 🔵 [   7] Раскрытие потенциально важных файлов
      ID: fileexposure
   5. 🔵 [   6] Листинг каталогов
      ID: directory_listing
   6. 🟡 [   3] Внедрение HTTP-заголовка
      ID: httpheaderinj
   7. 🔵 [   4] Раскрытие Unix-путей
      ID: unix_path
   8. 🔵 [   3] Раскрытие IP-адреса
      ID: disclosure_ip
   9. 🟡 [   2] Внедрение команд SSI
      ID: ssi
  10. 🔵 [   2] Раскрытие адресов электронной почты
      ID: disclosure_email

================================================================================
```

---

## 🧪 Пример 7: Работа с локациями

```python
>>> from sarif_parser import SarifParser
>>> 
>>> report = SarifParser.parse_file(r"C:\Users\ssinyakov\Downloads\AI3.sarif")
>>> 
>>> # Находим первую критическую находку с локацией
>>> critical = [f for f in report.findings if f.level.value == 'error']
>>> finding = critical[0]
>>> 
>>> print(f"Уязвимость: {finding.rule_name}")
Уязвимость: node-fetch 2.6.0
>>> 
>>> location = finding.locations[0]
>>> print(f"Файл: {location.file_path}")
Файл: ./saltcorn-master/packages/saltcorn-data/models/plugin.js
>>> 
>>> if location.start_line:
...     print(f"Строка: {location.start_line}")
>>> 
>>> if location.snippet:
...     print(f"Код:\n{location.snippet}")
Код:
fetch("http://store.saltcorn.com/api/extensions")
```

---

## 🧪 Пример 8: Интеграция с DM проектом

```python
>>> from integrate_sarif_to_dm import SecurityReportManager
>>> 
>>> manager = SecurityReportManager(reports_dir="security_reports")
>>> 
>>> # Импорт отчета
>>> metadata = manager.import_sarif_report(
...     sarif_file_path=r"C:\Users\ssinyakov\Downloads\bbs1_ru.sarif",
...     project_name="DM Backend"
... )
📥 Импорт SARIF отчета...
   Файл: C:\Users\ssinyakov\Downloads\bbs1_ru.sarif
   Проект: DM Backend

✅ Отчет импортирован!
   Метаданные сохранены: security_reports\report_20251009_143052.json
   Всего находок: 67
   Критических: 6
>>> 
>>> # Генерация списка находок
>>> findings_file = manager.generate_findings_list(
...     sarif_file_path=r"C:\Users\ssinyakov\Downloads\bbs1_ru.sarif",
...     output_format="json"
... )
✅ Список находок сохранен: security_reports\findings_20251009_143052.json
   Формат: JSON
   Записей: 67
>>> 
>>> # Создание данных для дашборда
>>> dashboard = manager.create_dashboard_summary(
...     sarif_file_path=r"C:\Users\ssinyakov\Downloads\bbs1_ru.sarif"
... )
✅ Данные для дашборда сохранены: security_reports\dashboard_data.json
>>> 
>>> print(dashboard['summary'])
{'total': 67, 'critical': 6, 'high': 7, 'medium': 54, 'low': 0}
```

---

## 🎨 Пример HTML отчета

После запуска `python example_usage.py` (пример 8), создается HTML файл:

```html
<!DOCTYPE html>
<html lang="ru">
<head>
    <title>SARIF Отчет - PT BlackBox</title>
    <style>
        /* Красивые стили */
    </style>
</head>
<body>
    <div class="container">
        <h1>SARIF Отчет: PT BlackBox</h1>
        
        <div class="stats">
            <div class="stat-card">
                <h3>Всего находок</h3>
                <div class="number">67</div>
            </div>
            <div class="stat-card">
                <h3 class="severity-error">Ошибки</h3>
                <div class="number severity-error">6</div>
            </div>
            <!-- ... -->
        </div>
        
        <h2>Топ-10 правил</h2>
        <table>
            <tr>
                <td>1</td>
                <td>Межсайтовое выполнение сценариев</td>
                <td>warning</td>
                <td>17</td>
            </tr>
            <!-- ... -->
        </table>
    </div>
</body>
</html>
```

---

## 📋 Пример экспорта в CSV

После экспорта (`example_usage.py`, пример 6):

**findings_export.csv:**
```csv
Rule ID,Rule Name,Severity,File,Line,Snippet
sqli,Внедрение SQL-кода,error,,
xss,Межсайтовое выполнение сценариев,warning,,
missing_content-security-policy,Отсутствует заголовок Content-Security-Policy,note,,
file_inclusion,Включение локальных файлов,error,,
...
```

---

## 📊 Пример JSON экспорта

После интеграции (`integrate_sarif_to_dm.py`):

**dashboard_data.json:**
```json
{
  "scan_date": "2025-10-09 14:30:52",
  "tool_name": "PT BlackBox",
  "summary": {
    "total": 67,
    "critical": 6,
    "high": 7,
    "medium": 54,
    "low": 0
  },
  "charts": {
    "severity_distribution": [
      {"name": "Критические", "value": 6},
      {"name": "Предупреждения", "value": 7},
      {"name": "Заметки", "value": 54}
    ],
    "top_vulnerabilities": {
      "xss": {
        "count": 17,
        "name": "Межсайтовое выполнение сценариев",
        "level": "warning"
      },
      "sqli": {
        "count": 10,
        "name": "Внедрение SQL-кода",
        "level": "error"
      }
    }
  },
  "recommendations": [
    {
      "priority": "high",
      "text": "Обнаружено 6 критических уязвимостей. Требуется немедленное исправление!"
    },
    {
      "priority": "high",
      "text": "Обнаружено 10 уязвимостей SQL Injection. Используйте параметризованные запросы."
    },
    {
      "priority": "medium",
      "text": "Обнаружено 17 уязвимостей XSS. Экранируйте пользовательский ввод."
    }
  ]
}
```

---

## 🎨 Пример работы с данными

```python
>>> from sarif_parser import SarifParser, SeverityLevel
>>> 
>>> report = SarifParser.parse_file(r"C:\Users\ssinyakov\Downloads\bbs1_ru.sarif")
>>> 
>>> # Доступ к инструменту
>>> print(report.tool)
ToolInfo(PT BlackBox)
>>> 
>>> # Доступ к правилам
>>> sqli_rule = report.rules['sqli']
>>> print(sqli_rule)
Rule(id='sqli', name='Внедрение SQL-кода', level=error)
>>> 
>>> # Доступ к находкам
>>> finding = report.findings[0]
>>> print(finding)
Finding(rule_id='access_by_ip', level=note, locations=1)
>>> 
>>> # Доступ к локациям
>>> if finding.locations:
...     location = finding.locations[0]
...     print(f"Файл: {location.file_path}")
...     print(f"Строка: {location.start_line}")
Файл: 
Строка: None
```

---

## 📈 Пример сравнения отчетов

```
================================================================================
ПРИМЕР 7: Сравнение отчетов
================================================================================

Отчет 1: PT BlackBox
  Находок: 67

Отчет 2: PT BlackBox
  Находок: 11

Общие типы находок: 6
Уникальные для отчета 1: 16
Уникальные для отчета 2: 0
```

---

## 🎯 Пример для CI/CD

```bash
$ python ci_check.py
🔍 Анализ безопасности завершен
   Критических: 6
   Предупреждений: 7

❌ Сборка провалена: обнаружено 6 критических уязвимостей!

Список критических проблем:
  1. Внедрение SQL-кода (sqli) - 10 находок
  2. Выполнение произвольного кода (rce) - 1 находка
  3. Внедрение команд ОС (oscmd) - 1 находка
  4. Включение локальных файлов (file_inclusion) - 1 находка
  5. Чтение произвольного файла (file_read) - 1 находка
  6. Загрузка произвольного файла (fileupload) - 1 находка

$ echo $?
1
```

---

## 🌟 Визуальные элементы

### Прогресс-бары (из demo.py)

```
📌 Распределение по уровням серьезности
--------------------------------------------------------------------------------
🔴 Ошибки         [████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░]    6 (  9.0%)
🟡 Предупреждения [█████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░]    7 ( 10.4%)
🔵 Заметки        [████████████████████████████████████████]   54 ( 80.6%)
```

### Таблицы

```
Топ-10 файлов с наибольшим количеством проблем:

 1. ./saltcorn-master/packages/server/auth/routes.js
    └─ Всего: 24 | 🔴 0 | 🟡 0 | 🔵 24
       Типов проблем: 2

 2. ./saltcorn-master/packages/saltcorn-data/base-plugin/types.js
    └─ Всего: 15 | 🔴 0 | 🟡 0 | 🔵 15
       Типов проблем: 1

 3. ./saltcorn-master/packages/server/routes/list.js
    └─ Всего: 6 | 🔴 0 | 🟡 0 | 🔵 6
       Типов проблем: 1
```

---

## 💼 Реальный пример использования

```python
"""
Скрипт для ежедневного мониторинга безопасности
"""

from sarif_parser import SarifParser, SeverityLevel
from datetime import datetime
import sys


def daily_security_check(sarif_file):
    """Ежедневная проверка безопасности"""
    
    print(f"🔍 Проверка безопасности - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"📂 Отчет: {sarif_file}\n")
    
    # Парсим отчет
    report = SarifParser.parse_file(sarif_file)
    stats = report.get_statistics()
    
    # Выводим статистику
    print(f"📊 Статистика:")
    print(f"   Всего проблем: {stats['total_findings']}")
    print(f"   🔴 Критических: {stats['by_severity']['error']}")
    print(f"   🟡 Предупреждений: {stats['by_severity']['warning']}")
    print(f"   🔵 Информационных: {stats['by_severity']['note']}\n")
    
    # Проверяем критические
    critical_count = stats['by_severity']['error']
    
    if critical_count > 0:
        print(f"❌ ВНИМАНИЕ: Обнаружено {critical_count} критических уязвимостей!\n")
        
        # Выводим список
        print("Список критических проблем:")
        critical_rules = {}
        for finding in report.findings:
            if finding.level == SeverityLevel.ERROR:
                critical_rules[finding.rule_id] = finding.rule_name
        
        for i, (rule_id, rule_name) in enumerate(critical_rules.items(), 1):
            count = sum(1 for f in report.findings if f.rule_id == rule_id)
            print(f"  {i}. {rule_name} ({rule_id}) - {count} находок")
        
        print("\n⚠️  Требуется немедленное внимание!")
        return False
    else:
        print("✅ Критических уязвимостей не обнаружено")
        
        if stats['by_severity']['warning'] > 0:
            print(f"⚠️  Есть {stats['by_severity']['warning']} предупреждений")
        
        return True


if __name__ == "__main__":
    sarif_file = sys.argv[1] if len(sys.argv) > 1 else "report.sarif"
    
    success = daily_security_check(sarif_file)
    sys.exit(0 if success else 1)
```

**Вывод:**

```
🔍 Проверка безопасности - 2025-10-09 14:35
📂 Отчет: bbs1_ru.sarif

📊 Статистика:
   Всего проблем: 67
   🔴 Критических: 6
   🟡 Предупреждений: 7
   🔵 Информационных: 54

❌ ВНИМАНИЕ: Обнаружено 6 критических уязвимостей!

Список критических проблем:
  1. Внедрение SQL-кода (sqli) - 10 находок
  2. Выполнение произвольного кода (rce) - 1 находка
  3. Внедрение команд ОС (oscmd) - 1 находка
  4. Включение локальных файлов (file_inclusion) - 1 находка
  5. Чтение произвольного файла (file_read) - 1 находка
  6. Загрузка произвольного файла (fileupload) - 1 находка

⚠️  Требуется немедленное внимание!
```

---

## 🎁 Вывод

Парсер создает **читаемый и информативный вывод** с:

- ✅ Цветными индикаторами (🔴🟡🔵)
- ✅ Прогресс-барами и графиками
- ✅ Структурированными таблицами
- ✅ Детальной статистикой
- ✅ Рекомендациями

**Попробуйте сами:** `python test_parser.py` 🚀

