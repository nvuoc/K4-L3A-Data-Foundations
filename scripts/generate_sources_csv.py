import csv
from pathlib import Path

dir_path = Path("data/university")
md_files = sorted(dir_path.glob("*.md"))

rows = []
for p in md_files:
    text = p.read_text(encoding="utf-8")
    fm = {}
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            for line in parts[1].strip().splitlines():
                if ":" in line:
                    k, v = line.split(":", 1)
                    fm[k.strip()] = v.strip().strip('"').strip("'")
                    
    doc_id = fm.get("doc_id", p.stem)
    file_path = f"data/university/{p.name}"
    title = fm.get("title", p.stem)
    source_url = fm.get("source_url", f"https://daihoc.edu.vn/quy-dinh/{p.stem}")
    retrieved_at = fm.get("retrieved_at", "2026-09-01")
    document_version = fm.get("document_version", "2026.1")
    license_or_permission = "public-source"
    audience = fm.get("audience", "student")
    
    rows.append({
        "doc_id": doc_id,
        "file_path": file_path,
        "title": title,
        "source_url": source_url,
        "retrieved_at": retrieved_at,
        "document_version": document_version,
        "license_or_permission": license_or_permission,
    })

csv_file = dir_path / "sources.csv"
with open(csv_file, "w", newline="", encoding="utf-8") as f:
    fieldnames = ["doc_id", "file_path", "title", "source_url", "retrieved_at", "document_version", "license_or_permission"]
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for r in rows:
        writer.writerow(r)

print(f"Generated {csv_file} with {len(rows)} entries.")
