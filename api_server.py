import os
import json
import uuid
import datetime
from pathlib import Path
from typing import Any, Dict, List

from flask import Flask, request, jsonify
from flask_cors import CORS

from sarif_parser import SarifParser, SeverityLevel


APP = Flask(__name__)
CORS(APP)

DATA_DIR = Path("data")
DB_PATH = DATA_DIR / "db.json"


def now_iso() -> str:
    return datetime.datetime.utcnow().isoformat() + "Z"


def load_db() -> Dict[str, Any]:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not DB_PATH.exists():
        return {"projects": []}
    try:
        with DB_PATH.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"projects": []}


def save_db(db: Dict[str, Any]):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    tmp = DB_PATH.with_suffix(".tmp")
    with tmp.open("w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=2)
    tmp.replace(DB_PATH)


def map_severity(level: SeverityLevel) -> str:
    # Map SARIF levels to UI severity classes
    if level == SeverityLevel.ERROR:
        return "high"
    if level == SeverityLevel.WARNING:
        return "medium"
    if level == SeverityLevel.NOTE:
        return "low"
    return "info"


def upsert_project(db: Dict[str, Any], name: str) -> Dict[str, Any]:
    for p in db.get("projects", []):
        if p.get("name") == name:
            return p
    project = {
        "id": str(uuid.uuid4()),
        "name": name,
        "description": "",
        "findings": [],
        "tools": [],
        "updated_at": now_iso(),
    }
    db.setdefault("projects", []).append(project)
    return project


@APP.route("/api/upload", methods=["POST"])
def api_upload():
    # Accept multiple files under key 'file'
    files = request.files.getlist("file")
    project_name = request.form.get("project_name") or request.form.get("project") or "Default Project"

    if not files:
        return jsonify({"error": "No files provided"}), 400

    db = load_db()
    project = upsert_project(db, project_name)

    total_findings = 0
    total_size = 0
    tools: List[str] = []

    for f in files:
        try:
            content = f.read()
            total_size += len(content)
            data = json.loads(content.decode("utf-8"))
            report = SarifParser.parse_dict(data)
        except Exception as e:
            return jsonify({"error": f"Failed to parse {f.filename}: {e}"}), 400

        tool_name = report.tool.name
        if tool_name and tool_name not in tools:
            tools.append(tool_name)

        for finding in report.findings:
            total_findings += 1
            # Choose primary location (first)
            loc = finding.locations[0] if finding.locations else None
            project["findings"].append({
                "severity": map_severity(finding.level),
                "ruleId": finding.rule_id,
                "message": finding.message or finding.rule_name or finding.rule_id,
                "file": loc.file_path if loc else "",
                "tool": tool_name,
                "status": "new",
                "projectName": project["name"],
                "created_at": now_iso(),
            })

        if tool_name and tool_name not in project["tools"]:
            project["tools"].append(tool_name)

    project["updated_at"] = now_iso()
    save_db(db)

    return jsonify({
        "total_files": len(files),
        "total_findings": total_findings,
        "size_mb": round(total_size / (1024 * 1024), 2),
        "tools": tools,
        "projects": [{"id": project["id"], "name": project["name"]}],
    })


@APP.route("/api/projects", methods=["GET"])
def api_projects():
    db = load_db()
    out = []
    for p in db.get("projects", []):
        out.append({
            "id": p.get("id"),
            "name": p.get("name"),
            "description": p.get("description"),
            "total_findings": len(p.get("findings", [])),
            "updated_at": p.get("updated_at"),
        })
    return jsonify(out)


@APP.route("/api/findings", methods=["GET"])
def api_findings():
    db = load_db()
    project_id = request.args.get("project_id")
    findings: List[Dict[str, Any]] = []
    for p in db.get("projects", []):
        if project_id and p.get("id") != project_id:
            continue
        findings.extend(p.get("findings", []))
    # Optional simple sort by severity
    return jsonify(findings)


@APP.route("/api/statistics", methods=["GET"])
def api_statistics():
    db = load_db()
    total_findings = 0
    total_projects = len(db.get("projects", []))
    total_files = 0  # Not tracked per-file yet; could be derived if stored
    by_severity = {"critical": 0, "high": 0, "medium": 0, "low": 0, "info": 0}

    for p in db.get("projects", []):
        for f in p.get("findings", []):
            total_findings += 1
            sev = f.get("severity", "info")
            if sev in by_severity:
                by_severity[sev] += 1

    return jsonify({
        "summary": {
            "total_findings": total_findings,
            "total_projects": total_projects,
            "total_files": total_files,
            "size_mb": None,
        },
        "by_severity": by_severity,
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    APP.run(host="0.0.0.0", port=port, debug=True)


