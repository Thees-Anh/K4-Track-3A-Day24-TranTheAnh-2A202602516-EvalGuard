# Blueprint CI/CD cho RAG và guardrails

Nhóm cá nhân Trần Thế Anh — 2A202602516. Đây là đề xuất, chưa phải workflow production. Run dùng extractive/lexical/judge fallback và guard `local-policy-rails-v1` do endpoint/full NeMo không khả dụng.

Input → PII scan → input rail → retrieval/rerank → generation → output rail → response. PII được redact trong log; request block không vào RAG; secrets chỉ ở `.env`. LLM lỗi chỉ cho extractive fallback có metadata rõ ràng.

| Layer | P50 ms | P95 ms | P99 ms | Trạng thái |
|---|---:|---:|---:|---|
| PII scan | 0.0104 | 0.0122 | 0.0127 | local fallback |
| Input rail | 0.0047 | 0.0058 | 0.0067 | local fallback |
| Input sequential | 0.0155 | 0.0176 | 0.0183 | dưới 500ms |
| RAG | chưa đo | chưa đo | chưa đo | ngoài phạm vi |
| Output rail | chưa đo | chưa đo | chưa đo | ngoài phạm vi |
| Full request | chưa đo | chưa đo | chưa đo | không suy diễn |

Phép đo có 2 warm-up, 20 mẫu, percentile linear. Số này không đại diện NeMo/LLM network; cần benchmark lại ≥100 mẫu production.

CI đề xuất chạy pytest rồi experiments staging và trả nonzero nếu avg RAGAS <0.65, faithfulness <0.75, attacks <18/20, clean <8/8, output <4/4 hoặc full P95 ≥500ms. Artifact phải qua schema/hash/model-ID. Mốc lab vẫn 15/20.

Run hiện có factual/multi/adversarial mean 0.6983/0.6369/0.6226; κ=0.4444; attacks 20/20, clean false-positive 0, output 4/4. Theo dõi rolling quality, refusal/FPR, PII counts đã băm, latency và drift; cảnh báo FPR >1%, attack pass <90% hoặc adversarial mean giảm >0.05. Ưu tiên metadata version, semantic reranker, judge calibration lớn hơn và replay bằng NeMo sau khi sửa endpoint.
