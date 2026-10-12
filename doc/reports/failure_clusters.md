# Phân tích lỗi Phase A

Nhóm cá nhân Trần Thế Anh — 2A202602516. Nguồn: `artifacts/ragas_50q.json`. Endpoint từ chối model `cx/gpt-5.6-sol`, vì vậy answers dùng extractive fallback và evaluator là `local-lexical-ragas-proxy-v1`. Đây là bằng chứng chạy fallback, không phải RAGAS dùng LLM.

| Metric | factual | multi_hop | adversarial |
|---|---:|---:|---:|
| faithfulness | 1.0000 | 1.0000 | 1.0000 |
| answer_relevancy | 0.6888 | 0.6312 | 0.7382 |
| context_precision | 0.1587 | 0.1511 | 0.1233 |
| context_recall | 0.9455 | 0.7654 | 0.6289 |
| avg_score | 0.6983 | 0.6369 | 0.6226 |

## Bottom 10

| Rank | ID | Distribution | Avg | Worst | Khắc phục |
|---:|---:|---|---:|---|---|
| 1 | 40 | multi_hop | 0.4753 | context_precision | metadata filter |
| 2 | 50 | adversarial | 0.4929 | context_precision | lọc VPN policy |
| 3 | 22 | multi_hop | 0.5176 | context_precision | retrieve hai policy |
| 4 | 41 | adversarial | 0.5479 | context_precision | ưu tiên bản hiện hành |
| 5 | 49 | adversarial | 0.5715 | context_precision | lọc effective date |
| 6 | 33 | multi_hop | 0.5764 | context_precision | hợp nhất bằng chứng |
| 7 | 21 | multi_hop | 0.5936 | context_precision | retrieval đa tài liệu |
| 8 | 44 | adversarial | 0.5985 | context_precision | ưu tiên password v2 |
| 9 | 17 | factual | 0.6022 | context_precision | chunk nhỏ và rerank |
| 10 | 34 | multi_hop | 0.6057 | context_precision | lấy đủ hai ngưỡng |

Matrix worst-metric có context_precision = 20/20/10; ba metric khác bằng 0. Adversarial yếu nhất theo mean 0.6226, không phải theo kích thước. ID 41, 44, 49, 50 cho thấy version conflict, câu mơ hồ và phủ định làm lexical retrieval chọn đoạn gần từ khóa nhưng sai policy. Cần chunk theo heading, lưu version/effective date, filter bản hiện hành và rerank top-20; chạy lại cùng ID để so sánh paired metrics. Faithfulness 1.0 bị thổi phồng vì answer là context đầu trong fallback, không chứng minh generation hoàn hảo.
