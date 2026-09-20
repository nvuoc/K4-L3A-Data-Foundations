# Báo Cáo Cá Nhân — Lab 7: Embedding & Vector Store
## Chủ đề nhóm: Quy định Học bổng của các trường đại học (K4-L3A)

**Họ tên:** Nguyễn Văn Ước
**Nhóm:** G03 — K4-L3A (Chủ đề: Học bổng Đại học)
**Ngày:** 2026-09-19

> **Nộp 1 bản / sinh viên.** Phần nhóm (lựa chọn tài liệu, thiết kế chiến lược, bộ câu hỏi đánh giá, demo) nộp chung 1 bản trong `REPORT_NHOM.md`. Chi tiết thang điểm: `docs/SCORING.md`.

**Tổng điểm phần cá nhân: 60** = Khởi động (5) + Hướng tiếp cận (10) + Hoàn thiện code (30) + Dự đoán độ tương tự (5) + Kết quả truy xuất của tôi (10).

---

## 1. Khởi động (Warm-up) — Cá nhân (5 điểm)

### Độ tương tự Cosine (Cosine Similarity) (Bài tập 1.1)

**Độ tương tự cosine cao (High cosine similarity) nghĩa là gì?**
> Độ tương tự cosine cao (tiến gần về 1) biểu thị hai vector embedding cùng chỉ về một hướng trong không gian vector đa chiều, cho thấy hai văn bản có độ tương đồng rất lớn về mặt ý nghĩa ngữ nghĩa hoặc chủ đề, không bị chi phối bởi độ dài số lượng từ giữa hai văn bản.

**Ví dụ có độ tương tự CAO (trong chủ đề Học bổng):**
- Câu A: Sinh viên có điểm trung bình từ 3.6 trở lên và điểm rèn luyện xuất sắc được nhận học bổng loại Xuất sắc.
- Câu B: Tiêu chuẩn xét cấp học bổng loại Xuất sắc là điểm GPA tối thiểu 3.60 kèm kết quả rèn luyện trên 90 điểm.
- Tại sao tương đồng: Cả hai câu đều cùng phát biểu một tiêu chí điều kiện chuẩn của học bổng khuyến khích học tập loại Xuất sắc (GPA $\ge$ 3.6 và DRL $\ge$ 90), dù sử dụng các cặp từ ngữ thay thế nhau ("điểm trung bình" vs "GPA", "điểm rèn luyện xuất sắc" vs "kết quả rèn luyện trên 90 điểm").

**Ví dụ có độ tương tự THẤP:**
- Câu A: Sinh viên nộp đơn xin xét cấp học bổng hỗ trợ vượt khó kèm bản sao công chứng sổ hộ nghèo.
- Câu B: Lịch thực hành cài đặt cấu hình router và switch tại phòng thí nghiệm mạng máy tính vào sáng thứ Ba.
- Tại sao khác: Hai câu thuộc hai miền kiến thức hoàn toàn không liên quan (chính sách an sinh xã hội / học bổng sinh viên khó khăn vs thực hành kỹ thuật viễn thông mạng), không chia sẻ ngữ cảnh hay trường từ vựng nào.

**Tại sao độ tương tự cosine (cosine similarity) được ưu tiên hơn khoảng cách Euclid (Euclidean distance) cho text embeddings?**
> Độ tương tự cosine đo góc định hướng giữa hai vector thay vì đo độ dài hình học tuyệt đối, do đó loại bỏ hoàn toàn sự sai lệch do độ dài văn bản (text length). Khoảng cách Euclid sẽ bị kéo giãn rất lớn khi so sánh hai đoạn văn bản cùng đề cập quy định học bổng nhưng một đoạn chỉ là một câu tóm tắt và một đoạn là cả một văn bản điều khoản dài gấp nhiều lần; ngược lại, cosine similarity chỉ tập trung vào sự đồng hướng về mặt ngữ nghĩa.

### Bài toán tính toán Chunking (Bài tập 1.2)

**Tài liệu 10,000 ký tự, chunk_size=500, overlap=50. Bao nhiêu chunks?**
> *Trình bày phép tính:*
> Áp dụng công thức: `số lượng chunk = ceil((độ_dài_tài_liệu - độ_chồng_chéo) / (kích_thước_chunk - độ_chồng_chéo))`
> Số lượng chunk = $\lceil (10,000 - 50) / (500 - 50) \rceil = \lceil 9,950 / 450 \rceil = \lceil 22.111... \rceil = 23$
> *Đáp án:* 23 chunks.

**Nếu độ chồng chéo (overlap) tăng lên 100, số lượng chunk thay đổi thế nào? Tại sao muốn độ chồng chéo nhiều hơn?**
> Số lượng chunk mới = $\lceil (10,000 - 100) / (500 - 100) \rceil = \lceil 9,900 / 400 \rceil = \lceil 24.75 \rceil = 25$ chunks (tăng thêm 2 chunks). Chúng ta muốn tăng độ chồng chéo trong các văn bản quy định học bổng nhằm tránh việc một điều khoản điều kiện (ví dụ: điều kiện GPA nằm ở cuối chunk trước nhưng điều kiện DRL và số tín chỉ lại rơi vào đầu chunk sau) bị cắt đứt ngữ cảnh, đảm bảo mô hình truy xuất luôn nắm bắt trọn vẹn mệnh đề quy định.

---

## 2. Hướng tiếp cận của tôi (My Approach) — Cá nhân (10 điểm)

Giải thích cách tiếp cận của bạn khi lập trình (implement) các phần chính trong gói `src`.

### Các hàm chia nhỏ (Chunking Functions)

**`SentenceChunker.chunk`** — hướng tiếp cận:
> Sử dụng regex `r"(?<=[.!?])\s+|(?<=\.)\n+"` với kỹ thuật lookbehind để xác định ranh giới kết thúc câu mà vẫn giữ nguyên vẹn dấu câu. Xử lý triệt để các edge cases như chuỗi rỗng hoặc nhiều dòng trống liên tiếp bằng `.strip()`. Sau đó gom nhóm câu thành chunk theo tham số `max_sentences_per_chunk` qua bước nhảy chỉ mục `range(0, len(sentences), step)`.

**`RecursiveChunker.chunk` / `_split`** — hướng tiếp cận:
> Áp dụng giải thuật chia phân cấp đệ quy duyệt danh sách dấu phân cách theo độ ưu tiên `["\n\n", "\n", ". ", " ", ""]`. Base case xảy ra khi đoạn văn bản hiện tại có độ dài $\le$ `chunk_size` hoặc khi danh sách dấu phân cách cạn kiệt (fallback cắt trượt theo ký tự). Thuật toán tách đoạn theo separator hiện tại, tích lũy các phần nhỏ vào `current_chunk` nếu tổng kích thước hợp lệ; chỉ gọi đệ quy sâu hơn khi một đoạn con đơn lẻ vượt quá `chunk_size`.

### Lớp EmbeddingStore

**`add_documents` + `search`** — hướng tiếp cận:
> Hàm `add_documents` chuẩn hóa mỗi `Document` thành bản ghi gồm `id`, `content`, `metadata` và vector nhúng tính từ `_embedding_fn`, lưu trữ vào danh sách bộ nhớ `self._store` (và đồng bộ sang ChromaDB nếu có). Hàm `search` vector hóa câu hỏi qua `_embedding_fn`, tính tích vô hướng (dot product) giữa vector truy vấn và toàn bộ vector trong store, sắp xếp giảm dần theo `score` và trả về danh sách `top_k` kết quả.

**`search_with_filter` + `delete_document`** — hướng tiếp cận:
> `search_with_filter` áp dụng chiến lược tiền lọc (pre-filtering): duyệt qua kho dữ liệu để chọn ra các chunk thỏa mãn toàn bộ điều kiện `key == value` trong `metadata_filter` (đặc biệt là `audience: student` để lọc bỏ các tài liệu học bổng sau đại học), sau đó mới tiến hành tính điểm và xếp hạng trên tập ứng viên này. `delete_document` lọc bỏ toàn bộ các bản ghi có `id == doc_id` hoặc `metadata['doc_id'] == doc_id` khỏi `self._store`, đồng bộ xóa trên ChromaDB và trả về `True` nếu có bản ghi bị xóa, ngược lại trả về `False`.

### Tác tử KnowledgeBaseAgent

**`answer`** — hướng tiếp cận:
> Triển khai mô hình RAG tiêu chuẩn gồm 3 bước: (1) Truy xuất `top_k` chunk liên quan nhất từ vector store bằng `self.store.search(question, top_k)`. (2) Dựng prompt có cấu trúc đưa ngữ cảnh các điều khoản học bổng vào phần `Context:\n{context}` kèm câu hỏi `Question: {question}`. (3) Gọi hàm `self.llm_fn(prompt)` để mô hình ngôn ngữ sinh câu trả lời có căn cứ xác thực từ ngữ cảnh được cung cấp.

---

## 3. Hoàn thiện code (Core Implementation) — Cá nhân (30 điểm)

Vượt qua bộ kiểm thử là điều kiện tính điểm phần này.

### Kết Quả Kiểm Thử (Test Results)

```
============================= test session starts =============================
platform win32 -- Python 3.14.7, pytest-9.1.1, pluggy-1.6.0 -- C:\Users\vanuo\AppData\Local\Programs\Python\Python314\python.exe
cachedir: .pytest_cache
rootdir: E:\Antigravity\ai20k_lab\K4-L3A-Data-Foundations
plugins: anyio-4.15.1
collecting ... collected 42 items

tests/test_solution.py::TestProjectStructure::test_root_main_entrypoint_exists PASSED [  2%]
tests/test_solution.py::TestProjectStructure::test_src_package_exists PASSED [  4%]
tests/test_solution.py::TestClassBasedInterfaces::test_chunker_classes_exist PASSED [  7%]
tests/test_solution.py::TestClassBasedInterfaces::test_mock_embedder_exists PASSED [  9%]
tests/test_solution.py::TestFixedSizeChunker::test_chunks_respect_size PASSED [ 11%]
tests/test_solution.py::TestFixedSizeChunker::test_correct_number_of_chunks_no_overlap PASSED [ 14%]
tests/test_solution.py::TestFixedSizeChunker::test_empty_text_returns_empty_list PASSED [ 16%]
tests/test_solution.py::TestFixedSizeChunker::test_no_overlap_no_shared_content PASSED [ 19%]
tests/test_solution.py::TestFixedSizeChunker::test_overlap_creates_shared_content PASSED [ 21%]
tests/test_solution.py::TestFixedSizeChunker::test_returns_list PASSED   [ 23%]
tests/test_solution.py::TestFixedSizeChunker::test_single_chunk_if_text_shorter PASSED [ 26%]
tests/test_solution.py::TestSentenceChunker::test_chunks_are_strings PASSED [ 28%]
tests/test_solution.py::TestSentenceChunker::test_respects_max_sentences PASSED [ 30%]
tests/test_solution.py::TestSentenceChunker::test_returns_list PASSED    [ 33%]
tests/test_solution.py::TestSentenceChunker::test_single_sentence_max_gives_many_chunks PASSED [ 35%]
tests/test_solution.py::TestRecursiveChunker::test_chunks_within_size_when_possible PASSED [ 38%]
tests/test_solution.py::TestRecursiveChunker::test_empty_separators_falls_back_gracefully PASSED [ 40%]
tests/test_solution.py::TestRecursiveChunker::test_handles_double_newline_separator PASSED [ 42%]
tests/test_solution.py::TestRecursiveChunker::test_returns_list PASSED   [ 45%]
tests/test_solution.py::TestEmbeddingStore::test_add_documents_increases_size PASSED [ 47%]
tests/test_solution.py::TestEmbeddingStore::test_add_more_increases_further PASSED [ 50%]
tests/test_solution.py::TestEmbeddingStore::test_initial_size_is_zero PASSED [ 52%]
tests/test_solution.py::TestEmbeddingStore::test_search_results_have_content_key PASSED [ 54%]
tests/test_solution.py::TestEmbeddingStore::test_search_results_have_score_key PASSED [ 57%]
tests/test_solution.py::TestEmbeddingStore::test_search_results_sorted_by_score_descending PASSED [ 59%]
tests/test_solution.py::TestEmbeddingStore::test_search_returns_at_most_top_k PASSED [ 61%]
tests/test_solution.py::TestEmbeddingStore::test_search_returns_list PASSED [ 64%]
tests/test_solution.py::TestKnowledgeBaseAgent::test_answer_non_empty PASSED [ 66%]
tests/test_solution.py::TestKnowledgeBaseAgent::test_answer_returns_string PASSED [ 69%]
tests/test_solution.py::TestComputeSimilarity::test_identical_vectors_return_1 PASSED [ 71%]
tests/test_solution.py::TestComputeSimilarity::test_opposite_vectors_return_minus_1 PASSED [ 73%]
tests/test_solution.py::TestComputeSimilarity::test_orthogonal_vectors_return_0 PASSED [ 76%]
tests/test_solution.py::TestComputeSimilarity::test_zero_vector_returns_0 PASSED [ 78%]
tests/test_solution.py::TestCompareChunkingStrategies::test_counts_are_positive PASSED [ 80%]
tests/test_solution.py::TestCompareChunkingStrategies::test_each_strategy_has_count_and_avg_length PASSED [ 83%]
tests/test_solution.py::TestCompareChunkingStrategies::test_returns_three_strategies PASSED [ 85%]
tests/test_solution.py::TestEmbeddingStoreSearchWithFilter::test_filter_by_department PASSED [ 88%]
tests/test_solution.py::TestEmbeddingStoreSearchWithFilter::test_no_filter_returns_all_candidates PASSED [ 90%]
tests/test_solution.py::TestEmbeddingStoreSearchWithFilter::test_returns_at_most_top_k PASSED [ 92%]
tests/test_solution.py::TestEmbeddingStoreDeleteDocument::test_delete_reduces_collection_size PASSED [ 95%]
tests/test_solution.py::TestEmbeddingStoreDeleteDocument::test_delete_returns_false_for_nonexistent_doc PASSED [ 97%]
tests/test_solution.py::TestEmbeddingStoreDeleteDocument::test_delete_returns_true_for_existing_doc PASSED [100%]

============================= 42 passed in 0.16s ==============================
```

**Số lượng bài test vượt qua (pass):** 42 / 42

---

## 4. Dự đoán độ tương tự (Similarity Predictions) — Cá nhân (5 điểm)

| Cặp | Câu A | Câu B | Dự đoán | Điểm Mock | Điểm Gemini (`gemini-embedding-001`) | Nhận xét |
|------|-----------|-----------|---------|-----------|-------------------------------------|----------|
| 1 | Sinh viên đạt GPA từ 3.6 trở lên và rèn luyện xuất sắc được nhận học bổng loại Xuất sắc. | Tiêu chuẩn nhận học bổng loại Xuất sắc là điểm trung bình tối thiểu 3.6 kèm điểm rèn luyện trên 90. | cao | 0.0286 | **0.9139** | Đúng tuyệt đối: Cùng diễn đạt điều kiện học bổng Xuất sắc |
| 2 | Học bổng vượt khó hỗ trợ sinh viên nghèo có nguy cơ bỏ học vì thiếu kinh phí. | Chứng chỉ tiếng Anh IELTS 6.0 là điều kiện bắt buộc để đi du học trao đổi quốc tế. | thấp | 0.3404 | **0.5847** | Đúng: Hai chính sách học bổng và tiêu chí hoàn toàn khác nhau |
| 3 | Tiền học bổng khuyến khích học tập được chuyển khoản trực tiếp vào thẻ ATM của người học. | Nhà trường chi trả trợ cấp học bổng qua tài khoản ngân hàng chính chủ của sinh viên. | cao | 0.1365 | **0.7909** | Đúng tuyệt đối: Cùng chỉ phương thức giải ngân học bổng |
| 4 | Thời hạn gửi đơn khiếu nại thắc mắc điểm xét học bổng là 5 ngày làm việc. | Quy định trang phục và thẻ sinh viên khi vào thư viện mượn giáo trình. | thấp | -0.0095 | **0.5823** | Đúng: Điểm tương đồng thấp nhất, hai lĩnh vực tách biệt |
| 5 | Học bổng tiến sĩ toàn phần 150 triệu đồng mỗi năm cho nghiên cứu sinh sau đại học. | Sinh viên đại học năm thứ nhất được xét trợ cấp xã hội và miễn giảm học phí. | thấp | -0.1877 | **0.6644** | Đúng: Hai đối tượng người học và định mức chi trả khác nhau |

**Kết quả nào bất ngờ nhất? Điều này nói gì về cách embeddings biểu diễn ý nghĩa?**
> - **Sự khác biệt mang tính bước ngoặt giữa MockEmbedder và Gemini Embeddings:**
>   - Ở **Cặp 1** và **Cặp 3**, khi dùng `MockEmbedder` (băm MD5 giả lập), điểm tương đồng chỉ đạt mức rất thấp (0.0286 và 0.1365), hoàn toàn không nhận diện được hai câu có cùng ý nghĩa thực tế. Ngược lại, khi chuyển sang mô hình thực tế **Gemini Embedding (`gemini-embedding-001`)**, điểm số lập tức nhảy vọt lên **0.9139** (Cặp 1) và **0.7909** (Cặp 3).
>   - Ở **Cặp 2**, `MockEmbedder` cho điểm cao bất thường (0.3404) do hiện tượng va chạm chuỗi giả ngẫu nhiên, trong khi Gemini Embedding kéo độ tương tự xuống nhóm thấp (**0.5847**), phản ánh chính xác sự khác biệt về trường từ vựng và ngữ cảnh.
> - **Bài học rút ra:** Mô hình embedding học sâu (Deep Learning Embeddings) không dựa vào sự trùng lặp ký tự đơn thuần mà ánh xạ các khái niệm ngữ nghĩa tương đương ("GPA $\ge$ 3.6" $\leftrightarrow$ "điểm trung bình tối thiểu 3.6", "thẻ ATM" $\leftrightarrow$ "tài khoản ngân hàng") vào các vùng lân cận gần nhau trong không gian vector đa chiều (3072 chiều).

---

## 5. Kết quả truy xuất của tôi (Competition Results) — Cá nhân (10 điểm)

Chạy **5 câu hỏi đánh giá của nhóm** trên tập ngữ liệu **Quy định học bổng của các trường đại học** với chiến lược chia nhỏ `MarkdownSectionChunker` và backend **Gemini Embeddings** (`gemini-embedding-001`):

| # | Câu hỏi (Query) | Top-1 Chunk truy xuất được (tóm tắt) | Điểm Score | Có liên quan không? (Relevant) | Câu trả lời của Agent (tóm tắt) |
|---|-------|--------------------------------|-------|-----------|------------------------|
| 1 | Tiêu chuẩn điểm GPA và điểm rèn luyện để sinh viên đạt Học bổng Khuyến khích học tập loại Xuất sắc là bao nhiêu? | `hoc-bong-khuyen-khich-hoc-tap_c3`: Mục 2. Phân loại và định mức học bổng | **0.8667** | Rất chính xác | Căn cứ quy chế, GPA từ 3.60 đến 4.00 và điểm rèn luyện từ 90 đến 100 điểm, tích lũy tối thiểu 15 tín chỉ, không môn dưới D. |
| 2 | Sinh viên thuộc diện nào và cần nộp những giấy tờ gì để xin xét Học bổng hỗ trợ sinh viên vượt khó? | `hoc-bong-ho-tro-sinh-vien-vuot-kho_c1`: Mục 1. Đối tượng và mục đích hỗ trợ *(Top-2 là chunk `_c4` về hồ sơ minh chứng)* | **0.8552** | Rất chính xác | Căn cứ chính sách, ưu tiên hộ nghèo/cận nghèo, mồ côi; hồ sơ gồm đơn xin xét cấp, sổ hộ nghèo công chứng/xác nhận khó khăn của UBND xã/phường, và bảng điểm. |
| 3 | Điều kiện chứng chỉ ngoại ngữ và điểm GPA tích lũy để ứng tuyển Học bổng Trao đổi sinh viên quốc tế là gì? | `hoc-bong-trao-doi-quoc-te_c2`: Mục 2. Tiêu chí và điều kiện tuyển chọn | **0.8034** | Rất chính xác | Căn cứ quy chế trao đổi quốc tế, yêu cầu điểm GPA tích lũy đạt từ 3.20/4.0 trở lên và chứng chỉ tiếng Anh tối thiểu IELTS 6.0 hoặc TOEFL iBT 75 điểm. |
| 4 | Sinh viên có bao nhiêu ngày làm việc để gửi đơn khiếu nại thắc mắc sau khi danh sách học bổng dự kiến được công bố? | `quy-trinh-xet-va-khieu-nai-hoc-bong_c2`: Mục 2. Quy định tiếp nhận và giải quyết khiếu nại | **0.8575** | Rất chính xác | Căn cứ quy trình khiếu nại, sinh viên có đúng 05 ngày làm việc kể từ thời điểm công bố danh sách dự kiến để gửi đơn khiếu nại tại Bộ phận Một cửa. |
| 5 | Chính sách học bổng hỗ trợ tài trợ học phí và kinh phí dành riêng cho đối tượng sinh viên đại học chính quy? *(lọc `metadata_filter={"audience": "student"}`)* | `hoc-bong-ho-tro-sinh-vien-vuot-kho_c0`: Chính sách học bổng hỗ trợ SV khó khăn *(lọc loại trừ học bổng Sau Đại học)* | **0.8034** | Rất chính xác | Căn cứ quy chế, sinh viên đại học được nhận học bổng doanh nghiệp/khuyến khích học tập; chính sách lọc loại trừ hoàn toàn học bổng sau đại học (dành cho Thạc sĩ/Tiến sĩ). |

**Bao nhiêu câu hỏi trả về chunk có liên quan trong top-3?** 5 / 5 (100% câu hỏi trả về chunk mục tiêu ngay tại vị trí Top-1 với điểm cosine similarity $> 0.80$).

**Điều hay nhất tôi học được từ thành viên khác / nhóm khác (qua demo):**
> 1. **Sức mạnh kết hợp giữa Section Chunking và Real Semantic Embeddings:** Khi kết hợp `MarkdownSectionChunker` (giữ nguyên vẹn toàn bộ điều khoản) với `GeminiEmbedder` (bản chất 3072 chiều phân tích ngữ nghĩa sâu), Top-1 của cả 5 câu hỏi truy vấn đều đạt độ chính xác gần như tuyệt đối (score từ 0.80 đến 0.87), loại bỏ hoàn toàn hiện tượng "râu ông nọ cắm cằm bà kia" thường thấy khi dùng chunking cố định hoặc băm giả lập.
> 2. **Sự cần thiết của Metadata Filtering trong nghiệp vụ trường đại học:** Khi truy vấn về chính sách học bổng dành riêng cho sinh viên đại học (Câu 5), nếu không lọc bằng `metadata_filter={"audience": "student"}`, các tài liệu học bổng sau đại học (150 triệu đồng/năm cho nghiên cứu sinh) có thể bị kéo vào do sự tương đồng về từ khóa "học bổng tài trợ kinh phí". Nhờ metadata filter, hệ thống đảm bảo trả lời đúng quyền lợi của nhóm sinh viên chính quy.

---

## Tự Đánh Giá (Phần Cá Nhân)

| Tiêu chí | Điểm tự đánh giá |
|----------|-------------------|
| Khởi động (Warm-up) | 5 / 5 |
| Hướng tiếp cận của tôi (My Approach) | 10 / 10 |
| Hoàn thiện code (Core Implementation — tests) | 30 / 30 |
| Dự đoán độ tương tự (Similarity Predictions) | 5 / 5 |
| Kết quả truy xuất của tôi (Competition Results) | 10 / 10 |
| **Tổng phần cá nhân** | **60 / 60** |
