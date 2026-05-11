"""Summarize saved UFC Fight Predictor backtest reports."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_REPORT_DIR = REPO_ROOT / "data" / "backtests"


def summarize_reports(paths: list[Path] | None = None) -> list[dict[str, Any]]:
    report_paths = paths or sorted(DEFAULT_REPORT_DIR.glob("*.json"))
    summaries = []
    for path in report_paths:
        report = json.loads(path.read_text())
        summaries.append(
            {
                "file": str(path.relative_to(REPO_ROOT) if path.is_relative_to(REPO_ROOT) else path),
                "generated_at": report.get("generated_at"),
                "start_date": report.get("start_date"),
                "events_scored": report.get("events_scored"),
                "predictions_scored": report.get("predictions_scored"),
                "accuracy": _metric(report, "accuracy"),
                "avg_confidence": _metric(report, "avg_confidence"),
                "calibration_gap": _metric(report, "calibration_gap"),
                "abs_calibration_error": _metric(report, "abs_calibration_error"),
                "log_loss": _metric(report, "log_loss"),
                "brier_score": _metric(report, "brier_score"),
                "roc_auc": _metric(report, "roc_auc"),
                "confidence_buckets": _bucket_summary(report.get("by_confidence_bucket")),
                "model_edge_buckets": _bucket_summary(report.get("by_model_edge_bucket")),
            }
        )
    return summaries


def _metric(report: dict[str, Any], key: str) -> float | None:
    overall = report.get("overall")
    if not isinstance(overall, dict):
        return None
    value = overall.get(key)
    return float(value) if isinstance(value, int | float) else None


def _bucket_summary(value: Any) -> list[dict[str, Any]]:
    if not isinstance(value, dict):
        return []
    return [
        {
            "bucket": bucket,
            "count": metrics.get("count"),
            "accuracy": metrics.get("accuracy"),
            "avg_confidence": metrics.get("avg_confidence"),
            "calibration_gap": metrics.get("calibration_gap"),
            "abs_calibration_error": metrics.get("abs_calibration_error"),
            "log_loss": metrics.get("log_loss"),
            "brier_score": metrics.get("brier_score"),
            "roc_auc": metrics.get("roc_auc"),
        }
        for bucket, metrics in value.items()
        if isinstance(metrics, dict)
    ]


def render_markdown(summaries: list[dict[str, Any]]) -> str:
    lines = [
        "| Report | Events | Predictions | Accuracy | Avg confidence | Calibration gap | Abs calibration error | Log loss | Brier | ROC AUC |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for summary in summaries:
        lines.append(
            "| {file} | {events} | {predictions} | {accuracy} | {avg_confidence} | {calibration_gap} | {abs_calibration_error} | {log_loss} | {brier} | {roc_auc} |".format(
                file=summary["file"],
                events=summary["events_scored"],
                predictions=summary["predictions_scored"],
                accuracy=_format_metric(summary["accuracy"]),
                avg_confidence=_format_metric(summary["avg_confidence"]),
                calibration_gap=_format_signed_metric(summary["calibration_gap"]),
                abs_calibration_error=_format_metric(summary["abs_calibration_error"]),
                log_loss=_format_metric(summary["log_loss"]),
                brier=_format_metric(summary["brier_score"]),
                roc_auc=_format_metric(summary["roc_auc"]),
            )
        )
        lines.extend(_render_bucket_table("Confidence Buckets", summary["confidence_buckets"]))
        lines.extend(_render_bucket_table("Model Edge Buckets", summary["model_edge_buckets"]))
    return "\n".join(lines)


def _render_bucket_table(title: str, buckets: list[dict[str, Any]]) -> list[str]:
    if not buckets:
        return []
    lines = [
        "",
        f"### {title}",
        "",
        "| Bucket | Count | Accuracy | Avg confidence | Calibration gap | Abs calibration error | Log loss | Brier | ROC AUC |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for bucket in sorted(buckets, key=lambda row: _bucket_sort_key(str(row["bucket"]))):
        lines.append(
            "| {bucket} | {count} | {accuracy} | {avg_confidence} | {calibration_gap} | {abs_calibration_error} | {log_loss} | {brier} | {roc_auc} |".format(
                bucket=bucket["bucket"],
                count=bucket["count"],
                accuracy=_format_metric(bucket["accuracy"]),
                avg_confidence=_format_metric(bucket["avg_confidence"]),
                calibration_gap=_format_signed_metric(bucket["calibration_gap"]),
                abs_calibration_error=_format_metric(bucket["abs_calibration_error"]),
                log_loss=_format_metric(bucket["log_loss"]),
                brier=_format_metric(bucket["brier_score"]),
                roc_auc=_format_metric(bucket["roc_auc"]),
            )
        )
    return lines


def _bucket_sort_key(bucket: str) -> tuple[int, str]:
    try:
        return (int(bucket.split("-", maxsplit=1)[0].removesuffix("+")), bucket)
    except ValueError:
        return (999, bucket)


def _format_metric(value: Any) -> str:
    if value is None:
        return ""
    return f"{float(value):.4f}"


def _format_signed_metric(value: Any) -> str:
    if value is None:
        return ""
    return f"{float(value):+.4f}"


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Summarize saved walk-forward backtest reports")
    parser.add_argument("reports", nargs="*", type=Path)
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    parser.add_argument("--output", type=Path, default=None)
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    paths = [path if path.is_absolute() else REPO_ROOT / path for path in args.reports]
    summaries = summarize_reports(paths or None)
    if args.format == "json":
        output = json.dumps(summaries, indent=2, allow_nan=False) + "\n"
    else:
        output = render_markdown(summaries) + "\n"

    if args.output is not None:
        output_path = args.output if args.output.is_absolute() else REPO_ROOT / args.output
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(output)
        return
    print(output, end="")


if __name__ == "__main__":
    main()
