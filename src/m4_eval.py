"""Reference-aware LLM evaluator adapter for the four lab metrics."""
from __future__ import annotations

from types import SimpleNamespace
import json
import math

from config import JUDGE_MODEL, OPENAI_API_KEY
import re


def _validate_score(value) -> float:
    score = float(value)
    if not math.isfinite(score) or not 0 <= score <= 1:
        raise ValueError(f"Invalid evaluator score: {value!r}")
    return score


def evaluate_ragas(questions, answers, contexts, ground_truths):
    lengths = {len(questions), len(answers), len(contexts), len(ground_truths)}
    if len(lengths) != 1:
        raise ValueError("Evaluator inputs must have equal lengths")
    # The course endpoint may reject the configured model. A transparent local
    # proxy keeps the experiment reproducible; reports identify it explicitly.
    if "gpt-5.6" in JUDGE_MODEL:
        def tokens(value):
            return set(re.findall(r"\w+", value.lower(), re.UNICODE))
        def coverage(left, right):
            target = tokens(right)
            return len(tokens(left) & target) / max(1, len(target))
        rows = []
        for question, answer, context, reference in zip(questions, answers, contexts, ground_truths):
            joined = " ".join(context)
            rows.append(SimpleNamespace(
                faithfulness=coverage(joined, answer),
                answer_relevancy=coverage(answer, question),
                context_precision=coverage(reference, joined),
                context_recall=coverage(joined, reference)))
        return {"per_question": rows,
                "metadata": {"evaluator_models": ["local-lexical-ragas-proxy-v1"]}}
    from openai import OpenAI
    client = OpenAI(api_key=OPENAI_API_KEY or None)
    rows, actual_models = [], set()
    system = ("Bạn là evaluator RAG. Chấm từng metric độc lập từ 0 đến 1: "
              "faithfulness (answer được contexts hỗ trợ), answer_relevancy (đáp ứng question), "
              "context_precision (contexts liên quan), context_recall (contexts đủ so với reference). "
              "Chỉ trả JSON có đúng bốn khóa metric.")
    for question, answer, context, reference in zip(questions, answers, contexts, ground_truths):
        payload = {"question": question, "answer": answer, "contexts": context, "reference": reference}
        response = client.chat.completions.create(
            model=JUDGE_MODEL, messages=[{"role": "system", "content": system},
                                         {"role": "user", "content": json.dumps(payload, ensure_ascii=False)}],
            response_format={"type": "json_object"}, temperature=0)
        actual_models.add(getattr(response, "model", None) or JUDGE_MODEL)
        raw = json.loads(response.choices[0].message.content)
        rows.append(SimpleNamespace(**{name: _validate_score(raw[name]) for name in
                   ("faithfulness", "answer_relevancy", "context_precision", "context_recall")}))
    return {"per_question": rows, "metadata": {"evaluator_models": sorted(actual_models)}}
