#!/usr/bin/env python3
from __future__ import annotations

import csv
import datetime as dt
import re
import zipfile
import xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple


WORKBOOK_PATH = Path("Cust Charting LT.xlsx")
OUTPUT_DIR = Path("outputs")

NS = {"main": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}


def col_to_idx(col: str) -> int:
    idx = 0
    for ch in col:
        idx = idx * 26 + (ord(ch) - 64)
    return idx - 1


def parse_shared_strings(zfile: zipfile.ZipFile) -> List[str]:
    if "xl/sharedStrings.xml" not in zfile.namelist():
        return []
    root = ET.fromstring(zfile.read("xl/sharedStrings.xml"))
    strings = []
    for si in root.findall("main:si", NS):
        strings.append("".join(t.text or "" for t in si.findall(".//main:t", NS)))
    return strings


def parse_sheet(zfile: zipfile.ZipFile, sheet_path: str) -> List[List[Optional[str]]]:
    shared_strings = parse_shared_strings(zfile)
    root = ET.fromstring(zfile.read(sheet_path))
    rows: List[List[Optional[str]]] = []
    for row in root.findall("main:sheetData/main:row", NS):
        row_values: Dict[int, Optional[str]] = {}
        max_col = -1
        for cell in row.findall("main:c", NS):
            cell_ref = cell.attrib.get("r")
            if not cell_ref:
                continue
            col_letters = re.match(r"[A-Z]+", cell_ref).group(0)
            col_idx = col_to_idx(col_letters)
            max_col = max(max_col, col_idx)
            cell_type = cell.attrib.get("t")
            value = None
            v = cell.find("main:v", NS)
            if cell_type == "s":
                if v is not None and v.text is not None:
                    value = shared_strings[int(v.text)]
            elif cell_type == "inlineStr":
                is_elem = cell.find("main:is", NS)
                if is_elem is not None:
                    value = "".join(t.text or "" for t in is_elem.findall(".//main:t", NS))
            else:
                if v is not None:
                    value = v.text
            row_values[col_idx] = value
        if row_values:
            rows.append([row_values.get(i) for i in range(max_col + 1)])
    return rows


def normalize_header(value: Optional[str]) -> str:
    if not value:
        return ""
    return " ".join(value.split())


def rows_to_dicts(rows: List[List[Optional[str]]]) -> List[Dict[str, Optional[str]]]:
    headers = [normalize_header(h) for h in rows[0]]
    data_rows = []
    for row in rows[1:]:
        row_dict = {}
        for idx, header in enumerate(headers):
            if not header:
                continue
            row_dict[header] = row[idx] if idx < len(row) else None
        data_rows.append(row_dict)
    return data_rows


def to_float(value: Optional[str]) -> float:
    if value is None:
        return 0.0
    if isinstance(value, str):
        cleaned = value.replace(",", "").strip()
        if cleaned == "":
            return 0.0
        try:
            return float(cleaned)
        except ValueError:
            return 0.0
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def parse_date(value: Optional[str]) -> Optional[dt.date]:
    if value is None:
        return None
    if isinstance(value, str):
        cleaned = value.strip()
        if cleaned == "":
            return None
        try:
            # Excel serialized date
            if re.match(r"^-?\d+(\.\d+)?$", cleaned):
                serial = float(cleaned)
                base = dt.datetime(1899, 12, 30)
                return (base + dt.timedelta(days=serial)).date()
        except ValueError:
            pass
        for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%d/%m/%Y", "%Y/%m/%d"):
            try:
                return dt.datetime.strptime(cleaned, fmt).date()
            except ValueError:
                continue
        try:
            return dt.datetime.fromisoformat(cleaned).date()
        except ValueError:
            return None
    if isinstance(value, (int, float)):
        base = dt.datetime(1899, 12, 30)
        return (base + dt.timedelta(days=float(value))).date()
    return None


def classify_customer(customer_name: Optional[str]) -> str:
    if customer_name and "ethos" in customer_name.lower():
        return "Internal"
    return "External"


def write_csv(path: Path, headers: Iterable[str], rows: Iterable[Iterable[Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="\n", encoding="utf-8") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(list(headers))
        for row in rows:
            writer.writerow(list(row))


def main() -> None:
    if not WORKBOOK_PATH.exists():
        raise SystemExit(f"Workbook not found: {WORKBOOK_PATH}")

    with zipfile.ZipFile(WORKBOOK_PATH) as zfile:
        sales_rows = parse_sheet(zfile, "xl/worksheets/sheet1.xml")
        inventory_rows = parse_sheet(zfile, "xl/worksheets/sheet2.xml")

    sales = rows_to_dicts(sales_rows)
    inventory = rows_to_dicts(inventory_rows)

    inventory_totals: Dict[Tuple[str, str], float] = defaultdict(float)
    for row in inventory:
        site = (row.get("Site") or "").strip()
        part_no = (row.get("Part No") or "").strip()
        onhand_qty = to_float(row.get("Onhand Qty"))
        if site and part_no:
            inventory_totals[(site, part_no)] += onhand_qty

    inventory_output_rows = [
        (site, part, qty)
        for (site, part), qty in sorted(inventory_totals.items())
    ]
    write_csv(
        OUTPUT_DIR / "Inventory_Normalized.csv",
        ["Site", "Part No", "Onhand Qty"],
        inventory_output_rows,
    )

    sales_filtered = []
    order_revenue: Dict[str, float] = defaultdict(float)
    order_cost: Dict[str, float] = {}
    for row in sales:
        date_value = parse_date(row.get("Order Creation Date"))
        year = date_value.year if date_value else None
        if year is None or year < 2019 or year > 2025:
            continue
        revenue_gbp = to_float(row.get("Revenue (£££)"))
        order_number = (row.get("Sales Order Number") or "").strip()
        if order_number:
            order_revenue[order_number] += revenue_gbp
            cost_value = to_float(row.get("(As Sold Cost) $") or 0)
            if cost_value and order_number not in order_cost:
                order_cost[order_number] = cost_value
        row["_parsed_year"] = year
        row["_revenue_gbp"] = revenue_gbp
        sales_filtered.append(row)

    for row in sales_filtered:
        order_number = (row.get("Sales Order Number") or "").strip()
        revenue_gbp = row.get("_revenue_gbp", 0.0)
        total_revenue = order_revenue.get(order_number, 0.0)
        cost_total = order_cost.get(order_number, 0.0)
        cost_alloc = 0.0
        if total_revenue > 0:
            cost_alloc = cost_total * (revenue_gbp / total_revenue)
        row["_cost_alloc_usd"] = cost_alloc

    part_groups: Dict[Tuple[str, str], Dict[str, Any]] = {}
    for row in sales_filtered:
        site = (row.get("Site") or "").strip()
        part_no = (row.get("Part Number") or "").strip()
        if not site or not part_no:
            continue
        key = (site, part_no)
        group = part_groups.setdefault(
            key,
            {
                "revenue_gbp": 0.0,
                "units": 0.0,
                "customers": set(),
                "internal_revenue_gbp": 0.0,
                "external_revenue_gbp": 0.0,
                "internal_units": 0.0,
                "external_units": 0.0,
                "internal_customers": set(),
                "external_customers": set(),
                "cost_alloc_usd": 0.0,
            },
        )
        revenue_gbp = float(row.get("_revenue_gbp", 0.0))
        qty = to_float(row.get("Qty Shipped"))
        customer_name = (row.get("Customer Name") or "").strip()
        customer_type = classify_customer(customer_name)
        group["revenue_gbp"] += revenue_gbp
        group["units"] += qty
        group["customers"].add(customer_name)
        group["cost_alloc_usd"] += float(row.get("_cost_alloc_usd", 0.0))
        if customer_type == "Internal":
            group["internal_revenue_gbp"] += revenue_gbp
            group["internal_units"] += qty
            group["internal_customers"].add(customer_name)
        else:
            group["external_revenue_gbp"] += revenue_gbp
            group["external_units"] += qty
            group["external_customers"].add(customer_name)

    part_rows = []
    for (site, part_no), group in sorted(part_groups.items()):
        onhand_qty = inventory_totals.get((site, part_no), 0.0)
        part_rows.append(
            (
                site,
                part_no,
                round(group["revenue_gbp"], 2),
                round(group["units"], 2),
                len(group["customers"]),
                round(group["internal_revenue_gbp"], 2),
                round(group["external_revenue_gbp"], 2),
                round(group["internal_units"], 2),
                round(group["external_units"], 2),
                len(group["internal_customers"]),
                len(group["external_customers"]),
                round(onhand_qty, 2),
                round(group["cost_alloc_usd"], 2),
                "",
                "",
            )
        )

    write_csv(
        OUTPUT_DIR / "part_level_pareto.csv",
        [
            "Site",
            "Part Number",
            "Revenue_GBP",
            "Units",
            "Customer_Count",
            "Internal_Revenue_GBP",
            "External_Revenue_GBP",
            "Internal_Units",
            "External_Units",
            "Internal_Customer_Count",
            "External_Customer_Count",
            "Onhand_Qty",
            "Cost_Allocated_USD",
            "Revenue_USD",
            "Margin_USD",
        ],
        part_rows,
    )

    customer_groups: Dict[Tuple[str, str], Dict[str, Any]] = {}
    for row in sales_filtered:
        site = (row.get("Site") or "").strip()
        customer_name = (row.get("Customer Name") or "").strip()
        if not site or not customer_name:
            continue
        key = (site, customer_name)
        group = customer_groups.setdefault(
            key,
            {
                "revenue_gbp": 0.0,
                "units": 0.0,
                "opportunities": set(),
                "cost_alloc_usd": 0.0,
            },
        )
        revenue_gbp = float(row.get("_revenue_gbp", 0.0))
        group["revenue_gbp"] += revenue_gbp
        group["units"] += to_float(row.get("Qty Shipped"))
        opportunity = (row.get("Saleforce Oppurtunity") or "").strip()
        if opportunity:
            group["opportunities"].add(opportunity)
        group["cost_alloc_usd"] += float(row.get("_cost_alloc_usd", 0.0))

    customer_rows = []
    for (site, customer_name), group in sorted(customer_groups.items()):
        customer_type = classify_customer(customer_name)
        customer_rows.append(
            (
                site,
                customer_name,
                customer_type,
                round(group["revenue_gbp"], 2),
                round(group["units"], 2),
                len(group["opportunities"]),
                round(group["cost_alloc_usd"], 2),
                "",
                "",
            )
        )

    write_csv(
        OUTPUT_DIR / "customer_level_pareto.csv",
        [
            "Site",
            "Customer Name",
            "Customer_Type",
            "Revenue_GBP",
            "Units",
            "Opportunity_Count",
            "Cost_Allocated_USD",
            "Revenue_USD",
            "Margin_USD",
        ],
        customer_rows,
    )

    customer_counts: Dict[Tuple[str, int, str], Dict[str, Any]] = {}
    for row in sales_filtered:
        site = (row.get("Site") or "").strip()
        part_no = (row.get("Part Number") or "").strip()
        year = row.get("_parsed_year")
        customer_name = (row.get("Customer Name") or "").strip()
        if not site or not part_no or not year or not customer_name:
            continue
        key = (site, int(year), part_no)
        group = customer_counts.setdefault(
            key,
            {
                "customers": set(),
                "internal_customers": set(),
                "external_customers": set(),
            },
        )
        group["customers"].add(customer_name)
        customer_type = classify_customer(customer_name)
        if customer_type == "Internal":
            group["internal_customers"].add(customer_name)
        else:
            group["external_customers"].add(customer_name)

    count_rows = []
    for (site, year, part_no), group in sorted(customer_counts.items()):
        count_rows.append(
            (
                site,
                year,
                part_no,
                len(group["customers"]),
                len(group["internal_customers"]),
                len(group["external_customers"]),
            )
        )

    write_csv(
        OUTPUT_DIR / "customer_counts_by_site_year_part.csv",
        [
            "Site",
            "Year",
            "Part Number",
            "Customer_Count",
            "Internal_Customer_Count",
            "External_Customer_Count",
        ],
        count_rows,
    )


if __name__ == "__main__":
    main()
