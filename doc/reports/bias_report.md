# Đánh giá Judge Phase B

Nhóm cá nhân Trần Thế Anh — 2A202602516. A từ answers, B từ human labels, reference từ test set. Endpoint không hỗ trợ model nên lượt này dùng reference-overlap fallback; không dùng human label khi ra quyết định.

| ID | Pass 1 | Pass 2 quy đổi | Final | Consistent | Score A/B |
|---:|---|---|---|---|---|
| 1 | A | A | A | true | 1.000/0.722 |
| 5 | B | B | B | true | 0.231/0.385 |
| 12 | A | A | A | true | 1.000/0.345 |
| 21 | B | B | B | true | 0.391/0.609 |
| 41 | A | A | A | true | 0.135/0.081 |

Position inconsistency 0/5; verbosity win rate 3/5 = 0.6. Đây chỉ là dấu hiệu vì token overlap vốn ưu tiên câu dài.

Calibration theo ID 1,5,12,21,23,29,33,41,46,50: judge `1,0,0,1,0,0,0,0,1,0`; human `1,0,1,1,1,0,1,0,1,0`. Agreement 7/10, chance agreement 0.46, Cohen’s κ=(0.70−0.46)/(1−0.46)=0.4444, mức moderate và chưa đạt bonus. Lệch ở ID 12, 23, 33 do câu đúng ý nhưng ít từ trùng reference. Cần chạy lại bằng judge hỗ trợ JSON, audit disagreement và mở rộng calibration; judge không phải ground truth.
