"""
Интеграция SARIF парсера с проектом Document Management (DM)

Этот скрипт демонстрирует, как можно интегрировать SARIF парсер
в существующий проект для управления отчетами безопасности.
"""

from sarif_parser import SarifParser, SeverityLevel
from datetime import datetime
from pathlib import Path
import json


class SecurityReportManager:
    """Менеджер отчетов безопасности для DM проекта"""
    
    def __init__(self, reports_dir="security_reports"):
        """
        Инициализация менеджера
        
        Args:
            reports_dir: директория для хранения отчетов
        """
        self.reports_dir = Path(reports_dir)
        self.reports_dir.mkdir(exist_ok=True)
    
    def import_sarif_report(self, sarif_file_path, project_name="Unknown"):
        """
        Импорт SARIF отчета в систему управления
        
        Args:
            sarif_file_path: путь к SARIF файлу
            project_name: название проекта
            
        Returns:
            dict с информацией об импортированном отчете
        """
        print(f"📥 Импорт SARIF отчета...")
        print(f"   Файл: {sarif_file_path}")
        print(f"   Проект: {project_name}")
        
        # Парсим SARIF файл
        report = SarifParser.parse_file(sarif_file_path)
        stats = report.get_statistics()
        
        # Создаем метаданные отчета
        report_metadata = {
            'import_date': datetime.now().isoformat(),
            'project_name': project_name,
            'source_file': str(sarif_file_path),
            'tool': {
                'name': report.tool.name,
                'version': report.tool.version,
                'organization': report.tool.organization
            },
            'statistics': {
                'total_findings': stats['total_findings'],
                'total_rules': stats['total_rules'],
                'by_severity': stats['by_severity'],
                'critical_files': self._get_critical_files(report),
                'top_issues': self._get_top_issues(stats)
            }
        }
        
        # Сохраняем метаданные
        metadata_file = self.reports_dir / f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(report_metadata, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Отчет импортирован!")
        print(f"   Метаданные сохранены: {metadata_file}")
        print(f"   Всего находок: {stats['total_findings']}")
        print(f"   Критических: {stats['by_severity']['error']}")
        
        return report_metadata
    
    def _get_critical_files(self, report):
        """Получить список критичных файлов"""
        critical_files = set()
        
        for finding in report.findings:
            if finding.level == SeverityLevel.ERROR:
                for location in finding.locations:
                    if location.file_path:
                        critical_files.add(location.file_path)
        
        return list(critical_files)
    
    def _get_top_issues(self, stats, limit=5):
        """Получить топ проблем"""
        sorted_rules = sorted(
            stats['by_rule'].items(),
            key=lambda x: x[1]['count'],
            reverse=True
        )
        
        return [
            {
                'rule_id': rule_id,
                'name': info['name'],
                'count': info['count'],
                'severity': info['level']
            }
            for rule_id, info in sorted_rules[:limit]
        ]
    
    def generate_findings_list(self, sarif_file_path, output_format="json"):
        """
        Генерация списка находок для импорта в DM
        
        Args:
            sarif_file_path: путь к SARIF файлу
            output_format: формат вывода ('json', 'csv')
            
        Returns:
            путь к созданному файлу
        """
        report = SarifParser.parse_file(sarif_file_path)
        
        findings_list = []
        
        for finding in report.findings:
            for location in finding.locations:
                finding_entry = {
                    'id': f"{finding.rule_id}_{hash(location.file_path)}",
                    'title': finding.rule_name or finding.rule_id,
                    'description': finding.message or '',
                    'severity': finding.level.value,
                    'status': 'open',
                    'file_path': location.file_path,
                    'line_number': location.start_line,
                    'code_snippet': location.snippet,
                    'rule_id': finding.rule_id,
                    'detected_date': datetime.now().isoformat()
                }
                findings_list.append(finding_entry)
        
        if output_format == "json":
            output_file = self.reports_dir / f"findings_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(findings_list, f, indent=2, ensure_ascii=False)
        
        elif output_format == "csv":
            import csv
            output_file = self.reports_dir / f"findings_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            
            if findings_list:
                with open(output_file, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=findings_list[0].keys())
                    writer.writeheader()
                    writer.writerows(findings_list)
        
        print(f"✅ Список находок сохранен: {output_file}")
        print(f"   Формат: {output_format.upper()}")
        print(f"   Записей: {len(findings_list)}")
        
        return str(output_file)
    
    def create_dashboard_summary(self, sarif_file_path):
        """
        Создать данные для дашборда DM
        
        Args:
            sarif_file_path: путь к SARIF файлу
            
        Returns:
            dict с данными для дашборда
        """
        report = SarifParser.parse_file(sarif_file_path)
        stats = report.get_statistics()
        
        # Формируем данные для дашборда
        dashboard_data = {
            'scan_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'tool_name': report.tool.name,
            'summary': {
                'total': stats['total_findings'],
                'critical': stats['by_severity']['error'],
                'high': stats['by_severity']['warning'],
                'medium': stats['by_severity']['note'],
                'low': 0
            },
            'charts': {
                'severity_distribution': [
                    {'name': 'Критические', 'value': stats['by_severity']['error']},
                    {'name': 'Предупреждения', 'value': stats['by_severity']['warning']},
                    {'name': 'Заметки', 'value': stats['by_severity']['note']}
                ],
                'top_vulnerabilities': stats['by_rule']
            },
            'recommendations': self._generate_recommendations(report)
        }
        
        # Сохраняем для дашборда
        output_file = self.reports_dir / "dashboard_data.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(dashboard_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Данные для дашборда сохранены: {output_file}")
        
        return dashboard_data
    
    def _generate_recommendations(self, report):
        """Генерация рекомендаций на основе находок"""
        recommendations = []
        
        # Подсчет критических
        critical_count = sum(
            1 for f in report.findings 
            if f.level == SeverityLevel.ERROR
        )
        
        if critical_count > 0:
            recommendations.append({
                'priority': 'high',
                'text': f'Обнаружено {critical_count} критических уязвимостей. Требуется немедленное исправление!'
            })
        
        # Подсчет SQL Injection
        sqli_count = sum(
            1 for f in report.findings 
            if 'sql' in f.rule_id.lower()
        )
        
        if sqli_count > 0:
            recommendations.append({
                'priority': 'high',
                'text': f'Обнаружено {sqli_count} уязвимостей SQL Injection. Используйте параметризованные запросы.'
            })
        
        # Подсчет XSS
        xss_count = sum(
            1 for f in report.findings 
            if 'xss' in f.rule_id.lower()
        )
        
        if xss_count > 0:
            recommendations.append({
                'priority': 'medium',
                'text': f'Обнаружено {xss_count} уязвимостей XSS. Экранируйте пользовательский ввод.'
            })
        
        return recommendations


def demo_integration():
    """Демонстрация интеграции с DM проектом"""
    
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║             🔗 ИНТЕГРАЦИЯ SARIF ПАРСЕРА С ПРОЕКТОМ DM                        ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
""")
    
    # Создаем менеджер
    manager = SecurityReportManager(reports_dir="security_reports")
    
    print("\n📁 Директория для отчетов создана: security_reports/\n")
    
    # Список файлов для тестирования
    test_files = [
        (r"C:\Users\ssinyakov\Downloads\bbs2_ru.sarif", "DM Project - BlackBox Scan 2"),
        (r"C:\Users\ssinyakov\Downloads\bbs1_ru.sarif", "DM Project - BlackBox Scan 1"),
    ]
    
    for sarif_file, project_name in test_files:
        if not Path(sarif_file).exists():
            print(f"⏭  Пропуск: {sarif_file} не найден\n")
            continue
        
        print(f"\n{'='*80}")
        print(f"Обработка: {project_name}")
        print(f"{'='*80}\n")
        
        try:
            # 1. Импорт отчета
            metadata = manager.import_sarif_report(sarif_file, project_name)
            
            print("\n" + "-"*80)
            
            # 2. Генерация списка находок
            print("\n📝 Генерация списка находок...")
            findings_file = manager.generate_findings_list(sarif_file, output_format="json")
            
            print("\n" + "-"*80)
            
            # 3. Создание данных для дашборда
            print("\n📊 Создание данных для дашборда...")
            dashboard_data = manager.create_dashboard_summary(sarif_file)
            
            # Показываем рекомендации
            if dashboard_data['recommendations']:
                print("\n💡 Рекомендации:")
                for rec in dashboard_data['recommendations']:
                    priority_icon = {
                        'high': '🔴',
                        'medium': '🟡',
                        'low': '🔵'
                    }.get(rec['priority'], '⚪')
                    print(f"   {priority_icon} {rec['text']}")
            
            input("\n⏸  Нажмите Enter для продолжения...")
            
        except Exception as e:
            print(f"\n❌ Ошибка: {e}")
            import traceback
            traceback.print_exc()
    
    print(f"\n{'='*80}")
    print("✅ Интеграция завершена!")
    print(f"{'='*80}\n")
    
    print("📂 Созданные файлы:")
    if Path("security_reports").exists():
        for file in Path("security_reports").glob("*"):
            print(f"   - {file.name}")
    
    print("""
🎯 Следующие шаги:

1. Интегрировать данные в базу данных DM проекта
2. Создать UI для отображения находок
3. Настроить автоматическое сканирование
4. Добавить систему трекинга исправлений

📚 См. ARCHITECTURE.md для деталей интеграции в DM проект
""")


if __name__ == "__main__":
    demo_integration()

