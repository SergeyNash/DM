"""
Тестирование SARIF парсера
"""

import sys
import os

# Добавляем текущую директорию в путь
sys.path.insert(0, os.path.dirname(__file__))

from sarif_parser import SarifParser, print_report_summary, SeverityLevel


def test_parse_files():
    """Тест парсинга файлов"""
    
    # Пути к файлам
    test_files = [
        r"C:\Users\ssinyakov\Downloads\bbs2_ru.sarif",
        r"C:\Users\ssinyakov\Downloads\bbs1_ru.sarif",
        r"C:\Users\ssinyakov\Downloads\AI3.sarif",
    ]
    
    for file_path in test_files:
        if not os.path.exists(file_path):
            print(f"⚠️  Файл не найден: {file_path}")
            continue
        
        print(f"\n{'='*80}")
        print(f"Тестирование файла: {os.path.basename(file_path)}")
        print(f"{'='*80}")
        
        try:
            # Парсим файл
            report = SarifParser.parse_file(file_path)
            
            # Выводим краткую информацию
            print_report_summary(report)
            
            # Дополнительная статистика
            print("\n📊 Дополнительная информация:")
            
            # Подсчет критических находок
            critical = [f for f in report.findings if f.level == SeverityLevel.ERROR]
            warnings = [f for f in report.findings if f.level == SeverityLevel.WARNING]
            
            print(f"  Критических (ERROR): {len(critical)}")
            print(f"  Предупреждений (WARNING): {len(warnings)}")
            
            # Уникальные файлы с уязвимостями
            files_with_issues = set()
            for finding in report.findings:
                for location in finding.locations:
                    if location.file_path:
                        files_with_issues.add(location.file_path)
            
            print(f"  Уникальных файлов с проблемами: {len(files_with_issues)}")
            
            # Показываем несколько примеров файлов
            if files_with_issues:
                print(f"\n  Примеры файлов с проблемами (первые 5):")
                for i, file_path in enumerate(sorted(files_with_issues)[:5], 1):
                    print(f"    {i}. {file_path}")
            
            print(f"\n✅ Парсинг успешен!")
            
        except Exception as e:
            print(f"\n❌ Ошибка при парсинге: {e}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    print("🔍 SARIF Parser - Тестирование\n")
    test_parse_files()
    print("\n✨ Тестирование завершено!")

