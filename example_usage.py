"""
Примеры использования SARIF парсера
"""

from sarif_parser import SarifParser, SeverityLevel, print_report_summary, print_detailed_findings


def example_1_basic_parsing():
    """Пример 1: Базовый парсинг файла"""
    print("="*80)
    print("ПРИМЕР 1: Базовый парсинг SARIF файла")
    print("="*80)
    
    # Парсим файл
    report = SarifParser.parse_file("bbs2_ru.sarif")
    
    # Выводим базовую информацию
    print(f"\nИнструмент: {report.tool.name}")
    print(f"Всего находок: {len(report.findings)}")
    print(f"Всего правил: {len(report.rules)}")


def example_2_statistics():
    """Пример 2: Получение статистики"""
    print("\n" + "="*80)
    print("ПРИМЕР 2: Статистика по отчету")
    print("="*80)
    
    report = SarifParser.parse_file("bbs1_ru.sarif")
    stats = report.get_statistics()
    
    print(f"\nОбщая статистика:")
    print(f"  Всего находок: {stats['total_findings']}")
    print(f"  Ошибки: {stats['by_severity']['error']}")
    print(f"  Предупреждения: {stats['by_severity']['warning']}")
    print(f"  Заметки: {stats['by_severity']['note']}")


def example_3_filter_by_severity():
    """Пример 3: Фильтрация по уровню серьезности"""
    print("\n" + "="*80)
    print("ПРИМЕР 3: Фильтрация находок по уровню серьезности")
    print("="*80)
    
    report = SarifParser.parse_file("AI3.sarif")
    
    # Фильтруем только критические ошибки
    critical_findings = [
        f for f in report.findings 
        if f.level == SeverityLevel.ERROR
    ]
    
    print(f"\nКритические находки (ERROR): {len(critical_findings)}")
    
    # Показываем первые 5
    for i, finding in enumerate(critical_findings[:5], 1):
        print(f"\n{i}. {finding.rule_name}")
        print(f"   ID: {finding.rule_id}")
        if finding.locations:
            print(f"   Файл: {finding.locations[0].file_path}")


def example_4_filter_by_rule():
    """Пример 4: Фильтрация по конкретному правилу"""
    print("\n" + "="*80)
    print("ПРИМЕР 4: Фильтрация по конкретному правилу")
    print("="*80)
    
    report = SarifParser.parse_file("bbs1_ru.sarif")
    
    # Ищем все находки SQL Injection
    sqli_findings = [
        f for f in report.findings 
        if f.rule_id == "sqli"
    ]
    
    print(f"\nНайдено SQL Injection: {len(sqli_findings)}")
    
    # Показываем файлы с уязвимостями
    files_with_sqli = set()
    for finding in sqli_findings:
        for location in finding.locations:
            if location.file_path:
                files_with_sqli.add(location.file_path)
    
    print(f"\nФайлы с SQL Injection ({len(files_with_sqli)}):")
    for file_path in sorted(files_with_sqli):
        print(f"  - {file_path}")


def example_5_rules_info():
    """Пример 5: Информация о правилах"""
    print("\n" + "="*80)
    print("ПРИМЕР 5: Информация о правилах")
    print("="*80)
    
    report = SarifParser.parse_file("bbs2_ru.sarif")
    
    print(f"\nВсего правил: {len(report.rules)}")
    print("\nПравила:")
    
    for rule_id, rule in list(report.rules.items())[:5]:
        print(f"\n- ID: {rule_id}")
        print(f"  Название: {rule.name}")
        print(f"  Уровень: {rule.level.value}")
        print(f"  Включено: {rule.enabled}")
        
        if rule.description_markdown:
            # Показываем первые 200 символов описания
            desc = rule.description_markdown[:200].replace('\n', ' ')
            print(f"  Описание: {desc}...")


def example_6_export_to_csv():
    """Пример 6: Экспорт в CSV"""
    print("\n" + "="*80)
    print("ПРИМЕР 6: Экспорт в CSV")
    print("="*80)
    
    import csv
    
    report = SarifParser.parse_file("AI3.sarif")
    
    output_file = "findings_export.csv"
    
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Rule ID', 'Rule Name', 'Severity', 'File', 'Line', 'Snippet']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        
        for finding in report.findings:
            for location in finding.locations:
                writer.writerow({
                    'Rule ID': finding.rule_id,
                    'Rule Name': finding.rule_name or '',
                    'Severity': finding.level.value,
                    'File': location.file_path,
                    'Line': location.start_line or '',
                    'Snippet': (location.snippet or '')[:100]  # Ограничиваем длину
                })
    
    print(f"\nРезультаты экспортированы в: {output_file}")


def example_7_compare_reports():
    """Пример 7: Сравнение двух отчетов"""
    print("\n" + "="*80)
    print("ПРИМЕР 7: Сравнение отчетов")
    print("="*80)
    
    report1 = SarifParser.parse_file("bbs1_ru.sarif")
    report2 = SarifParser.parse_file("bbs2_ru.sarif")
    
    print(f"\nОтчет 1: {report1.tool.name}")
    print(f"  Находок: {len(report1.findings)}")
    
    print(f"\nОтчет 2: {report2.tool.name}")
    print(f"  Находок: {len(report2.findings)}")
    
    # Сравниваем типы находок
    rules1 = set(f.rule_id for f in report1.findings)
    rules2 = set(f.rule_id for f in report2.findings)
    
    common_rules = rules1 & rules2
    unique_to_1 = rules1 - rules2
    unique_to_2 = rules2 - rules1
    
    print(f"\nОбщие типы находок: {len(common_rules)}")
    print(f"Уникальные для отчета 1: {len(unique_to_1)}")
    print(f"Уникальные для отчета 2: {len(unique_to_2)}")


def example_8_generate_html_report():
    """Пример 8: Генерация HTML отчета"""
    print("\n" + "="*80)
    print("ПРИМЕР 8: Генерация HTML отчета")
    print("="*80)
    
    report = SarifParser.parse_file("bbs2_ru.sarif")
    stats = report.get_statistics()
    
    html_content = f"""
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SARIF Отчет - {report.tool.name}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 20px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }}
        h1 {{ color: #333; border-bottom: 3px solid #4CAF50; padding-bottom: 10px; }}
        .stats {{ display: flex; gap: 20px; margin: 20px 0; }}
        .stat-card {{ flex: 1; padding: 20px; background: #f9f9f9; border-radius: 5px; text-align: center; }}
        .stat-card h3 {{ margin: 0; color: #666; }}
        .stat-card .number {{ font-size: 36px; font-weight: bold; color: #4CAF50; margin: 10px 0; }}
        .severity-error {{ color: #f44336; }}
        .severity-warning {{ color: #ff9800; }}
        .severity-note {{ color: #2196F3; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
        th {{ background-color: #4CAF50; color: white; }}
        tr:hover {{ background-color: #f5f5f5; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>SARIF Отчет: {report.tool.name}</h1>
        <p><strong>Версия инструмента:</strong> {report.tool.version or 'N/A'}</p>
        <p><strong>Организация:</strong> {report.tool.organization or 'N/A'}</p>
        
        <div class="stats">
            <div class="stat-card">
                <h3>Всего находок</h3>
                <div class="number">{stats['total_findings']}</div>
            </div>
            <div class="stat-card">
                <h3 class="severity-error">Ошибки</h3>
                <div class="number severity-error">{stats['by_severity']['error']}</div>
            </div>
            <div class="stat-card">
                <h3 class="severity-warning">Предупреждения</h3>
                <div class="number severity-warning">{stats['by_severity']['warning']}</div>
            </div>
            <div class="stat-card">
                <h3 class="severity-note">Заметки</h3>
                <div class="number severity-note">{stats['by_severity']['note']}</div>
            </div>
        </div>
        
        <h2>Топ-10 правил</h2>
        <table>
            <thead>
                <tr>
                    <th>#</th>
                    <th>Правило</th>
                    <th>Уровень</th>
                    <th>Количество</th>
                </tr>
            </thead>
            <tbody>
"""
    
    sorted_rules = sorted(
        stats['by_rule'].items(), 
        key=lambda x: x[1]['count'], 
        reverse=True
    )
    
    for i, (rule_id, rule_info) in enumerate(sorted_rules[:10], 1):
        html_content += f"""
                <tr>
                    <td>{i}</td>
                    <td><strong>{rule_info['name']}</strong><br><small>{rule_id}</small></td>
                    <td><span class="severity-{rule_info['level']}">{rule_info['level']}</span></td>
                    <td><strong>{rule_info['count']}</strong></td>
                </tr>
"""
    
    html_content += """
            </tbody>
        </table>
    </div>
</body>
</html>
"""
    
    output_file = "sarif_report.html"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"\nHTML отчет сгенерирован: {output_file}")


def run_all_examples():
    """Запустить все примеры"""
    examples = [
        example_1_basic_parsing,
        example_2_statistics,
        example_3_filter_by_severity,
        example_4_filter_by_rule,
        example_5_rules_info,
        example_6_export_to_csv,
        example_7_compare_reports,
        example_8_generate_html_report
    ]
    
    for example_func in examples:
        try:
            example_func()
        except FileNotFoundError as e:
            print(f"\n⚠️  Пропущено: {e}")
        except Exception as e:
            print(f"\n❌ Ошибка в {example_func.__name__}: {e}")


if __name__ == "__main__":
    run_all_examples()

