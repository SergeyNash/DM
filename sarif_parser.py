"""
SARIF Parser - парсер для отчетов в формате SARIF 2.1.0

Поддерживаемые инструменты:
- PT BlackBox
- PT Application Inspector
- Другие инструменты, использующие стандарт SARIF 2.1.0
"""

import json
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from pathlib import Path
from enum import Enum


class SeverityLevel(Enum):
    """Уровни серьезности находок"""
    ERROR = "error"
    WARNING = "warning"
    NOTE = "note"
    NONE = "none"


@dataclass
class Rule:
    """Правило (тип уязвимости)"""
    id: str
    name: str
    description_text: Optional[str] = None
    description_markdown: Optional[str] = None
    level: SeverityLevel = SeverityLevel.NOTE
    enabled: bool = True
    
    def __repr__(self):
        return f"Rule(id='{self.id}', name='{self.name}', level={self.level.value})"


@dataclass
class Location:
    """Локация находки в коде"""
    file_path: str
    snippet: Optional[str] = None
    start_line: Optional[int] = None
    end_line: Optional[int] = None
    start_column: Optional[int] = None
    end_column: Optional[int] = None
    
    def __repr__(self):
        location_str = self.file_path
        if self.start_line:
            location_str += f":{self.start_line}"
            if self.end_line and self.end_line != self.start_line:
                location_str += f"-{self.end_line}"
        return f"Location({location_str})"


@dataclass
class Finding:
    """Находка (уязвимость или проблема)"""
    rule_id: str
    rule_name: Optional[str] = None
    message: Optional[str] = None
    level: SeverityLevel = SeverityLevel.NOTE
    locations: List[Location] = field(default_factory=list)
    
    def __repr__(self):
        loc_count = len(self.locations)
        return f"Finding(rule_id='{self.rule_id}', level={self.level.value}, locations={loc_count})"


@dataclass
class ToolInfo:
    """Информация об инструменте сканирования"""
    name: str
    version: Optional[str] = None
    organization: Optional[str] = None
    information_uri: Optional[str] = None
    
    def __repr__(self):
        ver = f" v{self.version}" if self.version else ""
        return f"ToolInfo({self.name}{ver})"


@dataclass
class SarifReport:
    """SARIF отчет"""
    tool: ToolInfo
    rules: Dict[str, Rule] = field(default_factory=dict)
    findings: List[Finding] = field(default_factory=list)
    sarif_version: str = "2.1.0"
    
    def get_statistics(self) -> Dict[str, Any]:
        """Получить статистику по отчету"""
        stats = {
            "total_findings": len(self.findings),
            "total_rules": len(self.rules),
            "by_severity": {
                "error": 0,
                "warning": 0,
                "note": 0,
                "none": 0
            },
            "by_rule": {}
        }
        
        for finding in self.findings:
            # Подсчет по уровню серьезности
            stats["by_severity"][finding.level.value] += 1
            
            # Подсчет по правилам
            rule_id = finding.rule_id
            if rule_id not in stats["by_rule"]:
                stats["by_rule"][rule_id] = {
                    "count": 0,
                    "name": finding.rule_name or rule_id,
                    "level": finding.level.value
                }
            stats["by_rule"][rule_id]["count"] += 1
        
        return stats
    
    def __repr__(self):
        return f"SarifReport(tool={self.tool}, findings={len(self.findings)}, rules={len(self.rules)})"


class SarifParser:
    """Парсер SARIF отчетов"""
    
    @staticmethod
    def parse_file(file_path: str) -> SarifReport:
        """
        Парсить SARIF файл
        
        Args:
            file_path: путь к SARIF файлу
            
        Returns:
            SarifReport объект
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return SarifParser.parse_dict(data)
    
    @staticmethod
    def parse_dict(data: Dict[str, Any]) -> SarifReport:
        """
        Парсить SARIF данные из словаря
        
        Args:
            data: словарь с SARIF данными
            
        Returns:
            SarifReport объект
        """
        sarif_version = data.get("version", "2.1.0")
        
        # Парсим первый run (обычно он один)
        if not data.get("runs"):
            raise ValueError("SARIF файл не содержит запусков (runs)")
        
        run = data["runs"][0]
        
        # Парсим информацию об инструменте
        tool_data = run.get("tool", {}).get("driver", {})
        tool = SarifParser._parse_tool(tool_data)
        
        # Парсим правила
        rules = SarifParser._parse_rules(tool_data.get("rules", []))
        
        # Парсим находки
        findings = SarifParser._parse_findings(run.get("results", []), rules)
        
        return SarifReport(
            tool=tool,
            rules=rules,
            findings=findings,
            sarif_version=sarif_version
        )
    
    @staticmethod
    def _parse_tool(tool_data: Dict[str, Any]) -> ToolInfo:
        """Парсить информацию об инструменте"""
        return ToolInfo(
            name=tool_data.get("name", "Unknown"),
            version=tool_data.get("version"),
            organization=tool_data.get("organization"),
            information_uri=tool_data.get("informationUri")
        )
    
    @staticmethod
    def _parse_rules(rules_data: List[Dict[str, Any]]) -> Dict[str, Rule]:
        """Парсить правила"""
        rules = {}
        
        for rule_data in rules_data:
            rule_id = rule_data.get("id", "")
            
            # Извлекаем описание
            full_desc = rule_data.get("fullDescription", {})
            desc_text = full_desc.get("text")
            desc_markdown = full_desc.get("markdown")
            
            # Извлекаем уровень серьезности
            config = rule_data.get("defaultConfiguration", {})
            level_str = config.get("level", "note")
            try:
                level = SeverityLevel(level_str)
            except ValueError:
                level = SeverityLevel.NOTE
            
            rule = Rule(
                id=rule_id,
                name=rule_data.get("name", rule_id),
                description_text=desc_text,
                description_markdown=desc_markdown,
                level=level,
                enabled=config.get("enabled", True)
            )
            
            rules[rule_id] = rule
        
        return rules
    
    @staticmethod
    def _parse_findings(results_data: List[Dict[str, Any]], 
                       rules: Dict[str, Rule]) -> List[Finding]:
        """Парсить находки"""
        findings = []
        
        for result in results_data:
            rule_id = result.get("ruleId", "")
            
            # Получаем информацию о правиле
            rule = rules.get(rule_id)
            rule_name = rule.name if rule else rule_id
            level = rule.level if rule else SeverityLevel.NOTE
            
            # Извлекаем сообщение
            message_data = result.get("message", {})
            message = message_data.get("text")
            
            # Парсим локации
            locations = SarifParser._parse_locations(result.get("locations", []))
            
            finding = Finding(
                rule_id=rule_id,
                rule_name=rule_name,
                message=message,
                level=level,
                locations=locations
            )
            
            findings.append(finding)
        
        return findings
    
    @staticmethod
    def _parse_locations(locations_data: List[Dict[str, Any]]) -> List[Location]:
        """Парсить локации"""
        locations = []
        
        for loc_data in locations_data:
            physical_loc = loc_data.get("physicalLocation", {})
            
            # Извлекаем путь к файлу
            artifact_loc = physical_loc.get("artifactLocation", {})
            file_path = artifact_loc.get("uri", "")
            
            # Извлекаем регион (строки, колонки)
            region = physical_loc.get("region", {})
            start_line = region.get("startLine")
            end_line = region.get("endLine")
            start_column = region.get("startColumn")
            end_column = region.get("endColumn")
            
            # Извлекаем фрагмент кода
            snippet_data = region.get("snippet", {})
            snippet = snippet_data.get("text")
            
            location = Location(
                file_path=file_path,
                snippet=snippet,
                start_line=start_line,
                end_line=end_line,
                start_column=start_column,
                end_column=end_column
            )
            
            locations.append(location)
        
        return locations


def print_report_summary(report: SarifReport):
    """Вывести краткую информацию о отчете"""
    print(f"\n{'='*80}")
    print(f"SARIF Отчет: {report.tool.name}")
    if report.tool.version:
        print(f"Версия: {report.tool.version}")
    if report.tool.organization:
        print(f"Организация: {report.tool.organization}")
    print(f"{'='*80}\n")
    
    stats = report.get_statistics()
    
    print(f"Всего находок: {stats['total_findings']}")
    print(f"Всего правил: {stats['total_rules']}\n")
    
    print("Распределение по уровням серьезности:")
    print(f"  🔴 Ошибки (error):    {stats['by_severity']['error']}")
    print(f"  🟡 Предупреждения (warning): {stats['by_severity']['warning']}")
    print(f"  🔵 Заметки (note):     {stats['by_severity']['note']}")
    print(f"  ⚪ Прочие (none):      {stats['by_severity']['none']}\n")
    
    print("Топ-10 правил по количеству находок:")
    sorted_rules = sorted(
        stats['by_rule'].items(), 
        key=lambda x: x[1]['count'], 
        reverse=True
    )
    
    for i, (rule_id, rule_info) in enumerate(sorted_rules[:10], 1):
        level_icon = {
            'error': '🔴',
            'warning': '🟡',
            'note': '🔵',
            'none': '⚪'
        }.get(rule_info['level'], '⚪')
        
        print(f"  {i:2}. {level_icon} [{rule_info['count']:4}] {rule_info['name']}")
        print(f"      ID: {rule_id}")
    
    print(f"\n{'='*80}\n")


def print_detailed_findings(report: SarifReport, max_findings: int = 10):
    """Вывести детальную информацию о находках"""
    print(f"Детальный список находок (первые {max_findings}):\n")
    
    for i, finding in enumerate(report.findings[:max_findings], 1):
        level_icon = {
            SeverityLevel.ERROR: '🔴',
            SeverityLevel.WARNING: '🟡',
            SeverityLevel.NOTE: '🔵',
            SeverityLevel.NONE: '⚪'
        }.get(finding.level, '⚪')
        
        print(f"{i}. {level_icon} {finding.rule_name}")
        print(f"   ID: {finding.rule_id}")
        print(f"   Уровень: {finding.level.value}")
        
        if finding.message:
            print(f"   Сообщение: {finding.message}")
        
        if finding.locations:
            print(f"   Локации ({len(finding.locations)}):")
            for loc in finding.locations[:3]:  # Показываем только первые 3 локации
                print(f"     - {loc.file_path}")
                if loc.start_line:
                    print(f"       Строка: {loc.start_line}")
                if loc.snippet:
                    # Показываем только первые 100 символов сниппета
                    snippet_preview = loc.snippet[:100].replace('\n', ' ')
                    if len(loc.snippet) > 100:
                        snippet_preview += "..."
                    print(f"       Код: {snippet_preview}")
            
            if len(finding.locations) > 3:
                print(f"     ... и еще {len(finding.locations) - 3} локаций")
        
        print()


if __name__ == "__main__":
    # Пример использования
    import sys
    
    if len(sys.argv) < 2:
        print("Использование: python sarif_parser.py <путь_к_sarif_файлу>")
        print("\nПример:")
        print("  python sarif_parser.py report.sarif")
        sys.exit(1)
    
    sarif_file = sys.argv[1]
    
    try:
        print(f"Парсинг файла: {sarif_file}")
        report = SarifParser.parse_file(sarif_file)
        
        print_report_summary(report)
        print_detailed_findings(report)
        
    except FileNotFoundError:
        print(f"❌ Ошибка: Файл '{sarif_file}' не найден")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"❌ Ошибка парсинга JSON: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

