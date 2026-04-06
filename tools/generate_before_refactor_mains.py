"""
One-off generator for medium/large before_refactor/main.py (code-smell demos).
Run from repo root: python tools/generate_before_refactor_mains.py
"""
from __future__ import annotations

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

DEAD_IMPORTS_MEDIUM = """
import hashlib
import ftplib
import smtplib
import tarfile
import pickle
import wave
"""

DEAD_IMPORTS_LARGE = DEAD_IMPORTS_MEDIUM + """
import colorsys
import imaplib
import struct
import binascii
from html.parser import HTMLParser
import base64
"""


def _stub_methods(prefix: str, count: int, start: int = 0) -> list[str]:
    out: list[str] = []
    for i in range(start, start + count):
        n = i
        out.append(f"    def {prefix}_operation_{n}(self, payload=None, acc={{}}):")
        out.append("        \"\"\"Stub operation — part of god class surface.\"\"\"")
        out.append("        if payload is None:")
        out.append("            payload = {}")
        out.append(f"        acc['op_{n}'] = True")
        out.append("        temp_unused = acc.copy()")
        out.append("        return temp_unused")
        out.append("")
    return out


def _unused_helpers_medium() -> list[str]:
    lines: list[str] = []
    for i in range(10):
        lines.append(f"    def _unused_helper_medium_{i}(self, x):")
        lines.append("        y = x + 1")
        lines.append("        return y * 2")
        lines.append("")
    return lines


def _unused_helpers_large() -> list[str]:
    lines: list[str] = []
    for i in range(16):
        lines.append(f"    def _unused_helper_large_{i}(self, x):")
        lines.append("        y = x + 1")
        lines.append("        return y * 2")
        lines.append("")
    return lines


def write_medium() -> None:
    path = ROOT / "medium_project" / "before_refactor" / "main.py"
    path.parent.mkdir(parents=True, exist_ok=True)
    lines: list[str] = []
    lines.append('"""Analytics Pipeline — before refactor (intentional smells). Stdlib only."""')
    lines.append("import csv")
    lines.append("import io")
    lines.append("import math")
    lines.append("import random")
    lines.append("import statistics")
    lines.extend(DEAD_IMPORTS_MEDIUM.strip().splitlines())
    lines.append("from datetime import datetime, timedelta")
    lines.append("")
    lines.append("")
    lines.append("class DataManager:")
    lines.append("    \"\"\"God class: 50+ methods, mixed responsibilities.\"\"\"")
    lines.append("")
    lines.append("    def __init__(self):")
    lines.append("        self.unused_attr_1 = True")
    lines.append("        self.unused_attr_2 = 0")
    lines.append("        self._logs = []")
    lines.append("        self._cache = {}")
    lines.append("        random.seed(42)")
    lines.append("        self._build_synthetic_universe()")
    lines.append("")
    lines.append("    def _unreachable_tail(self):")
    lines.append("        return 1")
    lines.append("        x = 2")
    lines.append("        return x")
    lines.append("")
    lines.extend(_unused_helpers_medium())
    lines.extend(_stub_methods("dm", 85))
    # --- mutable defaults (11) — match teaching examples (lists / dicts as defaults) ---
    lines.append("    def add_sales_record(self, data, records=[], audit_log=[]):")
    lines.append("        records.append(data)")
    lines.append("        return records, audit_log")
    lines.append("")
    lines.append("    def process_sales_batch(self, items, results={}, errors=[]):")
    lines.append("        errors.append(items)")
    lines.append("        return results, errors")
    lines.append("")
    lines.append("    def build_sales_report(self, sections=[], config={}, metadata={}):")
    lines.append("        sections.append('section')")
    lines.append("        return sections, config, metadata")
    lines.append("")
    lines.append("    def update_inventory_cache(self, entries, cache={}, errors=[]):")
    lines.append("        cache['last'] = entries")
    lines.append("        return cache, errors")
    lines.append("")
    lines.append("    def accumulate_customer_data(self, batch, accumulated=[], stats={}):")
    lines.append("        accumulated.append(batch)")
    lines.append("        return accumulated, stats")
    lines.append("")
    lines.append("    def collect_validation_errors(self, record, field_errors=[], summary={}):")
    lines.append("        field_errors.append(record)")
    lines.append("        return field_errors, summary")
    lines.append("")
    lines.append("    def aggregate_product_metrics(self, products, metrics={}, tags=[]):")
    lines.append("        metrics['n'] = len(str(products))")
    lines.append("        return metrics, tags")
    lines.append("")
    lines.append("    def build_supplier_scorecard(self, suppliers, scorecard=[], weights={}):")
    lines.append("        scorecard.append(suppliers)")
    lines.append("        return scorecard, weights")
    lines.append("")
    lines.append("    def compute_kpi_dashboard(self, kpis=[], thresholds={}, alerts=[]):")
    lines.append("        alerts.append('tick')")
    lines.append("        return kpis, thresholds, alerts")
    lines.append("")
    lines.append("    def append_audit_trail(self, event, trail=[], session_meta={}):")
    lines.append("        trail.append(event)")
    lines.append("        return trail, session_meta")
    lines.append("")
    lines.append('    def merge_config(self, overrides, base_config={"debug": False, "log_level": "INFO"}):')
    lines.append("        base_config.update(overrides)")
    lines.append("        return base_config")
    lines.append("")
    # duplicated entity processors (8)
    entities = [
        ("sales", "sale_id", ["quantity", "price", "region"], "amount", "lambda r: float(r['quantity'])*float(r['price'])"),
        ("inventory", "item_id", ["stock", "warehouse"], "stock", "lambda r: float(r['stock'])"),
        ("customers", "customer_id", ["region", "lifetime_value"], "lifetime_value", "lambda r: float(r['lifetime_value'])"),
        ("products", "product_id", ["unit_cost", "category"], "unit_cost", "lambda r: float(r['unit_cost'])"),
        ("suppliers", "supplier_id", ["rating", "region"], "rating", "lambda r: float(r['rating'])"),
        ("returns", "return_id", ["amount", "reason"], "amount", "lambda r: float(r['amount'])"),
        ("orders", "order_id", ["total", "status"], "total", "lambda r: float(r['total'])"),
        ("shipments", "shipment_id", ["weight", "carrier"], "weight", "lambda r: float(r['weight'])"),
    ]
    for ent, pk, fields, metric, _ in entities:
        lines.append(f"    def _validate_{ent}_dup(self, records):")
        lines.append("        valid = []")
        lines.append("        for rec in records:")
        lines.append(f"            if not rec.get('{pk}'):")
        lines.append("                continue")
        for f in fields:
            if f in ("quantity", "price", "stock", "lifetime_value", "unit_cost", "rating", "amount", "total", "weight"):
                lines.append("            try:")
                lines.append(f"                if float(rec.get('{f}', 0) or 0) < 0:")
                lines.append("                    continue")
                lines.append("            except (TypeError, ValueError):")
                lines.append("                continue")
            elif f in ("region", "warehouse", "category", "reason", "status", "carrier"):
                lines.append(f"            if not rec.get('{f}'):")
                lines.append("                continue")
        lines.append("            valid.append(rec)")
        lines.append("        return valid")
        lines.append("")
        lines.append(f"    def _stats_dup_{ent}(self, values):")
        lines.append("        if not values:")
        lines.append("            return {'mean':0.0,'std':0.0,'median':0.0,'min':0.0,'max':0.0}")
        lines.append("        mean_v = sum(values)/len(values)")
        lines.append("        var = sum((x-mean_v)**2 for x in values)/len(values)")
        lines.append("        std_v = math.sqrt(var)")
        lines.append("        s = sorted(values)")
        lines.append("        mid = len(s)//2")
        lines.append("        med = s[mid] if len(s)%2 else (s[mid-1]+s[mid])/2")
        lines.append("        return {'mean':mean_v,'std':std_v,'median':med,'min':min(values),'max':max(values)}")
        lines.append("")
        lines.append(f"    def _csv_dup_{ent}(self, text):")
        lines.append("        out = []")
        lines.append("        for row in csv.DictReader(io.StringIO(text)):")
        lines.append("            out.append(dict(row))")
        lines.append("        return out")
        lines.append("")
    # data builder inside class as big method
    lines.append("    def _build_synthetic_universe(self):")
    lines.append("        regions = ['EU','NA','LATAM','APAC']")
    lines.append("        base = datetime(2023,1,1)")
    lines.append("        self.products = []")
    lines.append("        for i in range(2000):")
    lines.append("            self.products.append({")
    lines.append("                'product_id': f'P{i:05d}',")
    lines.append("                'category': random.choice(['A','B','C','D']),")
    lines.append("                'unit_cost': round(random.uniform(2,120),2),")
    lines.append("            })")
    lines.append("        self.customers = []")
    lines.append("        for i in range(3000):")
    lines.append("            self.customers.append({")
    lines.append("                'customer_id': f'C{i:05d}',")
    lines.append("                'region': random.choice(regions),")
    lines.append("                'lifetime_value': round(random.uniform(50,8000),2),")
    lines.append("            })")
    lines.append("        self.suppliers = []")
    lines.append("        for i in range(500):")
    lines.append("            self.suppliers.append({")
    lines.append("                'supplier_id': f'U{i:04d}',")
    lines.append("                'region': random.choice(regions),")
    lines.append("                'rating': round(random.uniform(1,5),2),")
    lines.append("            })")
    lines.append("        self.inventory = []")
    lines.append("        for i in range(5000):")
    lines.append("            self.inventory.append({")
    lines.append("                'item_id': f'I{i:05d}',")
    lines.append("                'stock': random.randint(0,800),")
    lines.append("                'warehouse': random.choice(['W1','W2','W3','W4']),")
    lines.append("            })")
    lines.append("        self.sales = []")
    lines.append("        for i in range(10000):")
    lines.append("            p = random.choice(self.products)")
    lines.append("            c = random.choice(self.customers)")
    lines.append("            self.sales.append({")
    lines.append("                'sale_id': f'S{i:05d}',")
    lines.append("                'customer_id': c['customer_id'],")
    lines.append("                'product_id': p['product_id'],")
    lines.append("                'quantity': random.randint(1,25),")
    lines.append("                'price': round(random.uniform(5,250),2),")
    lines.append("                'region': c['region'],")
    lines.append("                'sale_date': (base+timedelta(days=random.randint(0,500))).strftime('%Y-%m-%d'),")
    lines.append("            })")
    lines.append("        self.returns = []")
    lines.append("        for i in range(1500):")
    lines.append("            self.returns.append({")
    lines.append("                'return_id': f'R{i:05d}',")
    lines.append("                'amount': round(random.uniform(10,500),2),")
    lines.append("                'reason': random.choice(['defect','changed_mind','other']),")
    lines.append("            })")
    lines.append("        self.orders = []")
    lines.append("        for i in range(4000):")
    lines.append("            self.orders.append({")
    lines.append("                'order_id': f'O{i:05d}',")
    lines.append("                'total': round(random.uniform(20,2000),2),")
    lines.append("                'status': random.choice(['open','shipped','closed']),")
    lines.append("            })")
    lines.append("        self.shipments = []")
    lines.append("        for i in range(3000):")
    lines.append("            self.shipments.append({")
    lines.append("                'shipment_id': f'H{i:05d}',")
    lines.append("                'weight': round(random.uniform(0.5,200),2),")
    lines.append("                'carrier': random.choice(['ACME','FAST','GLOBAL']),")
    lines.append("            })")
    lines.append("")
    # long methods
    lines.extend(_long_method_process_sales_medium())
    lines.extend(_long_method_report_medium())
    lines.extend(_long_method_inventory_medium())
    lines.extend(_run_all_analyses_medium())
    lines.append("")
    lines.append("")
    lines.append("def main():")
    lines.append("    manager = DataManager()")
    lines.append("    manager.process_all_sales_data()")
    lines.append("    manager.generate_complete_report()")
    lines.append("    manager.run_full_inventory_analysis()")
    lines.append("    manager.run_all_analyses()")
    lines.append("")
    lines.append("")
    lines.append('if __name__ == "__main__":')
    lines.append("    main()")
    lines.append("")
    lines.append("# legacy_export_v0 = None")
    text = "\n".join(lines) + "\n"
    path.write_text(text, encoding="utf-8")
    print(f"Wrote {path} ({len(text.splitlines())} lines)")


def _long_method_process_sales_medium() -> list[str]:
    body: list[str] = []
    body.append("    def process_all_sales_data(self):")
    body.append('        """Long method: full sales pipeline inline (200+ lines)."""')
    body.append("        self._logs.append('sales_start')")
    body.append("        buf = io.StringIO()")
    body.append("        w = csv.DictWriter(buf, fieldnames=list(self.sales[0].keys()))")
    body.append("        w.writeheader()")
    body.append("        for row in self.sales:")
    body.append("            w.writerow(row)")
    body.append("        raw = self._csv_dup_sales(buf.getvalue())")
    body.append("        vs = self._validate_sales_dup(raw)")
    body.append("        passes = 3")
    body.append("        self._sales_pass_outputs = []")
    body.append("        for pass_idx in range(passes):")
    body.append("            region_totals = {'EU':0.0,'NA':0.0,'LATAM':0.0,'APAC':0.0}")
    body.append("            amounts = []")
    body.append("            for rec in vs:")
    body.append("                q = float(rec['quantity']); p = float(rec['price'])")
    body.append("                amounts.append(q*p)")
    body.append("                region_totals[rec['region']] = region_totals.get(rec['region'],0.0)+q*p")
    body.append("            st = self._stats_dup_sales(amounts)")
    body.append("            top = sorted([{'sale_id':r['sale_id'],'amt':float(r['quantity'])*float(r['price'])} for r in vs], key=lambda x:x['amt'], reverse=True)[:15]")
    body.append("            self._sales_pass_outputs.append({'pass':pass_idx,'stats':st,'region_totals':region_totals,'top':top})")
    body.append("        self._cache['sales'] = self._sales_pass_outputs")
    body.append("        self._logs.append('sales_end')")
    body.append("        return self._sales_pass_outputs")
    # pad with unreachable + repeated no-op blocks
    for i in range(350):
        body.append(f"        _pad_{i} = {i}")
        body.append(f"        if _pad_{i} < 0:")
        body.append("            return None")
    body.append("")
    return body


def _long_method_report_medium() -> list[str]:
    body: list[str] = []
    body.append("    def generate_complete_report(self):")
    body.append('        """Long method: cross-entity report (200+ lines)."""')
    body.append("        self._logs.append('report_start')")
    body.append("        chunks = []")
    body.append("        for ent in ['customers','products','suppliers','returns','orders','shipments']:")
    body.append("            buf = io.StringIO()")
    body.append("            rows = getattr(self, ent)")
    body.append("            if not rows:")
    body.append("                continue")
    body.append("            w = csv.DictWriter(buf, fieldnames=list(rows[0].keys()))")
    body.append("            w.writeheader()")
    body.append("            for row in rows:")
    body.append("                w.writerow(row)")
    body.append("            fn = getattr(self, f'_csv_dup_{ent}')")
    body.append("            parsed = fn(buf.getvalue())")
    body.append("            fnv = getattr(self, f'_validate_{ent}_dup')")
    body.append("            valid = fnv(parsed)")
    body.append("            if ent == 'customers':")
    body.append("                vals = [float(r['lifetime_value']) for r in valid]")
    body.append("            elif ent == 'products':")
    body.append("                vals = [float(r['unit_cost']) for r in valid]")
    body.append("            elif ent == 'suppliers':")
    body.append("                vals = [float(r['rating']) for r in valid]")
    body.append("            elif ent == 'returns':")
    body.append("                vals = [float(r['amount']) for r in valid]")
    body.append("            elif ent == 'orders':")
    body.append("                vals = [float(r['total']) for r in valid]")
    body.append("            else:")
    body.append("                vals = [float(r['weight']) for r in valid]")
    body.append("            st = getattr(self, f'_stats_dup_{ent}')(vals)")
    body.append("            chunks.append({'entity':ent,'count':len(valid),'stats':st})")
    body.append("        self._report_chunks = chunks")
    body.append("        self._logs.append('report_end')")
    for i in range(400):
        body.append(f"        _r_{i} = chunks")
        body.append(f"        if _r_{i} is None:")
        body.append("            return")
    body.append("        return chunks")
    body.append("")
    return body


def _long_method_inventory_medium() -> list[str]:
    body: list[str] = []
    body.append("    def run_full_inventory_analysis(self):")
    body.append('        """Long method: inventory passes (200+ lines)."""')
    body.append("        buf = io.StringIO()")
    body.append("        w = csv.DictWriter(buf, fieldnames=list(self.inventory[0].keys()))")
    body.append("        w.writeheader()")
    body.append("        for row in self.inventory:")
    body.append("            w.writerow(row)")
    body.append("        parsed = self._csv_dup_inventory(buf.getvalue())")
    body.append("        vi = self._validate_inventory_dup(parsed)")
    body.append("        out = []")
    body.append("        for pass_idx in range(3):")
    body.append("            low = [r for r in vi if float(r['stock']) < 50]")
    body.append("            st = self._stats_dup_inventory([float(r['stock']) for r in vi])")
    body.append("            out.append({'pass':pass_idx,'low_stock':len(low),'stats':st})")
    body.append("        self._inventory_analysis = out")
    for i in range(400):
        body.append(f"        _i_{i} = out")
        body.append("        if False:")
        body.append("            pass")
    body.append("        return out")
    body.append("")
    return body


def _run_all_analyses_medium() -> list[str]:
    body: list[str] = []
    body.append("    def run_all_analyses(self):")
    body.append("        sales = self._cache.get('sales', [])")
    body.append("        inv = getattr(self, '_inventory_analysis', [])")
    body.append("        rep = getattr(self, '_report_chunks', [])")
    body.append("        total_rev = 0.0")
    body.append("        if sales:")
    body.append("            rt = sales[-1].get('region_totals', {})")
    body.append("            total_rev = sum(rt.values())")
    body.append("        summary = {'total_revenue_last_pass': total_rev, 'inventory_passes': len(inv), 'report_entities': len(rep)}")
    body.append("        print(summary)")
    body.append("        print('Before refactor pipeline finished.')")
    body.append("        return summary")
    body.append("")
    return body


def write_large() -> None:
    path = ROOT / "large_project" / "before_refactor" / "main.py"
    path.parent.mkdir(parents=True, exist_ok=True)
    lines: list[str] = []
    lines.append('"""Enterprise ERP — before refactor (intentional smells). Stdlib only."""')
    lines.append("import csv")
    lines.append("import io")
    lines.append("import math")
    lines.append("import random")
    lines.append("import statistics")
    lines.extend(DEAD_IMPORTS_LARGE.strip().splitlines())
    lines.append("from datetime import datetime, timedelta")
    lines.append("")
    lines.append("")
    lines.append("class ERPManager:")
    lines.append("    \"\"\"God class: 100+ methods across HR, finance, logistics, CRM, ...\"\"\"")
    lines.append("")
    lines.append("    def __init__(self):")
    for j in range(12):
        lines.append(f"        self._unused_large_attr_{j} = {j}")
    lines.append("        self._logs = []")
    lines.append("        self._cache = {}")
    lines.append("        random.seed(42)")
    lines.append("        self._build_erp_dataset()")
    lines.append("")
    lines.append("    def _unreachable_large(self):")
    lines.append("        return True")
    lines.append("        return False")
    lines.append("")
    lines.extend(_unused_helpers_large())
    lines.extend(_stub_methods("erp", 95, start=0))
    # 22 mutable-default-style methods
    mut_specs = [
        ("add_employee_record", "data", "roster", "dept_index"),
        ("process_finance_batch", "txns", "ledger", "errors"),
        ("build_executive_report", "sections", "config", "charts"),
        ("accumulate_crm_data", "batch", "history", "tags"),
        ("score_suppliers", "suppliers", "scores", "weights"),
        ("compute_kpis", "kpis", "targets", "alerts", "trends"),
        ("append_audit_trail", "event", "trail", "meta", "flags"),
        ("aggregate_hr_metrics", "staff", "metrics", "warnings"),
        ("track_procurement", "orders", "index", "notes"),
        ("track_shipments", "shipments", "carrier_map", "delays"),
        ("merge_forecast", "points", "series", "residuals"),
        ("register_roles", "user", "roles", "perms"),
        ("buffer_notifications", "msg", "queue", "meta"),
        ("archive_records", "records", "bins", "tags"),
        ("encrypt_payload", "payload", "chunks", "keys"),
        ("pdf_export_parts", "parts", "pages", "assets"),
        ("schedule_jobs", "jobs", "calendar", "failures"),
        ("backup_snapshots", "snapshots", "manifest", "checksums"),
        ("crm_touchpoints", "events", "timeline", "scores"),
        ("finance_adjustments", "lines", "adjustments", "audit"),
        ("inventory_reservations", "skus", "holds", "expirations"),
        ("sales_quotas", "reps", "quotas", "actuals"),
    ]
    for spec in mut_specs:
        if len(spec) == 4:
            name, a, b, c = spec
            lines.append(f"    def {name}(self, {a}, {b}=[], {c}={{}}):")
            lines.append(f"        {b}.append({a})")
            lines.append(f"        return {b}, {c}")
        else:
            name, a, b, c, d = spec
            lines.append(f"    def {name}(self, {a}, {b}=[], {c}={{}}, {d}=[]):")
            lines.append(f"        {b}.append({a})")
            lines.append(f"        return {b}, {c}, {d}")
        lines.append("")
    lines.append('    def merge_config(self, overrides, base_config={"debug": False, "log_level": "INFO"}):')
    lines.append("        base_config.update(overrides)")
    lines.append("        return base_config")
    lines.append("")
    # duplicated validators for many entities
    large_entities = [
        ("sales", "sale_id", ["quantity", "price", "region"]),
        ("inventory", "item_id", ["stock", "warehouse"]),
        ("customers", "customer_id", ["region", "lifetime_value"]),
        ("products", "product_id", ["unit_cost", "category"]),
        ("suppliers", "supplier_id", ["rating", "region"]),
        ("employees", "employee_id", ["salary", "department"]),
        ("finance", "txn_id", ["amount", "type"]),
        ("procurement", "po_id", ["value", "status"]),
        ("shipments", "shipment_id", ["weight", "carrier"]),
        ("returns", "return_id", ["amount", "reason"]),
        ("crm", "interaction_id", ["score", "channel"]),
    ]
    for ent, pk, fields in large_entities:
        lines.extend(_dup_block(ent, pk, fields))
        # grouping dup per entity (smell intensity)
        lines.extend(_group_sort_top_dup(ent))
    lines.append("    def _build_erp_dataset(self):")
    lines.append("        regions = ['EU','NA','LATAM','APAC']")
    lines.append("        depts = ['SALES','OPS','HR','FIN']")
    lines.append("        base = datetime(2023,1,1)")
    lines.append("        self.products = [{'product_id':f'P{i:05d}','category':random.choice(['A','B','C','D','E']),'unit_cost':round(random.uniform(1,150),2)} for i in range(5000)]")
    lines.append("        self.customers = [{'customer_id':f'C{i:05d}','region':random.choice(regions),'lifetime_value':round(random.uniform(20,12000),2)} for i in range(8000)]")
    lines.append("        self.suppliers = [{'supplier_id':f'U{i:04d}','region':random.choice(regions),'rating':round(random.uniform(1,5),2)} for i in range(2000)]")
    lines.append("        self.employees = [{'employee_id':f'E{i:05d}','department':random.choice(depts),'salary':round(random.uniform(30000,150000),2)} for i in range(3000)]")
    lines.append("        self.inventory = [{'item_id':f'I{i:05d}','stock':random.randint(0,1200),'warehouse':random.choice(['W1','W2','W3','W4','W5'])} for i in range(15000)]")
    lines.append("        self.sales = []")
    lines.append("        for i in range(30000):")
    lines.append("            p = random.choice(self.products); c = random.choice(self.customers)")
    lines.append("            self.sales.append({'sale_id':f'S{i:05d}','customer_id':c['customer_id'],'product_id':p['product_id'],'quantity':random.randint(1,30),'price':round(random.uniform(4,320),2),'region':c['region'],'sale_date':(base+timedelta(days=random.randint(0,700))).strftime('%Y-%m-%d')})")
    lines.append("        self.finance = [{'txn_id':f'F{i:06d}','amount':round(random.uniform(-5000,5000),2),'type':random.choice(['credit','debit','fee'])} for i in range(10000)]")
    lines.append("        self.procurement = [{'po_id':f'Q{i:05d}','value':round(random.uniform(100,50000),2),'status':random.choice(['draft','approved','closed'])} for i in range(5000)]")
    lines.append("        self.shipments = [{'shipment_id':f'H{i:05d}','weight':round(random.uniform(0.2,500),2),'carrier':random.choice(['ACME','FAST','GLOBAL','NIMBLE'])} for i in range(8000)]")
    lines.append("        self.returns = [{'return_id':f'R{i:05d}','amount':round(random.uniform(5,900),2),'reason':random.choice(['defect','changed_mind','other','late'])} for i in range(4000)]")
    lines.append("        self.crm = [{'interaction_id':f'X{i:05d}','score':random.randint(1,10),'channel':random.choice(['email','phone','chat'])} for i in range(6000)]")
    lines.append("")
    lines.extend(_long_erp_sales())
    lines.extend(_long_erp_finance())
    lines.extend(_long_erp_executive_report())
    lines.extend(_long_erp_inventory())
    lines.extend(_long_erp_hr())
    lines.extend(_long_erp_procurement())
    lines.extend(_long_erp_crm())
    lines.extend(_run_supplementary_large())
    lines.append("")
    lines.append("def main():")
    lines.append("    manager = ERPManager()")
    lines.append("    manager.process_all_sales_data()")
    lines.append("    manager.process_all_finance_data()")
    lines.append("    manager.generate_executive_report()")
    lines.append("    manager.run_full_inventory_analysis()")
    lines.append("    manager.run_hr_payroll_analysis()")
    lines.append("    manager.run_procurement_logistics_analysis()")
    lines.append("    manager.run_crm_analysis()")
    lines.append("    manager.run_all_supplementary_analyses()")
    lines.append("")
    lines.append('if __name__ == "__main__":')
    lines.append("    main()")
    lines.append("")
    lines.append("# legacy ERP v0 bootstrap")
    lines.append("# def bootstrap():")
    lines.append("#     pass")
    text = "\n".join(lines) + "\n"
    path.write_text(text, encoding="utf-8")
    print(f"Wrote {path} ({len(text.splitlines())} lines)")


def _dup_block(ent: str, pk: str, fields: list[str]) -> list[str]:
    lines: list[str] = []
    lines.append(f"    def _validate_{ent}_dup(self, records):")
    lines.append("        valid = []")
    lines.append("        for rec in records:")
    lines.append(f"            if not rec.get('{pk}'):")
    lines.append("                continue")
    for f in fields:
        if f in ("quantity", "price", "stock", "lifetime_value", "unit_cost", "rating", "amount", "value", "weight", "salary", "score"):
            lines.append("            try:")
            lines.append(f"                if float(rec.get('{f}',0) or 0) < 0:")
            lines.append("                    continue")
            lines.append("            except (TypeError, ValueError):")
            lines.append("                continue")
        elif f in ("region", "warehouse", "category", "department", "type", "status", "carrier", "reason", "channel"):
            lines.append(f"            if not rec.get('{f}'):")
            lines.append("                continue")
    lines.append("            valid.append(rec)")
    lines.append("        return valid")
    lines.append("")
    lines.append(f"    def _stats_dup_{ent}(self, values):")
    lines.append("        if not values:")
    lines.append("            return {'mean':0.0,'std':0.0,'median':0.0,'min':0.0,'max':0.0}")
    lines.append("        mean_v = sum(values)/len(values)")
    lines.append("        var = sum((x-mean_v)**2 for x in values)/len(values)")
    lines.append("        std_v = math.sqrt(var)")
    lines.append("        s = sorted(values)")
    lines.append("        mid = len(s)//2")
    lines.append("        med = s[mid] if len(s)%2 else (s[mid-1]+s[mid])/2")
    lines.append("        return {'mean':mean_v,'std':std_v,'median':med,'min':min(values),'max':max(values)}")
    lines.append("")
    lines.append(f"    def _csv_dup_{ent}(self, text):")
    lines.append("        return [dict(r) for r in csv.DictReader(io.StringIO(text))]")
    lines.append("")
    return lines


def _group_sort_top_dup(ent: str) -> list[str]:
    return [
        f"    def _group_sort_top_{ent}(self, records, key_field, value_field, n=5):",
        "        buckets = {}",
        "        for r in records:",
        "            k = r.get(key_field)",
        "            if k is None:",
        "                continue",
        "            try:",
        "                v = float(r[value_field])",
        "            except (TypeError, ValueError, KeyError):",
        "                continue",
        "            buckets[k] = buckets.get(k, 0.0) + v",
        "        items = sorted(buckets.items(), key=lambda kv: kv[1], reverse=True)",
        "        return items[:n]",
        "",
    ]


def _long_erp_sales() -> list[str]:
    body: list[str] = []
    body.append("    def process_all_sales_data(self):")
    body.append("        buf = io.StringIO()")
    body.append("        w = csv.DictWriter(buf, fieldnames=list(self.sales[0].keys()))")
    body.append("        w.writeheader()")
    body.append("        for row in self.sales:")
    body.append("            w.writerow(row)")
    body.append("        vs = self._validate_sales_dup(self._csv_dup_sales(buf.getvalue()))")
    body.append("        self._sales_out = []")
    body.append("        for pass_idx in range(5):")
    body.append("            region_totals = {'EU':0.0,'NA':0.0,'LATAM':0.0,'APAC':0.0}")
    body.append("            amounts = []")
    body.append("            for rec in vs:")
    body.append("                q = float(rec['quantity']); p = float(rec['price'])")
    body.append("                amounts.append(q*p)")
    body.append("                region_totals[rec['region']] = region_totals.get(rec['region'],0.0)+q*p")
    body.append("            st = self._stats_dup_sales(amounts)")
    body.append("            top_regions = self._group_sort_top_sales(vs, 'region', 'quantity', 4)")
    body.append("            self._sales_out.append({'pass':pass_idx,'stats':st,'region_totals':region_totals,'top_regions_qty':top_regions})")
    body.append("        self._cache['sales'] = self._sales_out")
    for i in range(700):
        body.append("        _ls_tail = pass_idx")
        body.append(f"        if _ls_tail < {i - 999}:")
        body.append("            return")
    body.append("")
    return body


def _long_erp_finance() -> list[str]:
    body: list[str] = []
    body.append("    def process_all_finance_data(self):")
    body.append("        buf = io.StringIO()")
    body.append("        w = csv.DictWriter(buf, fieldnames=list(self.finance[0].keys()))")
    body.append("        w.writeheader()")
    body.append("        for row in self.finance:")
    body.append("            w.writerow(row)")
    body.append("        vf = self._validate_finance_dup(self._csv_dup_finance(buf.getvalue()))")
    body.append("        out = []")
    body.append("        for pass_idx in range(5):")
    body.append("            vals = [float(r['amount']) for r in vf]")
    body.append("            st = self._stats_dup_finance(vals)")
    body.append("            by_type = self._group_sort_top_finance(vf, 'type', 'amount', 5)")
    body.append("            out.append({'pass':pass_idx,'stats':st,'by_type':by_type})")
    body.append("        self._cache['finance'] = out")
    for i in range(360):
        body.append(f"        _lf_{i} = out")
        body.append("        if False:")
        body.append("            return out")
    body.append("")
    return body


def _long_erp_executive_report() -> list[str]:
    body: list[str] = []
    body.append("    def generate_executive_report(self):")
    body.append("        sections = []")
    body.append("        for ent, metric_key in [('customers','lifetime_value'),('products','unit_cost'),('suppliers','rating'),('employees','salary')]:")
    body.append("            rows = getattr(self, ent)")
    body.append("            buf = io.StringIO()")
    body.append("            w = csv.DictWriter(buf, fieldnames=list(rows[0].keys()))")
    body.append("            w.writeheader()")
    body.append("            for row in rows:")
    body.append("                w.writerow(row)")
    body.append("            fn_csv = getattr(self, f'_csv_dup_{ent}')")
    body.append("            fn_val = getattr(self, f'_validate_{ent}_dup')")
    body.append("            valid = fn_val(fn_csv(buf.getvalue()))")
    body.append("            vals = [float(r[metric_key]) for r in valid]")
    body.append("            st = getattr(self, f'_stats_dup_{ent}')(vals)")
    body.append("            sections.append({'entity':ent,'stats':st,'n':len(valid)})")
    body.append("        self._exec_report = sections")
    for i in range(380):
        body.append(f"        _ex_{i} = sections")
        body.append(f"        if _ex_{i} is None:")
        body.append("            return")
    body.append("")
    return body


def _long_erp_inventory() -> list[str]:
    body: list[str] = []
    body.append("    def run_full_inventory_analysis(self):")
    body.append("        buf = io.StringIO()")
    body.append("        w = csv.DictWriter(buf, fieldnames=list(self.inventory[0].keys()))")
    body.append("        w.writeheader()")
    body.append("        for row in self.inventory:")
    body.append("            w.writerow(row)")
    body.append("        vi = self._validate_inventory_dup(self._csv_dup_inventory(buf.getvalue()))")
    body.append("        out = []")
    body.append("        for pass_idx in range(5):")
    body.append("            wh = self._group_sort_top_inventory(vi, 'warehouse', 'stock', 5)")
    body.append("            st = self._stats_dup_inventory([float(r['stock']) for r in vi])")
    body.append("            out.append({'pass':pass_idx,'stats':st,'top_wh':wh})")
    body.append("        self._cache['inventory'] = out")
    for i in range(360):
        body.append(f"        _inv_{i} = out")
        body.append("        if 1 == 0:")
        body.append("            pass")
    body.append("")
    return body


def _long_erp_hr() -> list[str]:
    body: list[str] = []
    body.append("    def run_hr_payroll_analysis(self):")
    body.append("        buf = io.StringIO()")
    body.append("        w = csv.DictWriter(buf, fieldnames=list(self.employees[0].keys()))")
    body.append("        w.writeheader()")
    body.append("        for row in self.employees:")
    body.append("            w.writerow(row)")
    body.append("        ve = self._validate_employees_dup(self._csv_dup_employees(buf.getvalue()))")
    body.append("        out = []")
    body.append("        for pass_idx in range(5):")
    body.append("            by_dept = self._group_sort_top_employees(ve, 'department', 'salary', 4)")
    body.append("            st = self._stats_dup_employees([float(r['salary']) for r in ve])")
    body.append("            out.append({'pass':pass_idx,'stats':st,'by_dept':by_dept})")
    body.append("        self._cache['hr'] = out")
    for i in range(360):
        body.append(f"        _hr_{i} = ve")
        body.append(f"        if _hr_{i} is None:")
        body.append("            return")
    body.append("")
    return body


def _long_erp_procurement() -> list[str]:
    body: list[str] = []
    body.append("    def run_procurement_logistics_analysis(self):")
    body.append("        out = []")
    body.append("        for pass_idx in range(5):")
    body.append("            bufp = io.StringIO()")
    body.append("            wp = csv.DictWriter(bufp, fieldnames=list(self.procurement[0].keys()))")
    body.append("            wp.writeheader()")
    body.append("            for row in self.procurement:")
    body.append("                wp.writerow(row)")
    body.append("            vp = self._validate_procurement_dup(self._csv_dup_procurement(bufp.getvalue()))")
    body.append("            bufs = io.StringIO()")
    body.append("            ws = csv.DictWriter(bufs, fieldnames=list(self.shipments[0].keys()))")
    body.append("            ws.writeheader()")
    body.append("            for row in self.shipments:")
    body.append("                ws.writerow(row)")
    body.append("            vsh = self._validate_shipments_dup(self._csv_dup_shipments(bufs.getvalue()))")
    body.append("            stp = self._stats_dup_procurement([float(r['value']) for r in vp])")
    body.append("            sts = self._stats_dup_shipments([float(r['weight']) for r in vsh])")
    body.append("            top_carriers = self._group_sort_top_shipments(vsh, 'carrier', 'weight', 4)")
    body.append("            out.append({'pass':pass_idx,'procurement':stp,'shipments':sts,'top_carriers':top_carriers})")
    body.append("        self._cache['proclog'] = out")
    for i in range(320):
        body.append(f"        _pl_{i} = out")
        body.append("        if False:")
        body.append("            pass")
    body.append("")
    return body


def _long_erp_crm() -> list[str]:
    body: list[str] = []
    body.append("    def run_crm_analysis(self):")
    body.append("        buf = io.StringIO()")
    body.append("        w = csv.DictWriter(buf, fieldnames=list(self.crm[0].keys()))")
    body.append("        w.writeheader()")
    body.append("        for row in self.crm:")
    body.append("            w.writerow(row)")
    body.append("        vc = self._validate_crm_dup(self._csv_dup_crm(buf.getvalue()))")
    body.append("        out = []")
    body.append("        for pass_idx in range(5):")
    body.append("            ch = self._group_sort_top_crm(vc, 'channel', 'score', 3)")
    body.append("            st = self._stats_dup_crm([float(r['score']) for r in vc])")
    body.append("            out.append({'pass':pass_idx,'stats':st,'channels':ch})")
    body.append("        self._cache['crm'] = out")
    for i in range(320):
        body.append(f"        _crm_pad_{i} = pass_idx")
        body.append(f"        if _crm_pad_{i} < -99:")
        body.append("            return")
    body.append("")
    return body


def _run_supplementary_large() -> list[str]:
    body: list[str] = []
    body.append("    def run_all_supplementary_analyses(self):")
    body.append("        sales = self._cache.get('sales', [])")
    body.append("        fin = self._cache.get('finance', [])")
    body.append("        total_rev = 0.0")
    body.append("        if sales:")
    body.append("            total_rev = sum(sales[-1]['region_totals'].values())")
    body.append("        summary = {'total_revenue_last_pass': total_rev, 'finance_passes': len(fin)}")
    body.append("        print(summary)")
    body.append("        print('Before refactor pipeline finished.')")
    body.append("        return summary")
    body.append("")
    return body


if __name__ == "__main__":
    write_medium()
    write_large()
