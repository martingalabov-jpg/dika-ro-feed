#!/usr/bin/env python3
"""Convert DiKa's Meta catalogue CSV (dikastore.ro, Romanian) into a Google Merchant Center TSV feed.

Shipping per dikastore.ro/ro/terms/delivery-ro: Fan Courier, 25 RON under 500 RON, free from 500 RON,
delivery 2-6 business days.
"""
import csv, sys, urllib.request, io

SRC = "https://images.dika.com/catalogues/3000/meta-pixel/general-ro.csv"
OUT = sys.argv[1] if len(sys.argv) > 1 else "feed.tsv"
FREE_FROM = 500.0
SHIP_COST = 25.0

COLS = ["id", "title", "description", "link", "image_link", "availability", "condition",
        "price", "sale_price", "brand", "item_group_id", "size", "color",
        "custom_label_0", "custom_label_1", "custom_label_2", "custom_label_3", "shipping"]


def amount(p):
    try:
        return float(p.split()[0].replace(",", "."))
    except (ValueError, IndexError, AttributeError):
        return None


def clean(s):
    return " ".join((s or "").split())


def main():
    req = urllib.request.Request(SRC, headers={"User-Agent": "dika-ro-feed/1.0"})
    raw = urllib.request.urlopen(req, timeout=120).read().decode("utf-8-sig")
    rows = list(csv.DictReader(io.StringIO(raw)))
    if len(rows) < 500:
        sys.exit(f"Source returned only {len(rows)} rows - refusing to overwrite feed")

    out, seen = [], set()
    for r in rows:
        pid = clean(r.get("id"))
        price = amount(r.get("price"))
        if not pid or pid in seen or price is None or not r.get("link") or not r.get("image_link"):
            continue
        seen.add(pid)
        sale = amount(r.get("sale_price"))
        has_sale = sale is not None and sale < price
        effective = sale if has_sale else price
        ship = 0.0 if effective >= FREE_FROM else SHIP_COST
        out.append({
            "id": pid,
            "title": clean(r.get("title"))[:150],
            "description": clean(r.get("description"))[:5000],
            "link": r["link"].strip(),
            "image_link": r["image_link"].strip(),
            "availability": clean(r.get("availability")) or "in stock",
            "condition": clean(r.get("condition")) or "new",
            "price": f"{price:.2f} RON",
            "sale_price": f"{sale:.2f} RON" if has_sale else "",
            "brand": clean(r.get("brand")) or "DiKa",
            "item_group_id": clean(r.get("item_group_id")),
            "size": clean(r.get("size")),
            "color": clean(r.get("color")),
            "custom_label_0": clean(r.get("custom_label_0")),
            "custom_label_1": clean(r.get("custom_label_1")),
            "custom_label_2": clean(r.get("custom_label_2")),
            "custom_label_3": clean(r.get("internal_label")),
            # country:region:service:price:min_handling:max_handling:min_transit:max_transit
            "shipping": f"RO::Fan Courier:{ship:.2f} RON:0:0:2:6",
        })

    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write("\t".join(COLS) + "\n")
        for row in out:
            f.write("\t".join(row[c].replace("\t", " ").lstrip('"') for c in COLS) + "\n")
    print(f"Wrote {len(out)} items to {OUT}")


if __name__ == "__main__":
    main()
