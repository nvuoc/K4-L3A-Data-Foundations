import os
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.chunking import ChunkingStrategyComparator

docs = [
    "data/university/hoc-bong-khuyen-khich-hoc-tap.md",
    "data/university/hoc-bong-ho-tro-sinh-vien-vuot-kho.md",
    "data/university/quy-trinh-xet-va-khieu-nai-hoc-bong.md",
]

comp = ChunkingStrategyComparator()
for d in docs:
    txt = Path(d).read_text(encoding="utf-8")
    body = txt.split("---", 2)[2].strip() if txt.startswith("---") else txt
    res = comp.compare(body)
    print(f"\nDocument: {Path(d).stem} ({len(body)} chars)")
    for strat, val in res.items():
        print(f"  - {strat}: Chunks = {val.get('count')}, Avg Length = {val.get('avg_length')}")
