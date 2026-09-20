import os
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

from src.embeddings import GeminiEmbedder, _mock_embed
from src.chunking import compute_similarity

pairs = [
    (
        "Sinh viên đạt GPA từ 3.6 trở lên và rèn luyện xuất sắc được nhận học bổng loại Xuất sắc.",
        "Tiêu chuẩn nhận học bổng loại Xuất sắc là điểm trung bình tối thiểu 3.6 kèm điểm rèn luyện trên 90."
    ),
    (
        "Học bổng vượt khó hỗ trợ sinh viên nghèo có nguy cơ bỏ học vì thiếu kinh phí.",
        "Chứng chỉ tiếng Anh IELTS 6.0 là điều kiện bắt buộc để đi du học trao đổi quốc tế."
    ),
    (
        "Tiền học bổng khuyến khích học tập được chuyển khoản trực tiếp vào thẻ ATM của người học.",
        "Nhà trường chi trả trợ cấp học bổng qua tài khoản ngân hàng chính chủ của sinh viên."
    ),
    (
        "Thời hạn gửi đơn khiếu nại thắc mắc điểm xét học bổng là 5 ngày làm việc.",
        "Quy định trang phục và thẻ sinh viên khi vào thư viện mượn giáo trình."
    ),
    (
        "Học bổng tiến sĩ toàn phần 150 triệu đồng mỗi năm cho nghiên cứu sinh sau đại học.",
        "Sinh viên đại học năm thứ nhất được xét trợ cấp xã hội và miễn giảm học phí."
    )
]

gemini = GeminiEmbedder()

print("--- RESULTS ---")
for i, (a, b) in enumerate(pairs, 1):
    mock_score = compute_similarity(_mock_embed(a), _mock_embed(b))
    gem_score = compute_similarity(gemini(a), gemini(b))
    print(f"Pair {i}: Mock={mock_score:.4f} | Gemini={gem_score:.4f}")
