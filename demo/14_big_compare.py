"""Large-scale clone detection test — 50+ line functions with complex structure."""

import csv
import io
from datetime import datetime, timedelta
from collections import defaultdict


def generate_monthly_report_standard(data, start_date, end_date):
    """Generate a monthly sales report grouped by category."""
    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(["category", "total_sales", "order_count", "avg_value", "top_product"])
    period_data = [r for r in data if start_date <= r.date <= end_date]
    grouped = defaultdict(lambda: {"sales": 0, "count": 0, "products": defaultdict(int)})
    for record in period_data:
        g = grouped[record.category]
        g["sales"] += record.amount
        g["count"] += 1
        g["products"][record.product] += record.quantity
    for cat, stats in sorted(grouped.items()):
        top_product = max(stats["products"], key=stats["products"].get)
        avg = stats["sales"] / stats["count"] if stats["count"] else 0
        writer.writerow([cat, round(stats["sales"], 2), stats["count"], round(avg, 2), top_product])
    report = buffer.getvalue()
    buffer.close()
    return report


def generate_weekly_report_standard(data, start_date, end_date):
    """Generate a weekly inventory report grouped by warehouse."""
    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(["warehouse", "total_value", "item_count", "avg_cost", "top_item"])
    period_data = [r for r in data if start_date <= r.date <= end_date]
    grouped = defaultdict(lambda: {"value": 0, "count": 0, "items": defaultdict(int)})
    for record in period_data:
        g = grouped[record.warehouse]
        g["value"] += record.cost * record.quantity
        g["count"] += 1
        g["items"][record.sku] += record.quantity
    for wh, stats in sorted(grouped.items()):
        top_item = max(stats["items"], key=stats["items"].get)
        avg = stats["value"] / stats["count"] if stats["count"] else 0
        writer.writerow([wh, round(stats["value"], 2), stats["count"], round(avg, 2), top_item])
    report = buffer.getvalue()
    buffer.close()
    return report


class DataPipelineV1:
    """A complex ETL pipeline — unique structure, no duplicates."""

    def __init__(self, source, transforms=None):
        self.source = source
        self.transforms = transforms or []
        self.state = {"processed": 0, "errors": 0, "skipped": 0}

    def run(self):
        raw = self._extract()
        cleaned = self._clean(raw)
        for transform in self.transforms:
            cleaned = transform(cleaned)
        self._load(cleaned)
        return self.state

    def _extract(self):
        with open(self.source) as f:
            return [json.loads(line) for line in f if line.strip()]

    def _clean(self, rows):
        valid = []
        for row in rows:
            try:
                row = {k: v.strip() if isinstance(v, str) else v for k, v in row.items()}
                if all(k in row for k in ("id", "type", "timestamp")):
                    valid.append(row)
                    self.state["processed"] += 1
                else:
                    self.state["skipped"] += 1
            except Exception:
                self.state["errors"] += 1
        return valid

    def _load(self, data):
        pass


class DataPipelineV2:
    """Another ETL pipeline — structurally similar to V1? Test finds out."""

    def __init__(self, config):
        self.input_path = config.get("input")
        self.output_path = config.get("output")
        self.filters = config.get("filters", [])
        self.metrics = {"total": 0, "failures": 0, "omissions": 0}

    def execute(self):
        records = self._read()
        filtered = self._filter(records)
        for fn in self.filters:
            filtered = fn(filtered)
        self._write(filtered)
        return self.metrics

    def _read(self):
        with open(self.input_path) as f:
            return [json.loads(line) for line in f if line.strip()]

    def _filter(self, records):
        good = []
        for rec in records:
            try:
                rec = {k: v.strip() if isinstance(v, str) else v for k, v in rec.items()}
                if "id" in rec and "type" in rec:
                    good.append(rec)
                    self.metrics["total"] += 1
                else:
                    self.metrics["omissions"] += 1
            except Exception:
                self.metrics["failures"] += 1
        return good

    def _write(self, data):
        pass
