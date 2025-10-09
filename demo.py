"""
Демонстрация работы SARIF парсера
Визуальная презентация возможностей
"""

from sarif_parser import SarifParser, SeverityLevel, print_report_summary
import os


def print_header(text):
    """Красивый заголовок"""
    print(f"\n{'='*80}")
    print(f"  {text}")
    print(f"{'='*80}\n")


def print_section(title):
    """Заголовок секции"""
    print(f"\n{'-'*80}")
    print(f"📌 {title}")
    print(f"{'-'*80}")


def demo_basic_parsing():
    """Демо 1: Базовый парсинг"""
    print_header("ДЕМО 1: Базовый парсинг SARIF файла")
    
    file_path = r"C:\Users\ssinyakov\Downloads\bbs2_ru.sarif"
    
    if not os.path.exists(file_path):
        print(f"⚠️  Файл не найден: {file_path}")
        print("Используйте свой путь к SARIF файлу")
        return
    
    print(f"📂 Файл: {os.path.basename(file_path)}")
    print(f"📊 Размер: {os.path.getsize(file_path) / 1024:.1f} KB\n")
    
    # Парсинг
    print("⏳ Парсинг...")
    report = SarifParser.parse_file(file_path)
    print("✅ Готово!\n")
    
    # Базовая информация
    print(f"🔧 Инструмент: {report.tool.name}")
    if report.tool.version:
        print(f"📦 Версия: {report.tool.version}")
    if report.tool.organization:
        print(f"🏢 Организация: {report.tool.organization}")
    
    print(f"\n📋 Всего правил: {len(report.rules)}")
    print(f"🔍 Всего находок: {len(report.findings)}")


def demo_statistics():
    """Демо 2: Статистика"""
    print_header("ДЕМО 2: Детальная статистика")
    
    file_path = r"C:\Users\ssinyakov\Downloads\bbs1_ru.sarif"
    
    if not os.path.exists(file_path):
        print(f"⚠️  Файл не найден: {file_path}")
        return
    
    report = SarifParser.parse_file(file_path)
    stats = report.get_statistics()
    
    print_section("Распределение по уровням серьезности")
    
    total = stats['total_findings']
    
    # Визуальные индикаторы
    error_count = stats['by_severity']['error']
    warning_count = stats['by_severity']['warning']
    note_count = stats['by_severity']['note']
    
    def print_bar(label, count, total, icon, color):
        """Рисует прогресс-бар"""
        percentage = (count / total * 100) if total > 0 else 0
        bar_length = 40
        filled = int(bar_length * count / total) if total > 0 else 0
        bar = '█' * filled + '░' * (bar_length - filled)
        print(f"{icon} {label:15} [{bar}] {count:4} ({percentage:5.1f}%)")
    
    print_bar("Ошибки", error_count, total, "🔴", "red")
    print_bar("Предупреждения", warning_count, total, "🟡", "yellow")
    print_bar("Заметки", note_count, total, "🔵", "blue")
    
    print_section("Топ-10 типов уязвимостей")
    
    sorted_rules = sorted(
        stats['by_rule'].items(),
        key=lambda x: x[1]['count'],
        reverse=True
    )
    
    for i, (rule_id, info) in enumerate(sorted_rules[:10], 1):
        icon = {
            'error': '🔴',
            'warning': '🟡',
            'note': '🔵',
            'none': '⚪'
        }.get(info['level'], '⚪')
        
        print(f"{i:2}. {icon} {info['name']}")
        print(f"    └─ Находок: {info['count']} | ID: {rule_id}")


def demo_filtering():
    """Демо 3: Фильтрация"""
    print_header("ДЕМО 3: Фильтрация находок")
    
    file_path = r"C:\Users\ssinyakov\Downloads\AI3.sarif"
    
    if not os.path.exists(file_path):
        print(f"⚠️  Файл не найден: {file_path}")
        return
    
    report = SarifParser.parse_file(file_path)
    
    print_section("Фильтр 1: Только критические уязвимости")
    
    critical = [f for f in report.findings if f.level == SeverityLevel.ERROR]
    print(f"Найдено критических: {len(critical)}")
    
    if critical:
        print("\nПримеры:")
        for i, finding in enumerate(critical[:3], 1):
            print(f"\n{i}. {finding.rule_name}")
            print(f"   ID: {finding.rule_id}")
            if finding.locations:
                print(f"   Файл: {finding.locations[0].file_path}")
                if finding.locations[0].start_line:
                    print(f"   Строка: {finding.locations[0].start_line}")
    
    print_section("Фильтр 2: По типу уязвимости")
    
    # Ищем SQL Injection
    sqli = [f for f in report.findings if 'sql' in f.rule_id.lower()]
    print(f"SQL Injection: {len(sqli)}")
    
    # Ищем XSS
    xss = [f for f in report.findings if 'xss' in f.rule_id.lower()]
    print(f"Cross-Site Scripting (XSS): {len(xss)}")
    
    # Ищем RCE
    rce = [f for f in report.findings if any(x in f.rule_id.lower() for x in ['rce', 'code execution'])]
    print(f"Remote Code Execution (RCE): {len(rce)}")


def demo_file_analysis():
    """Демо 4: Анализ файлов"""
    print_header("ДЕМО 4: Анализ пораженных файлов")
    
    file_path = r"C:\Users\ssinyakov\Downloads\bbs1_ru.sarif"
    
    if not os.path.exists(file_path):
        print(f"⚠️  Файл не найден: {file_path}")
        return
    
    report = SarifParser.parse_file(file_path)
    
    print_section("Анализ по файлам")
    
    # Собираем статистику по файлам
    from collections import defaultdict
    
    files_stats = defaultdict(lambda: {
        'total': 0,
        'critical': 0,
        'warnings': 0,
        'notes': 0,
        'types': set()
    })
    
    for finding in report.findings:
        for location in finding.locations:
            if location.file_path:
                file = location.file_path
                files_stats[file]['total'] += 1
                files_stats[file]['types'].add(finding.rule_id)
                
                if finding.level == SeverityLevel.ERROR:
                    files_stats[file]['critical'] += 1
                elif finding.level == SeverityLevel.WARNING:
                    files_stats[file]['warnings'] += 1
                else:
                    files_stats[file]['notes'] += 1
    
    print(f"Всего уникальных файлов с проблемами: {len(files_stats)}")
    
    # Топ-10 файлов
    sorted_files = sorted(
        files_stats.items(),
        key=lambda x: x[1]['total'],
        reverse=True
    )
    
    print("\nТоп-10 файлов с наибольшим количеством проблем:\n")
    
    for i, (file, stats) in enumerate(sorted_files[:10], 1):
        # Укорачиваем путь для читаемости
        short_path = file if len(file) < 60 else "..." + file[-57:]
        
        print(f"{i:2}. {short_path}")
        print(f"    └─ Всего: {stats['total']} | ", end="")
        print(f"🔴 {stats['critical']} | ", end="")
        print(f"🟡 {stats['warnings']} | ", end="")
        print(f"🔵 {stats['notes']}")
        print(f"       Типов проблем: {len(stats['types'])}")


def demo_export():
    """Демо 5: Экспорт данных"""
    print_header("ДЕМО 5: Экспорт данных")
    
    file_path = r"C:\Users\ssinyakov\Downloads\bbs2_ru.sarif"
    
    if not os.path.exists(file_path):
        print(f"⚠️  Файл не найден: {file_path}")
        return
    
    report = SarifParser.parse_file(file_path)
    
    print_section("Экспорт в CSV")
    
    import csv
    
    output_file = "demo_export.csv"
    
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=[
            'Rule ID',
            'Rule Name',
            'Severity',
            'File',
            'Line',
            'Snippet'
        ])
        
        writer.writeheader()
        
        for finding in report.findings:
            for location in finding.locations:
                writer.writerow({
                    'Rule ID': finding.rule_id,
                    'Rule Name': finding.rule_name or '',
                    'Severity': finding.level.value,
                    'File': location.file_path,
                    'Line': location.start_line or '',
                    'Snippet': (location.snippet or '')[:100]
                })
    
    print(f"✅ Экспортировано в: {output_file}")
    print(f"📊 Записей: {sum(len(f.locations) for f in report.findings)}")
    
    print_section("Экспорт в JSON")
    
    import json
    
    output_file = "demo_export.json"
    
    data = {
        'metadata': {
            'tool': report.tool.name,
            'version': report.tool.version,
            'total_findings': len(report.findings)
        },
        'statistics': report.get_statistics(),
        'findings': [
            {
                'id': finding.rule_id,
                'name': finding.rule_name,
                'severity': finding.level.value,
                'locations': [
                    {
                        'file': loc.file_path,
                        'line': loc.start_line
                    }
                    for loc in finding.locations
                ]
            }
            for finding in report.findings[:10]  # Только первые 10
        ]
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Экспортировано в: {output_file}")


def main():
    """Главная функция - запуск всех демо"""
    
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║                        🔍 SARIF PARSER - ДЕМОНСТРАЦИЯ                        ║
║                                                                              ║
║             Парсер отчетов о безопасности в формате SARIF 2.1.0             ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
""")
    
    demos = [
        ("Базовый парсинг", demo_basic_parsing),
        ("Детальная статистика", demo_statistics),
        ("Фильтрация находок", demo_filtering),
        ("Анализ файлов", demo_file_analysis),
        ("Экспорт данных", demo_export),
    ]
    
    print("\nДоступные демонстрации:\n")
    for i, (name, _) in enumerate(demos, 1):
        print(f"  {i}. {name}")
    
    print("\n" + "="*80)
    
    # Запускаем все демо по очереди
    for name, demo_func in demos:
        try:
            demo_func()
            input("\n⏸  Нажмите Enter для продолжения...")
        except FileNotFoundError as e:
            print(f"\n⚠️  Пропущено: файл не найден")
            input("\n⏸  Нажмите Enter для продолжения...")
        except Exception as e:
            print(f"\n❌ Ошибка: {e}")
            import traceback
            traceback.print_exc()
            input("\n⏸  Нажмите Enter для продолжения...")
    
    print_header("ДЕМОНСТРАЦИЯ ЗАВЕРШЕНА")
    print("""
✨ Все возможности продемонстрированы!

📚 Дополнительная информация:
  - README_SARIF_PARSER.md  - полная документация
  - QUICKSTART.md            - быстрый старт
  - example_usage.py         - больше примеров

🚀 Готово к использованию в вашем проекте!
""")


if __name__ == "__main__":
    main()

