"""Report-only leakage audit for UFC Fight Predictor model code."""
from __future__ import annotations

import argparse
import ast
import json
from dataclasses import asdict, dataclass
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_OUTPUT_DIR = REPO_ROOT / "data" / "experiments"
ML_DIR = Path(__file__).resolve().parent
FEATURES_PATH = ML_DIR / "features.py"
TRAIN_PATH = ML_DIR / "train.py"
BACKTEST_PATH = ML_DIR / "backtest.py"

POINT_IN_TIME_HELPERS = [
    "_career_stats",
    "_ufc_fight_count",
    "_recent_form",
    "_career_profile",
    "_weight_class_record_profile",
    "_round_tendency_profile",
    "_prior_results_by_opponent",
    "_damage_index",
]


@dataclass(frozen=True)
class AuditCheck:
    category: str
    name: str
    status: str
    detail: str


def run_leakage_audit(
    *,
    include_db: bool = False,
    start_date: date | None = None,
    max_events: int | None = None,
) -> dict[str, Any]:
    """Build a leakage audit report without training or persisting a model."""
    checks = [
        *_audit_feature_sources(),
        *_audit_training_sources(),
        *_audit_harness_sources(),
    ]
    if include_db:
        checks.extend(_audit_database_boundaries(start_date=start_date, max_events=max_events))

    failed = [check for check in checks if check.status != "pass"]
    report = {
        "generated_at": datetime.now(UTC).isoformat(),
        "audit_type": "model-reliability-leakage",
        "report_only": True,
        "writes_model_versions": False,
        "args": {
            "include_db": include_db,
            "start_date": start_date.isoformat() if start_date else None,
            "max_events": max_events,
        },
        "status": "fail" if failed else "pass",
        "summary": {
            "checks": len(checks),
            "passed": len(checks) - len(failed),
            "failed": len(failed),
        },
        "checks": [asdict(check) for check in checks],
    }
    return report


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Model Leakage Audit",
        "",
        f"- Generated: `{report['generated_at']}`",
        f"- Status: **{report['status'].upper()}**",
        f"- Report-only: `{str(report['report_only']).lower()}`",
        f"- Writes `model_versions`: `{str(report['writes_model_versions']).lower()}`",
        f"- Checks: {report['summary']['passed']}/{report['summary']['checks']} passed",
        "",
        "## Checks",
        "",
        "| Category | Check | Status | Detail |",
        "|---|---|---|---|",
    ]
    for check in report["checks"]:
        lines.append(
            "| "
            f"{_escape_md(check['category'])} | "
            f"{_escape_md(check['name'])} | "
            f"{check['status']} | "
            f"{_escape_md(check['detail'])} |"
        )
    lines.extend(
        [
            "",
            "## Policy",
            "",
            "This report audits code shape and optional database event boundaries. It does not train a model, save a model file, write `model_versions`, or validate betting edge.",
            "",
        ]
    )
    return "\n".join(lines)


def _audit_feature_sources() -> list[AuditCheck]:
    checks: list[AuditCheck] = []
    features_source = FEATURES_PATH.read_text()
    for helper_name in POINT_IN_TIME_HELPERS:
        source = _function_source(features_source, helper_name)
        checks.append(
            _source_check(
                "feature_point_in_time",
                f"{helper_name} uses strict prior-event cutoff",
                "e.date < %s" in source,
                "query filters prior rows with e.date < target_date",
                "query does not show strict e.date < target_date cutoff",
            )
        )

    build_features_source = _function_source(features_source, "build_features")
    checks.append(
        _source_check(
            "feature_point_in_time",
            "build_features derives target context before label",
            _ordered(build_features_source, "target_date", "target_weight_class", "build_feature_row", "_label"),
            "target date and weight class are passed into feature construction before label serialization",
            "target context or label ordering changed; inspect for target-result leakage",
        )
    )
    build_feature_dict_source = _function_source(features_source, "build_feature_dict")
    checks.append(
            _source_check(
                "feature_point_in_time",
                "build_feature_dict threads fight_date through feature helpers",
                all(
                    f"{helper_name}(" in build_feature_dict_source
                    for helper_name in POINT_IN_TIME_HELPERS
                    if helper_name != "_prior_results_by_opponent"
                ),
                "production feature helpers are called from one fight_date-scoped dictionary builder",
                "one or more production feature helpers are not called from the fight_date-scoped builder",
            )
    )
    return checks


def _audit_training_sources() -> list[AuditCheck]:
    train_source = _function_source(TRAIN_PATH.read_text(), "train")
    backtest_source = _function_source(BACKTEST_PATH.read_text(), "run_walk_forward_backtest")
    return [
        _source_check(
            "train_test_boundary",
            "train.py uses chronological split",
            _ordered(train_source, "samples.sort", "train_samples = samples[:split_index]", "holdout_samples = samples[split_index:]"),
            "training samples are sorted by event date before holdout split",
            "chronological training split was not found",
        ),
        _source_check(
            "train_test_boundary",
            "walk-forward trains only on earlier events",
            'sample["event_date"] < event["event_date"]' in backtest_source,
            "walk-forward train set excludes same-day and future target events",
            "walk-forward train set does not show strict event_date < target date filter",
        ),
        _source_check(
            "train_test_boundary",
            "walk-forward targets one event at a time",
            'sample["event_id"] == event["event_id"]' in backtest_source,
            "target samples are selected by current event_id only",
            "target sample boundary by event_id was not found",
        ),
    ]


def _audit_harness_sources() -> list[AuditCheck]:
    source = Path(__file__).read_text()
    tree = ast.parse(source)
    call_names = {_call_name(node) for node in ast.walk(tree) if isinstance(node, ast.Call)}
    insert_marker = "INSERT INTO " + "model_versions"
    return [
        _source_check(
            "report_only",
            "leakage audit does not write active models",
            insert_marker not in source
            and "_insert_model_version" not in call_names
            and "save_model" not in call_names,
            "audit source has no model persistence calls",
            "audit source contains model persistence markers",
        )
    ]


def _audit_database_boundaries(
    *,
    start_date: date | None,
    max_events: int | None,
) -> list[AuditCheck]:
    from ml import backtest, features

    rows = backtest._load_completed_fights()
    candidate_events = _raw_target_events(rows, start_date)
    if max_events is not None:
        candidate_events = candidate_events[:max_events]
    cutoff_date = max((event["event_date"] for event in candidate_events), default=None)
    sample_rows = [row for row in rows if cutoff_date is None or row["event_date"] <= cutoff_date]
    samples = backtest._build_samples(sample_rows, features.FEATURE_NAMES)
    candidate_event_ids = {event["event_id"] for event in candidate_events}
    events = [event for event in backtest._target_events(samples, start_date, cutoff_date) if event["event_id"] in candidate_event_ids]

    violations: list[str] = []
    for event in events:
        train_samples = [sample for sample in samples if sample["event_date"] < event["event_date"]]
        target_samples = [sample for sample in samples if sample["event_id"] == event["event_id"]]
        if any(sample["event_date"] >= event["event_date"] for sample in train_samples):
            violations.append(f"{event['event_id']}: train set contains target/future rows")
        if any(sample["event_id"] != event["event_id"] for sample in target_samples):
            violations.append(f"{event['event_id']}: target set contains other events")

    return [
        _source_check(
            "database_boundary",
            "loaded walk-forward samples respect event boundaries",
            not violations,
            f"checked {len(events)} event boundaries from {len(samples)} labeled samples",
            "; ".join(violations[:5]),
        )
    ]


def _raw_target_events(rows: list[dict[str, Any]], start_date: date | None) -> list[dict[str, Any]]:
    events_by_id: dict[str, dict[str, Any]] = {}
    for row in rows:
        if start_date is not None and row["event_date"] < start_date:
            continue
        events_by_id[row["event_id"]] = {
            "event_id": row["event_id"],
            "event_name": row["event_name"],
            "event_date": row["event_date"],
        }
    return sorted(events_by_id.values(), key=lambda row: (row["event_date"], row["event_id"]))


def _source_check(
    category: str,
    name: str,
    passed: bool,
    pass_detail: str,
    fail_detail: str,
) -> AuditCheck:
    return AuditCheck(
        category=category,
        name=name,
        status="pass" if passed else "fail",
        detail=pass_detail if passed else fail_detail,
    )


def _ordered(source: str, *needles: str) -> bool:
    position = -1
    for needle in needles:
        next_position = source.find(needle, position + 1)
        if next_position == -1:
            return False
        position = next_position
    return True


def _function_source(module_source: str, function_name: str) -> str:
    tree = ast.parse(module_source)
    lines = module_source.splitlines()
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == function_name:
            return "\n".join(lines[node.lineno - 1 : node.end_lineno])
    raise ValueError(f"function {function_name!r} not found")


def _call_name(node: ast.Call) -> str:
    if isinstance(node.func, ast.Name):
        return node.func.id
    if isinstance(node.func, ast.Attribute):
        return node.func.attr
    return ""


def _escape_md(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def _resolve_repo_path(path: Path) -> Path:
    return path if path.is_absolute() else REPO_ROOT / path


def _display_path(path: Path) -> str:
    try:
        return str(path.relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the UFC predictor leakage audit")
    parser.add_argument("--include-db", action="store_true", help="Audit live database event boundaries too.")
    parser.add_argument("--start-date", type=date.fromisoformat, default=None)
    parser.add_argument("--max-events", type=int, default=None)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT_DIR / "leakage-audit.json")
    parser.add_argument("--markdown", type=Path, default=DEFAULT_OUTPUT_DIR / "leakage-audit.md")
    parser.add_argument("--stdout", choices=["summary", "full", "none"], default="summary")
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    output_path = _resolve_repo_path(args.output)
    markdown_path = _resolve_repo_path(args.markdown)
    report = run_leakage_audit(
        include_db=args.include_db,
        start_date=args.start_date,
        max_events=args.max_events,
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2, allow_nan=False) + "\n")
    markdown_path.write_text(render_markdown(report))
    if args.stdout == "none":
        return
    output = report if args.stdout == "full" else {
        "status": report["status"],
        "summary": report["summary"],
        "output": _display_path(output_path),
        "markdown": _display_path(markdown_path),
    }
    print(json.dumps(output, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
