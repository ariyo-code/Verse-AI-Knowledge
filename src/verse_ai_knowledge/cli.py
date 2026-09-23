from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

from .api_index import lookup
from .policy import repo_root


def run_script(root: Path, rel: str, args: list[str]) -> int:
    cmd = [sys.executable, str(root / rel), *args]
    proc = subprocess.run(cmd)
    return proc.returncode


def cmd_api(root: Path, symbol: str) -> int:
    row, suggestions = lookup(symbol, root)
    if row:
        print(json.dumps(row, indent=2, ensure_ascii=False))
        if row.get("signature") and not row.get("exact_signature_claim_allowed"):
            print("\nWARNING: a legacy signature string exists, but exact signature evidence is insufficient.")
            print("Use TODO(API VERIFY) before presenting that exact signature as certain.")
        return 0
    print(f"No exact structured API match for: {symbol}")
    if suggestions:
        print("Closest entries:")
        for item in suggestions:
            print("-", item)
    print("TODO(API VERIFY)")
    return 2


def cmd_doctor(root: Path) -> int:
    manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
    checks = {
        "schema_22": manifest.get("schema_version") == 22,
        "bootstrap": (root / "AI_BOOTSTRAP.md").exists(),
        "symbol_index": (root / "knowledge/api/symbols.jsonl").exists(),
        "trust_schema": (root / "schemas/trust.schema.json").exists(),
        "validation_schema": (root / "schemas/validation_status.schema.json").exists(),
        "ci": (root / ".github/workflows/ci.yml").exists(),
    }
    print("Verse AI Knowledge doctor")
    print("Repository:", root)
    print("Release:", manifest.get("release", {}).get("version", "unknown"))
    for name, ok in checks.items():
        print(f"[{'PASS' if ok else 'FAIL'}] {name}")
    print("UEFN compile status: NOT TESTED by doctor")
    return 0 if all(checks.values()) else 1


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="verse-ai", description="Verse AI Knowledge V22 CLI")
    sub = p.add_subparsers(dest="cmd", required=True)

    q = sub.add_parser("search")
    q.add_argument("query")
    q.add_argument("--limit", type=int, default=12)
    q.add_argument("--json", action="store_true")

    c = sub.add_parser("context")
    c.add_argument("query")
    c.add_argument("--budget", type=int, default=18000)
    c.add_argument("--output", default="rag/generated/CONTEXT.md")

    a = sub.add_parser("api")
    a.add_argument("symbol")

    e = sub.add_parser("errors")
    e.add_argument("query")
    e.add_argument("--limit", type=int, default=10)

    project = sub.add_parser("project")
    psub = project.add_subparsers(dest="project_cmd", required=True)
    scan = psub.add_parser("scan")
    scan.add_argument("project_root")
    scan.add_argument("--output", default="project_scan.json")

    verify = sub.add_parser("verify")
    verify.add_argument("path")

    lab = sub.add_parser("lab")
    lsub = lab.add_subparsers(dest="lab_cmd", required=True)
    lsub.add_parser("next")
    lsub.add_parser("status")

    maintenance = sub.add_parser("maintenance")
    msub = maintenance.add_subparsers(dest="maintenance_cmd", required=True)
    msub.add_parser("check")

    sub.add_parser("doctor")
    sub.add_parser("validate")
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = repo_root()

    if args.cmd == "search":
        extra = [args.query, "--limit", str(args.limit)]
        if args.json:
            extra.append("--json")
        return run_script(root, "tools/rag_query.py", extra)
    if args.cmd == "context":
        return run_script(root, "tools/rag_context_pack.py", [args.query, "--budget", str(args.budget), "--output", args.output])
    if args.cmd == "api":
        return cmd_api(root, args.symbol)
    if args.cmd == "errors":
        return run_script(root, "tools/search_errors.py", [args.query, "--limit", str(args.limit)])
    if args.cmd == "project" and args.project_cmd == "scan":
        return run_script(root, "tools/scan_verse_project.py", [args.project_root, "--output", args.output])
    if args.cmd == "verify":
        return run_script(root, "tools/check_api_references.py", [args.path])
    if args.cmd == "lab" and args.lab_cmd == "next":
        return run_script(root, "tools/compile_queue.py", ["next"])
    if args.cmd == "lab" and args.lab_cmd == "status":
        return run_script(root, "tools/verselab_status.py", [])
    if args.cmd == "maintenance" and args.maintenance_cmd == "check":
        return run_script(root, "tools/revalidation_report.py", [])
    if args.cmd == "doctor":
        return cmd_doctor(root)
    if args.cmd == "validate":
        for rel in ["tools/validate_v22_integrity.py", "tools/check_generated_drift.py", "tools/self_test.py"]:
            rc = run_script(root, rel, [])
            if rc:
                return rc
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
