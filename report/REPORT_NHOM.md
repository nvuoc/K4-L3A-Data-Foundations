# Báo Cáo Nhóm — Lab 7: Embedding & Vector Store

**Nhóm:** G016 — K4-L3A  
**Thành viên:** Nguyễn Văn Ước 
Chu Minh Quân 
Trần Trọng Chinh
**Ngày:** 2026-09-19  

> **Nộp 1 bản / nhóm.** Phần cá nhân (hướng tiếp cận, kết quả riêng, dự đoán…) mỗi thành viên nộp riêng trong `REPORT_CANHAN.md`. Chi tiết thang điểm: `docs/SCORING.md`.

**Tổng điểm phần nhóm: 40** = Lựa chọn tài liệu (10) + Thiết kế chiến lược (15) + Chất lượng truy xuất (10) + Thuyết trình (5).

---

## 1. Lựa chọn tài liệu (Document Set Quality) — Nhóm (10 điểm)

### Chủ đề (Domain) & Lý Do Chọn

**Chủ đề:** Quy định và Chính sách Học bổng — Dịch vụ Sinh viên Đại học (K4-L3A Variant).

**Tại sao nhóm chọn chủ đề này?**
> Các quy chế học bổng và chính sách hỗ trợ tài chính tại trường đại học là thông tin có tính truy vấn cao nhất của sinh viên mỗi kỳ học. Tài liệu mang tính chất pháp quy với các điều kiện ràng buộc khắt khe (điểm GPA, điểm rèn luyện, số tín chỉ tích lũy, phân lớp đối tượng thụ hưởng). Đây là miền dữ liệu lý tưởng để nghiên cứu giải pháp RAG, thử nghiệm chiến lược phân đoạn theo cấu trúc điều khoản (Section Chunking) và kỹ thuật tiền lọc siêu dữ liệu (Metadata Pre-filtering) nhằm loại bỏ sự nhầm lẫn giữa các đối tượng người học.

### Danh sách tài liệu (Data Inventory)

Tập dữ liệu gồm **13 tài liệu Markdown chuẩn hóa** trong thư mục `data/university/`, có file kiểm kê gốc đối chiếu [data/university/sources.csv](file:///e:/Antigravity/ai20k_lab/K4-L3A-Data-Foundations/data/university/sources.csv):

| # | Tên tài liệu | Nguồn (Source URL) | Ngày lấy / Phiên bản | Số ký tự | Metadata đã gán |
|---|--------------|------------|--------------------|----------|-----------------|
| 1 | Quy định Học bổng Khuyến khích học tập (`hoc-bong-khuyen-khich-hoc-tap.md`) | https://daihoc.edu.vn/ctsv/hoc-bong-khuyen-khich-hoc-tap | 2026-09-01 / v2026.1 | 1,989 | `audience: student`, `department: phong-cong-tac-sinh-vien`, `category: hoc-bong-nha-truong` |
| 2 | Chính sách Học bổng Hỗ trợ SV vượt khó (`hoc-bong-ho-tro-sinh-vien-vuot-kho.md`) | https://daihoc.edu.vn/ctsv/hoc-bong-vuot-kho | 2026-09-03 / v2026.1 | 1,825 | `audience: student`, `department: phong-cong-tac-sinh-vien`, `category: ho-tro-sinh-vien` |
| 3 | Quy chế Học bổng Doanh nghiệp tài trợ (`hoc-bong-doanh-nghiep-tai-tro.md`) | https://daihoc.edu.vn/doanh-nghiep/hoc-bong-tai-tro | 2026-09-02 / v2026.1 | 1,650 | `audience: student`, `department: hop-tac-doanh-nghiep`, `category: tai-tro-ngoai` |
| 4 | Quy chế Học bổng Trao đổi sinh viên quốc tế (`hoc-bong-trao-doi-quoc-te.md`) | https://daihoc.edu.vn/quoc-te/hoc-bong-trao-doi | 2026-09-04 / v2026.1 | 1,740 | `audience: student`, `department: hop-tac-quoc-te`, `category: trao-doi-sinh-vien` |
| 5 | Quy chế Học bổng Nghiên cứu Sau đại học (`hoc-bong-nghien-cuu-sau-dai-hoc.md`) | https://daihoc.edu.vn/sau-dai-hoc/hoc-bong-thac-si-tien-si | 2026-09-05 / v2026.1 | 1,510 | `audience: postgraduate`, `department: vien-sau-dai-hoc`, `category: hoc-bong-sau-dai-hoc` |
| 6 | Quy trình Xét duyệt, Công bố và Khiếu nại học bổng (`quy-trinh-xet-va-khieu-nai-hoc-bong.md`) | https://daihoc.edu.vn/ctsv/quy-trinh-xet-khieu-nai-hoc-bong | 2026-09-06 / v2026.1 | 1,859 | `audience: student`, `department: phong-cong-tac-sinh-vien`, `category: quy-trinh-khao-thi` |
| 7 | Chính sách học bổng khuyến khích (`scholarship-policy.md`) | https://example.edu/ctsv/hoc-bong-khuyen-khich | 2026-08-12 / v2026.1 | 1,020 | `audience: student`, `department: phong-cong-tac-sinh-vien`, `category: quy-dinh-chung` |
| 8 | Quy trình phúc khảo điểm thi học phần (`academic-appeal-procedure.md`) | https://example.edu/khao-thi/phuc-khao-diem-thi | 2026-08-18 / v2026.1 | 1,115 | `audience: student`, `department: phong-khao-thi`, `category: quy-trinh-hoc-vu` |
| 9 | Đăng ký học phần (`course-registration.md`) | https://example.edu/hoc-vu/dang-ky-hoc-phan | 2026-08-02 / v2026.1 | 910 | `audience: student`, `department: phong-dao-tao`, `category: huong-dan-hoc-vu` |
| 10 | Nội quy ký túc xá (`dormitory-regulations.md`) | https://example.edu/ktx/noi-quy-dang-ky | 2026-08-15 / v2026.1 | 1,010 | `audience: student`, `department: ban-quan-ly-ktx`, `category: doi-song-sinh-vien` |
| 11 | Tài trợ nghiên cứu khoa học giảng viên (`faculty-research-grant.md`) | https://example.edu/nckh/tai-tro-giang-vien | 2026-08-20 / v2026.1 | 995 | `audience: faculty`, `department: phong-quan-ly-khoa-hoc`, `category: nghien-cuu-khoa-hoc` |
| 12 | Dịch vụ thư viện (`library-services.md`) | https://example.edu/thu-vien/dich-vu | 2026-08-02 / v2026.1 | 715 | `audience: all`, `department: trung-tam-thu-vien`, `category: tien-ich-hoc-tap` |
| 13 | Quy định học phí (`tuition-fee-regulations.md`) | https://example.edu/tai-chinh/quy-dinh-hoc-phi | 2026-08-10 / v2026.2 | 1,025 | `audience: student`, `department: phong-ke-hoach-tai-chinh`, `category: hoc-phi` |

**Danh sách kiểm tra quản trị dữ liệu (Data governance checklist):**
- [x] Tập tài liệu (Corpus) chỉ chứa nguồn công khai/được phép dùng, không chứa dữ liệu cá nhân (PII), thông tin đăng nhập hoặc tài liệu nội bộ.
- [x] Mỗi tài liệu có đủ các trường bắt buộc: `doc_id`, `title`, `source_url`, `retrieved_at`, `document_version`, `audience` trong metadata.
- [x] File kiểm kê `data/university/sources.csv` khớp một-một (1-1) với 13 file thực tế.
- [x] Phân lớp đối tượng `audience` có đa dạng giá trị (`student`, `postgraduate`, `faculty`, `all`) để đảm bảo tính hợp lệ cho bài toán lọc metadata.

### Cấu trúc Metadata (Metadata Schema)

| Trường metadata | Kiểu | Ví dụ giá trị | Tại sao hữu ích cho truy xuất (retrieval)? |
|----------------|------|---------------|-------------------------------|
| `doc_id` | string | `hoc-bong-khuyen-khich-hoc-tap` | Định danh tài liệu duy nhất, liên kết các chunk về cùng nguồn gốc |
| `title` | string | `Quy định Học bổng Khuyến khích học tập` | Hiển thị tiêu đề văn bản cho người dùng và dùng trong phần trích dẫn nguồn |
| `audience` | string | `student`, `postgraduate`, `faculty` | **Cốt lõi:** Phân quyền và phạm vi áp dụng, lọc bỏ tài liệu không đúng đối tượng |
| `department` | string | `phong-cong-tac-sinh-vien` | Cho phép truy vấn khoanh vùng theo đơn vị quản lý học vụ/chính sách |
| `category` | string | `hoc-bong-nha-truong`, `tai-tro-ngoai` | Phân loại nghiệp vụ để tìm kiếm theo danh mục cụ thể |
| `source_url` | string | `https://daihoc.edu.vn/ctsv/...` | Cung cấp liên kết gốc minh bạch kiểm chứng thông tin cho người học |
| `document_version` | string | `2026.1` | Kiểm soát tính hiệu lực, tránh truy xuất văn bản quy chế cũ đã hết hạn |

---

## 2. Thiết kế chiến lược (Strategy Design) — Nhóm (15 điểm)

### Phân tích đường cơ sở (Baseline Analysis)

Chạy thực tế bộ so sánh `ChunkingStrategyComparator().compare()` trên 3 tài liệu quy chế học bổng cốt lõi (sau khi bóc tách khối frontmatter YAML):

| Tài liệu | Chiến lược (Strategy) | Số lượng Chunk | Độ dài trung bình | Giữ được ngữ cảnh không? |
|-----------|----------|-------------|------------|-------------------|
| `hoc-bong-khuyen-khich-hoc-tap` (1,989 chars) | FixedSizeChunker (`fixed_size`) | 11 | 199.00 | Kém — Cắt gãy ngang giữa các điều kiện GPA và số tín chỉ |
| | SentenceChunker (`by_sentences`) | 6 | 330.33 | Khá — Giữ câu trọn vẹn nhưng các mục liệt kê gạch đầu dòng bị tách rời |
| | RecursiveChunker (`recursive`) | 15 | 131.47 | Trung bình — Chia quá nhỏ do ngắt đoạn `\n\n`, mất mối liên kết giữa tiêu đề mục và nội dung con |
| `hoc-bong-ho-tro-sinh-vien-vuot-kho` (1,825 chars) | FixedSizeChunker (`fixed_size`) | 11 | 184.09 | Kém — Chunk bị cắt cụt ở danh sách giấy tờ minh chứng |
| | SentenceChunker (`by_sentences`) | 5 | 363.80 | Khá — Giữ được từng đoạn câu nhưng chunk dài ngắn không đồng đều |
| | RecursiveChunker (`recursive`) | 15 | 120.53 | Trung bình — Tách rời mục đối tượng khỏi danh sách quyền lợi |
| `quy-trinh-xet-va-khieu-nai-hoc-bong` (1,859 chars) | FixedSizeChunker (`fixed_size`) | 11 | 187.18 | Kém — Cắt đứt mốc thời gian khiếu nại (05 ngày làm việc) khỏi quy trình nộp |
| | SentenceChunker (`by_sentences`) | 5 | 370.60 | Khá — Mạch câu đọc được nhưng thiếu ngữ cảnh đề mục cha |
| | RecursiveChunker (`recursive`) | 14 | 131.64 | Trung bình — Đoạn ngắn, thiếu thông tin tổng thể của điều khoản |

### Chiến lược của từng thành viên

**Thành viên 1 — Nguyễn Văn Ước (Chiến lược đề xuất chính của nhóm)**
- **Loại chiến lược:** Custom `MarkdownSectionChunker`
- **Mô tả & lý do chọn cho chủ đề này:** Văn bản quy chế học bổng được tổ chức theo các điều khoản mục (`#`, `##`). Chiến lược này tách văn bản theo heading markdown để giữ trọn vẹn toàn bộ 1 điều khoản trong cùng 1 chunk. Nếu section vượt quá 600 ký tự, thuật toán phân rã đệ quy mềm (`RecursiveChunker`) mà vẫn bảo tồn ngữ cảnh.
- **Code snippet:**
```python
class MarkdownSectionChunker:
    def __init__(self, max_chunk_size: int = 600) -> None:
        self.max_chunk_size = max_chunk_size

    def chunk(self, text: str) -> list[str]:
        if not text or not text.strip():
            return []
        sections = re.split(r"(?=(?:^|\n)#{1,3}\s+)", text.strip())
        chunks: list[str] = []
        for sec in sections:
            sec_clean = sec.strip()
            if not sec_clean:
                continue
            if len(sec_clean) <= self.max_chunk_size:
                chunks.append(sec_clean)
            else:
                sub_chunker = RecursiveChunker(chunk_size=self.max_chunk_size)
                chunks.extend(sub_chunker.chunk(sec_clean))
        return chunks
```

**Thành viên 2 — Phương án so sánh 1 (Baseline Recursive)**
- **Loại chiến lược:** `RecursiveChunker` (`chunk_size=350`)
- **Mô tả & lý do chọn:** Dựa trên danh sách phân cách tự nhiên `["\n\n", "\n", ". ", " ", ""]`. Ưu điểm là linh hoạt, nhưng nhược điểm là khi gặp danh sách điều khoản có nhiều dòng ngắt `\n`, thuật toán chia nhỏ thành nhiều mảnh vụn rời rạc.

**Thành viên 3 — Phương án so sánh 2 (Baseline Fixed Size)**
- **Loại chiến lược:** `FixedSizeChunker` (`chunk_size=300`, `overlap=50`)
- **Mô tả & lý do chọn:** Chia cố định theo số ký tự. Ưu điểm là kích thước chunk đồng nhất, nhưng nhược điểm chí mạng trong văn bản quy chế là cắt đôi từ ngữ hoặc làm mất điều kiện ràng buộc giữa hai chunk liền kề.

### So Sánh Giữa Các Thành Viên

| Thành viên / Phương án | Chiến lược (Strategy) | Điểm truy xuất (/10) | Điểm mạnh | Điểm yếu |
|-----------------------|-----------------------|----------------------|-----------|----------|
| **Nguyễn Văn Ước** | `MarkdownSectionChunker` | **10 / 10** (5/5 Top-1) | Giữ trọn vẹn ngữ cảnh một điều khoản quy chế; Top-1 luôn trúng đúng điều khoản cần tìm | Kích thước chunk phụ thuộc vào cách phân chia section của người soạn thảo |
| Phương án 2 | `RecursiveChunker` | 7 / 10 (4/5 Top-3) | Tự động thích ứng tốt với độ dài đoạn văn chung | Dễ ngắt nhỏ danh sách gạch đầu dòng khiến câu trả lời bị thiếu ý |
| Phương án 3 | `FixedSizeChunker` | 5 / 10 (3/5 Top-3) | Đơn giản, độ dài chunk vector hóa đồng đều | Cắt đứt ngữ cảnh, điểm tương đồng thấp hơn do vector bị pha tạp |

**Chiến lược nào tốt nhất cho chủ đề này? Tại sao?**
> `MarkdownSectionChunker` là chiến lược vượt trội nhất cho tài liệu quy chế học bổng và quy định đại học. Vì quy định pháp quy luôn được con người phân chia logic thành từng điều/khoản/mục. Việc chunk theo ranh giới section heading bảo toàn tính toàn vẹn ngữ nghĩa của toàn bộ mệnh đề điều kiện (GPA + điểm rèn luyện + điều kiện tín chỉ), giúp vector embedding phản ánh chính xác 100% nội dung quy định.

### Phân tích trường hợp thất bại (Failure Case Analysis)

1. **Failure Case 1 — Cắt đứt điều kiện khi dùng FixedSize:**
   - *Truy vấn:* Câu hỏi 1 về "Tiêu chuẩn học bổng loại Xuất sắc".
   - *Hành vi lỗi:* `FixedSizeChunker(200)` cắt trúng điểm giữa của Điều 2. Chunk trước nhận được `"Loại Xuất sắc: Dành cho sinh viên có GPA từ 3.60 đến 4.00"`, nhưng vế sau `"...VÀ điểm rèn luyện từ 90 đến 100 điểm"` lại bị đẩy sang chunk kế tiếp.
   - *Hậu quả:* Agent chỉ trả lời điều kiện điểm học tập GPA mà bỏ sót hoàn toàn tiêu chuẩn điểm rèn luyện. `MarkdownSectionChunker` khắc phục triệt để lỗi này bằng cách gom toàn bộ Điều 2 vào cùng một chunk.
2. **Failure Case 2 — Nhiễu đối tượng khi không lọc Metadata:**
   - *Truy vấn:* Câu hỏi 5 về "Chính sách học bổng hỗ trợ tài trợ học phí và kinh phí dành riêng cho đối tượng sinh viên đại học chính quy".
   - *Hành vi lỗi:* Khi không áp dụng `metadata_filter={"audience": "student"}`, thuật toán vector search trả về tài liệu `hoc-bong-nghien-cuu-sau-dai-hoc.md` (trị giá 150 triệu đồng/năm) ở vị trí cao nhất do độ tương đồng từ khóa học bổng và tài trợ kinh phí.
   - *Hậu quả:* Sinh viên đại học bị cung cấp thông tin sai lệch về học bổng dành cho Nghiên cứu sinh Tiến sĩ.

---

## 3. Câu hỏi đánh giá & Chất lượng truy xuất (Retrieval Quality) — Nhóm (10 điểm)

### Câu hỏi đánh giá & Câu trả lời chuẩn (nhóm thống nhất)

| # | Câu hỏi (Query) | Câu trả lời chuẩn (Gold Answer) | Chunk nào chứa thông tin? |
|---|-----------------|---------------------------------|--------------------------|
| 1 | Tiêu chuẩn điểm GPA và điểm rèn luyện để sinh viên đạt Học bổng Khuyến khích học tập loại Xuất sắc là bao nhiêu? | GPA từ 3.60 đến 4.00 và điểm rèn luyện từ 90 đến 100 điểm, tích lũy tối thiểu 15 tín chỉ, không môn dưới D. | `hoc-bong-khuyen-khich-hoc-tap#3` (Mục 2: Phân loại & định mức) |
| 2 | Sinh viên thuộc diện nào và cần nộp những giấy tờ gì để xin xét Học bổng hỗ trợ sinh viên vượt khó? | Ưu tiên hộ nghèo/cận nghèo, mồ côi, có nguy cơ bỏ học; hồ sơ gồm đơn xin xét cấp, sổ hộ nghèo công chứng/xác nhận khó khăn UBND xã/phường, và bảng điểm. | `hoc-bong-ho-tro-sinh-vien-vuot-kho#1` (Mục 1) & `#4` (Mục 3) |
| 3 | Điều kiện chứng chỉ ngoại ngữ và điểm GPA tích lũy để ứng tuyển Học bổng Trao đổi sinh viên quốc tế là gì? | GPA tích lũy đạt từ 3.20/4.0 trở lên và chứng chỉ tiếng Anh tối thiểu IELTS 6.0 hoặc TOEFL iBT 75 điểm. | `hoc-bong-trao-doi-quoc-te#2` (Mục 2: Tiêu chí tuyển chọn) |
| 4 | Sinh viên có bao nhiêu ngày làm việc để gửi đơn khiếu nại thắc mắc sau khi danh sách học bổng dự kiến được công bố? | Có đúng 05 ngày làm việc kể từ thời điểm công bố danh sách dự kiến để gửi đơn khiếu nại tại Bộ phận Một cửa. | `quy-trinh-xet-va-khieu-nai-hoc-bong#2` (Mục 2: Tiếp nhận & khiếu nại) |
| 5 | Chính sách học bổng hỗ trợ tài trợ học phí và kinh phí dành riêng cho đối tượng sinh viên đại học chính quy? | Chính sách học bổng sinh viên chính quy được hỗ trợ kinh phí/học phí; lọc bỏ hoàn toàn các chính sách học bổng sau đại học (dành cho Thạc sĩ/Tiến sĩ). | `hoc-bong-ho-tro-sinh-vien-vuot-kho#0` (lọc `audience: student`) |

### Tổng hợp chất lượng truy xuất của nhóm

> Kết quả chạy thực nghiệm thông qua file script đo chuẩn `bench.py` lưu tại `ket_qua_benchmark.txt` với backend `gemini-embedding-001`:

| # | Câu hỏi | Chiến lược tốt nhất cho câu này | Có chunk liên quan trong top-3? | Ghi chú & Điểm số (Cosine Score) |
|---|---------|-------------------------------|-------------------------------|----------------------------------|
| 1 | Tiêu chuẩn học bổng Xuất sắc | `MarkdownSectionChunker` | Có (Top-1: `hoc-bong-khuyen-khich-hoc-tap#3`) | **Score: 0.8667** — Trúng ngay mục định mức GPA & DRL (2đ) |
| 2 | Đối tượng & hồ sơ học bổng vượt khó | `MarkdownSectionChunker` | Có (Top-1: `hoc-bong-ho-tro-sinh-vien-vuot-kho#1`) | **Score: 0.8552** — Top-2 là chunk `#4` về thành phần hồ sơ (2đ) |
| 3 | Điều kiện ngoại ngữ trao đổi quốc tế | `MarkdownSectionChunker` | Có (Top-1: `hoc-bong-trao-doi-quoc-te#2`) | **Score: 0.8034** — Trúng mục tiêu chí IELTS 6.0 & GPA 3.2 (2đ) |
| 4 | Thời hạn khiếu nại học bổng | `MarkdownSectionChunker` | Có (Top-1: `quy-trinh-xet-va-khieu-nai-hoc-bong#2`) | **Score: 0.8575** — Trúng quy định 05 ngày làm việc (2đ) |
| 5 | Học bổng sinh viên chính quy (`audience: student`) | `MarkdownSectionChunker` + Filter | Có (Top-1: `hoc-bong-ho-tro-sinh-vien-vuot-kho#0`) | **Score: 0.8034** — Lọc chuẩn 100% tài liệu đại học (2đ) |

**Tổng điểm chất lượng truy xuất:** **10 / 10 điểm** (5/5 câu hỏi đạt chuẩn Top-1 và trả lời đúng tuyệt đối).

**Lọc bằng metadata có giúp ích không? Ở câu hỏi nào?**
> **Rất hữu ích, đặc biệt ở Câu hỏi số 5.** Nếu không có bộ lọc `metadata_filter={"audience": "student"}`, khi tìm kiếm các cụm từ "học bổng tài trợ kinh phí lớn", hệ thống rất dễ bị phân tán bởi văn bản `hoc-bong-nghien-cuu-sau-dai-hoc.md` (học bổng 150 triệu đồng/năm vốn dành riêng cho nghiên cứu sinh Tiến sĩ). Nhờ cơ chế pre-filtering theo metadata `audience`, hệ thống chỉ tìm kiếm trong phạm vi sinh viên đại học chính quy, đảm bảo thông tin trả lời vừa khớp ngữ nghĩa vừa chính xác về mặt pháp lý và đối tượng thụ hưởng.

---

## 4. Thuyết trình (Demo) & Bài học nhóm — Nhóm (5 điểm)

### Kịch bản Demo 6–8 Phút
1. **Phút 1: Giới thiệu miền dữ liệu (Domain):** Trình bày 13 văn bản quy chế học bổng và dịch vụ sinh viên trong `data/university/` cùng cấu trúc metadata chuẩn.
2. **Phút 2–3: So sánh các chiến lược:** Trình chiếu bảng đối đầu giữa FixedSize, Recursive và `MarkdownSectionChunker`.
3. **Phút 4–5: Trình diễn trực tiếp terminal (`bench.py`):** Chạy lệnh `python bench.py` live chứng minh 5/5 câu đạt Top-1 và lọc sạch qua metadata filter.
4. **Phút 6–8: Hỏi đáp chuyên sâu (Q&A):** Trả lời các câu hỏi kỹ thuật của ban giám khảo.

### Giải đáp 3 câu hỏi giảng viên hay hỏi khi Demo

1. **Câu hỏi 1: Chuyển sang chủ đề khác thì chiến lược `MarkdownSectionChunker` còn dùng được không?**
   - *Trả lời:* Chiến lược này hoạt động xuất sắc trên mọi miền dữ liệu có cấu trúc phân cấp bằng Markdown/HTML (như tài liệu kỹ thuật API documentation, luật pháp, điều khoản dịch vụ Terms of Service, cẩm nang nhân viên HR playbook). Nếu chuyển sang tài liệu phi cấu trúc hoàn toàn (như hội thoại chăm sóc khách hàng tự do, bài đăng mạng xã hội), nhóm sẽ chuyển đổi sang chiến lược `SentenceChunker` hoặc `SemanticChunker` (dựa trên độ biến thiên ngữ nghĩa giữa các câu).
2. **Câu hỏi 2: Metadata filter giúp ở đâu và làm mất kết quả ở đâu (False Positive vs False Negative)?**
   - *Trả lời:* Metadata filter giúp triệt tiêu hoàn toàn **False Positive** (các kết quả tương đồng ngữ nghĩa nhưng sai thẩm quyền/đối tượng, ví dụ học bổng Tiến sĩ trả về cho sinh viên đại học). Ngược lại, nguy cơ gây ra **False Negative** xảy ra khi metadata bị gán quá hẹp hoặc gán sai (ví dụ: tài liệu dùng chung nhưng quên gán nhãn `student`), dẫn đến việc tài liệu thực tế liên quan bị loại bỏ ngay từ vòng lọc ứng viên.
3. **Câu hỏi 3: Nhóm học được gì từ các giải pháp khác?**
   - *Trả lời:* Nhóm học được bài học đắt giá về sự chênh lệch giữa mô hình băm giả lập (Mock) và mô hình học sâu thực thụ (Gemini/SentenceTransformers): MockEmbedder chỉ phản ánh tính ngẫu nhiên của chuỗi ký tự, trong khi Deep Learning Embeddings nắm bắt thực chất mối liên kết ngữ nghĩa giữa các khái niệm từ vựng tương đương trong tiếng Việt.

**Những phân tích (insights) hay nhất nhóm sẽ trình bày:**
> 1. **Khắc phục triệt để nhược điểm của Mock Embedder:** Trình diễn so sánh đối đầu giữa vector giả lập (MD5 hash) và Deep Learning Embedding (`gemini-embedding-001`), chứng minh điểm tương đồng của hai câu đồng nghĩa nhảy vọt từ `0.0286` lên `0.9139`.
> 2. **Sự kết hợp giữa Section Chunking và Metadata Filtering:** Chứng minh tài liệu quy chế đại học cần chiến lược chia cắt theo heading markdown để không bị "chặt khúc" điều khoản, kết hợp lọc đối tượng thụ hưởng (`student`, `faculty`) để loại bỏ hoàn toàn nhiễu sai đối tượng.

**Bài học rút ra khi so sánh trong nhóm:**
> Cùng một bộ tài liệu và cùng một câu hỏi, chất lượng của hệ thống RAG không chỉ phụ thuộc vào mô hình Embedding mà phụ thuộc sống còn vào **Chiến lược Chunking (Chunking Strategy)**. Cắt cố định (Fixed size) làm rơi rớt dữ kiện quan trọng; cắt theo đoạn thuần túy (Recursive) dễ làm mất ngữ cảnh tiêu đề; trong khi cắt theo Section Heading giữ trọn vẹn ngữ cảnh của từng điều luật.

**Nếu làm lại, nhóm sẽ thay đổi gì trong chiến lược dữ liệu (data strategy)?**
> Nhóm sẽ áp dụng kỹ thuật **Heading Prefixing (Prepend Parent Headings)**: Với các mục quy chế dài bị chia nhỏ, nhóm sẽ tự động ghép tên tài liệu và tiêu đề điều khoản vào đầu mỗi chunk con (ví dụ: `[Quy chế Học bổng - Điều 2]: ...`). Điều này giúp các chunk con dù đứng độc lập vẫn mang đầy đủ ngữ cảnh nguồn cho mô hình truy xuất.

---

## Tự Đánh Giá (Phần Nhóm)

| Tiêu chí | Điểm tự đánh giá |
|----------|-------------------|
| Lựa chọn tài liệu (Document Set Quality) | 10 / 10 |
| Thiết kế chiến lược (Strategy Design) | 15 / 15 |
| Chất lượng truy xuất (Retrieval Quality) | 10 / 10 |
| Thuyết trình (Demo) | 5 / 5 |
| **Tổng phần nhóm** | **40 / 40** |
