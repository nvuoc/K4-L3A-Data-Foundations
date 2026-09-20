from __future__ import annotations

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

load_dotenv()

from src.models import Document
from src.chunking import MarkdownSectionChunker
from src.embeddings import (
    EMBEDDING_PROVIDER_ENV,
    GEMINI_EMBEDDING_MODEL,
    LOCAL_EMBEDDING_MODEL,
    OPENAI_EMBEDDING_MODEL,
    GeminiEmbedder,
    LocalEmbedder,
    OpenAIEmbedder,
    _mock_embed,
)
from src.store import EmbeddingStore

BENCHMARK_QUERIES = [
    {
        "id": 1,
        "query": "Tiêu chuẩn điểm GPA và điểm rèn luyện để sinh viên đạt Học bổng Khuyến khích học tập loại Xuất sắc là bao nhiêu?",
        "filter": None,
        "gold_doc": "hoc-bong-khuyen-khich-hoc-tap",
        "gold_answer": "GPA từ 3.60 đến 4.00 và điểm rèn luyện từ 90 đến 100 điểm, tích lũy tối thiểu 15 tín chỉ, không môn dưới D.",
    },
    {
        "id": 2,
        "query": "Sinh viên thuộc diện nào và cần nộp những giấy tờ gì để xin xét Học bổng hỗ trợ sinh viên vượt khó?",
        "filter": None,
        "gold_doc": "hoc-bong-ho-tro-sinh-vien-vuot-kho",
        "gold_answer": "Ưu tiên hộ nghèo/cận nghèo, mồ côi, có nguy cơ bỏ học; hồ sơ gồm đơn xin xét cấp, sổ hộ nghèo công chứng/xác nhận khó khăn UBND xã/phường, và bảng điểm.",
    },
    {
        "id": 3,
        "query": "Điều kiện chứng chỉ ngoại ngữ và điểm GPA tích lũy để ứng tuyển Học bổng Trao đổi sinh viên quốc tế là gì?",
        "filter": None,
        "gold_doc": "hoc-bong-trao-doi-quoc-te",
        "gold_answer": "GPA tích lũy đạt từ 3.20/4.0 trở lên và chứng chỉ tiếng Anh tối thiểu IELTS 6.0 hoặc TOEFL iBT 75 điểm.",
    },
    {
        "id": 4,
        "query": "Sinh viên có bao nhiêu ngày làm việc để gửi đơn khiếu nại thắc mắc sau khi danh sách học bổng dự kiến được công bố?",
        "filter": None,
        "gold_doc": "quy-trinh-xet-va-khieu-nai-hoc-bong",
        "gold_answer": "Có đúng 05 ngày làm việc kể từ thời điểm công bố danh sách dự kiến để gửi đơn khiếu nại tại Bộ phận Một cửa.",
    },
    {
        "id": 5,
        "query": "Chính sách học bổng hỗ trợ tài trợ học phí và kinh phí dành riêng cho đối tượng sinh viên đại học chính quy?",
        "filter": {"audience": "student"},
        "gold_doc": "hoc-bong-ho-tro-sinh-vien-vuot-kho",
        "gold_answer": "Chính sách học bổng sinh viên chính quy được hỗ trợ kinh phí/học phí; lọc bỏ hoàn toàn các chính sách học bổng sau đại học (dành cho Thạc sĩ/Tiến sĩ).",
    },
]


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    metadata: dict[str, str] = {}
    content = text
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            fm_text = parts[1].strip()
            content = parts[2].strip()
            for line in fm_text.splitlines():
                if ":" in line:
                    k, v = line.split(":", 1)
                    metadata[k.strip()] = v.strip().strip('"').strip("'")
    return metadata, content


def get_embedder():
    provider = os.getenv(EMBEDDING_PROVIDER_ENV, "gemini").strip().lower()
    if provider == "gemini":
        try:
            return GeminiEmbedder(model_name=os.getenv("GEMINI_EMBEDDING_MODEL", GEMINI_EMBEDDING_MODEL))
        except Exception as e:
            print(f"Warning: Failed to initialize GeminiEmbedder ({e}), falling back to mock")
            return _mock_embed
    elif provider == "openai":
        try:
            return OpenAIEmbedder(model_name=os.getenv("OPENAI_EMBEDDING_MODEL", OPENAI_EMBEDDING_MODEL))
        except Exception as e:
            print(f"Warning: Failed to initialize OpenAIEmbedder ({e}), falling back to mock")
            return _mock_embed
    elif provider == "local":
        try:
            return LocalEmbedder(model_name=os.getenv("LOCAL_EMBEDDING_MODEL", LOCAL_EMBEDDING_MODEL))
        except Exception as e:
            print(f"Warning: Failed to initialize LocalEmbedder ({e}), falling back to mock")
            return _mock_embed
    return _mock_embed


def main() -> int:
    data_dir = Path("data/university")
    if not data_dir.exists():
        print(f"Data directory not found: {data_dir}")
        return 1

    md_files = sorted(data_dir.glob("*.md"))
    print(f"=== BENCHMARK RETRIEVAL — LAB 7 ===")
    print(f"Loaded dataset: {data_dir} ({len(md_files)} markdown files)")

    # 1. Strategy: MarkdownSectionChunker
    chunker = MarkdownSectionChunker(max_chunk_size=600)
    print(f"Chunking Strategy: {chunker.__class__.__name__} (max_chunk_size=600)")

    # 2. Embedding backend
    embedder = get_embedder()
    print(f"Embedding Backend: {getattr(embedder, '_backend_name', embedder.__class__.__name__)}")

    # 3. Create Chunks and Documents
    documents: list[Document] = []
    for p in md_files:
        raw_text = p.read_text(encoding="utf-8")
        fm_meta, body = parse_frontmatter(raw_text)
        chunks = chunker.chunk(body)
        for i, ch in enumerate(chunks):
            ch_meta = dict(fm_meta)
            ch_meta["doc_id"] = fm_meta.get("doc_id", p.stem)
            ch_meta["source"] = str(p)
            ch_meta["chunk_index"] = i
            doc_id = f"{p.stem}#{i}"
            documents.append(Document(id=doc_id, content=ch, metadata=ch_meta))

    print(f"Total Chunks Generated: {len(documents)}")

    # 4. Store and Index
    store = EmbeddingStore(collection_name="benchmark_store", embedding_fn=embedder)
    store.add_documents(documents)
    print(f"Stored {store.get_collection_size()} chunks in EmbeddingStore\n")

    # 5. Run Benchmark Queries
    top3_success_count = 0
    top1_success_count = 0

    for item in BENCHMARK_QUERIES:
        q_id = item["id"]
        query = item["query"]
        q_filter = item["filter"]
        gold_doc = item["gold_doc"]
        gold_answer = item["gold_answer"]

        print(f"----------------------------------------------------------------------")
        print(f"Query #{q_id}: {query}")
        if q_filter:
            print(f"Metadata Filter: {q_filter}")
            results = store.search_with_filter(query, metadata_filter=q_filter, top_k=3)
        else:
            results = store.search(query, top_k=3)

        hit_top3 = False
        hit_top1 = False

        for rank, res in enumerate(results, 1):
            r_id = res["id"]
            r_doc_id = res["metadata"].get("doc_id", "")
            score = res["score"]
            preview = res["content"][:130].replace("\n", " ")
            is_gold = (gold_doc in r_doc_id) or (gold_doc in r_id)
            if is_gold:
                hit_top3 = True
                if rank == 1:
                    hit_top1 = True
            mark = "[GOLD MATCH]" if is_gold else "            "
            print(f"  Top-{rank} {mark} score={score:.4f} | doc={r_doc_id} (id={r_id})")
            print(f"         content: {preview}...")

        if hit_top3:
            top3_success_count += 1
        if hit_top1:
            top1_success_count += 1

        print(f"Gold Answer: {gold_answer}")
        print(f"Result Status: {'PASSED (Top-1)' if hit_top1 else ('PASSED (Top-3)' if hit_top3 else 'FAILED')}\n")

    print(f"============================ SUMMARY ============================")
    print(f"Top-1 Accuracy: {top1_success_count}/{len(BENCHMARK_QUERIES)} ({top1_success_count/len(BENCHMARK_QUERIES)*100:.1f}%)")
    print(f"Top-3 Accuracy: {top3_success_count}/{len(BENCHMARK_QUERIES)} ({top3_success_count/len(BENCHMARK_QUERIES)*100:.1f}%)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
