import os
import re
import sys
from pathlib import Path
from dotenv import load_dotenv

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

load_dotenv()

from src.models import Document
from src.chunking import MarkdownSectionChunker
from src.embeddings import GeminiEmbedder
from src.store import EmbeddingStore

def parse_markdown_with_frontmatter(file_path: Path) -> tuple[dict, str]:
    text = file_path.read_text(encoding="utf-8")
    metadata = {"source": str(file_path)}
    content = text
    
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            fm_text = parts[1].strip()
            content = parts[2].strip()
            for line in fm_text.splitlines():
                if ":" in line:
                    k, v = line.split(":", 1)
                    k = k.strip()
                    v = v.strip().strip('"').strip("'")
                    metadata[k] = v
    return metadata, content

def run_benchmark():
    files = list(Path("data/university").glob("*.md"))
    chunker = MarkdownSectionChunker(max_chunk_size=600)
    embedder = GeminiEmbedder()
    store = EmbeddingStore(collection_name="university_scholarships_gemini", embedding_fn=embedder)
    
    chunk_docs = []
    for f in sorted(files):
        meta, content = parse_markdown_with_frontmatter(f)
        chunks = chunker.chunk(content)
        for i, ch in enumerate(chunks):
            ch_meta = dict(meta)
            ch_meta["chunk_index"] = i
            doc_id = meta.get("doc_id", f.stem)
            chunk_docs.append(Document(id=f"{doc_id}_c{i}", content=ch, metadata=ch_meta))
            
    print(f"Total chunks indexed: {len(chunk_docs)}")
    store.add_documents(chunk_docs)
    
    queries = [
        (
            1,
            "Tiêu chuẩn điểm GPA và điểm rèn luyện để sinh viên đạt Học bổng Khuyến khích học tập loại Xuất sắc là bao nhiêu?",
            None
        ),
        (
            2,
            "Sinh viên thuộc diện nào và cần nộp những giấy tờ gì để xin xét Học bổng hỗ trợ sinh viên vượt khó?",
            None
        ),
        (
            3,
            "Điều kiện chứng chỉ ngoại ngữ và điểm GPA tích lũy để ứng tuyển Học bổng Trao đổi sinh viên quốc tế là gì?",
            None
        ),
        (
            4,
            "Sinh viên có bao nhiêu ngày làm việc để gửi đơn khiếu nại thắc mắc sau khi danh sách học bổng dự kiến được công bố?",
            None
        ),
        (
            5,
            "Chính sách học bổng hỗ trợ tài trợ học phí và kinh phí dành riêng cho đối tượng sinh viên đại học chính quy?",
            {"audience": "student"}
        ),
    ]
    
    for q_id, q, meta_filter in queries:
        print(f"\n================ Question {q_id} ================")
        print(f"Query: {q}")
        print(f"Filter: {meta_filter}")
        if meta_filter:
            results = store.search_with_filter(q, metadata_filter=meta_filter, top_k=3)
        else:
            results = store.search(q, top_k=3)
            
        for r_idx, r in enumerate(results, 1):
            doc_id = r["id"]
            score = r["score"]
            preview = r["content"][:140].replace("\n", " ")
            print(f"  [{r_idx}] ID: {doc_id} | Score: {score:.4f}")
            print(f"      Preview: {preview}...")

if __name__ == "__main__":
    run_benchmark()
