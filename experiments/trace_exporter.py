import json


_BASELINE_NAMES = [
    "FullCalibratorAdapter",
    "KeywordRuleBaseline",
    "SafeKeywordFirstBaseline",
    "RiskContextOracleBaseline",
    "NoExperienceNoAffectiveBaseline",
]

_ABLATION_NAMES = [
    "full",
    "w/o_strict_context_priority",
    "w/o_affective_pressure",
    "w/o_experience_memory",
    "w/o_case_level_reset",
    "w/o_boundary_regex",
]


def _extract_prediction(pred):
    return {
        "decision": pred.get("decision", ""),
        "reason": pred.get("reason", ""),
    }


def export_traces(cases, baseline_predictions, ablation_predictions, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        for idx, case in enumerate(cases):
            predictions = {}
            for name in _BASELINE_NAMES:
                preds = baseline_predictions.get(name, [])
                pred = preds[idx] if idx < len(preds) else {}
                predictions[name] = _extract_prediction(pred)

            ablations = {}
            for name in _ABLATION_NAMES:
                preds = ablation_predictions.get(name, [])
                pred = preds[idx] if idx < len(preds) else {}
                ablations[name] = _extract_prediction(pred)

            full_decision = ablations.get("full", {}).get("decision", "")
            expected_decision = case.get("expected_decision", "")

            trace = {
                "case_id": case.get("case_id", ""),
                "category": case.get("category", ""),
                "user_request": case.get("user_request", ""),
                "expected_decision": expected_decision,
                "predictions": predictions,
                "ablations": ablations,
                "full_correct": full_decision == expected_decision,
                "risk_context": case.get("risk_context", {}),
                "affective_signal": case.get("affective_signal", {}),
                "experience_context": case.get("experience_context", {}),
            }

            f.write(json.dumps(trace, ensure_ascii=False) + "\n")


def load_traces(path):
    traces = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                traces.append(json.loads(line))
    return traces
