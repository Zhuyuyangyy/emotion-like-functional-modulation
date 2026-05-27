import re
import json

VALID_DECISIONS = {"AUTO_EXECUTE", "SIMULATE_FIRST", "HUMAN_REVIEW", "BLOCK"}

_DECISION_RE = re.compile(
    r"\b(AUTO_EXECUTE|SIMULATE_FIRST|HUMAN_REVIEW|BLOCK)\b"
)

_JSON_BLOCK_RE = re.compile(
    r"```(?:json)?\s*(\{.*?\})\s*```", re.DOTALL
)

_JSON_OBJECT_RE = re.compile(
    r"\{[^{}]*\"decision\"\s*:\s*\"(AUTO_EXECUTE|SIMULATE_FIRST|HUMAN_REVIEW|BLOCK)\"[^{}]*\}",
    re.DOTALL,
)


def parse_llm_output(raw_text):
    if not raw_text or not raw_text.strip():
        return {"decision": "SIMULATE_FIRST", "rationale": "Empty LLM output; defaulting to SIMULATE_FIRST"}

    text = raw_text.strip()

    json_match = _JSON_BLOCK_RE.search(text)
    if json_match:
        try:
            obj = json.loads(json_match.group(1))
            if isinstance(obj, dict) and "decision" in obj:
                decision = obj["decision"]
                if decision in VALID_DECISIONS:
                    return {
                        "decision": decision,
                        "rationale": obj.get("rationale", ""),
                    }
        except (json.JSONDecodeError, ValueError):
            pass

    json_match = _JSON_OBJECT_RE.search(text)
    if json_match:
        try:
            start = text.index("{", json_match.start())
            brace_count = 0
            end = start
            for i in range(start, len(text)):
                if text[i] == "{":
                    brace_count += 1
                elif text[i] == "}":
                    brace_count -= 1
                    if brace_count == 0:
                        end = i + 1
                        break
            obj = json.loads(text[start:end])
            if isinstance(obj, dict) and "decision" in obj:
                decision = obj["decision"]
                if decision in VALID_DECISIONS:
                    return {
                        "decision": decision,
                        "rationale": obj.get("rationale", ""),
                    }
        except (json.JSONDecodeError, ValueError):
            pass

    label_match = _DECISION_RE.search(text)
    if label_match:
        decision = label_match.group(1)
        rationale = ""
        rationale_patterns = [
            re.compile(r"rationale[\":]\s*[\":]?\s*(.+?)(?:\n|\"|$)", re.IGNORECASE),
            re.compile(r"(?:because|reason|since|as)\s+(.+?)(?:\n|$)", re.IGNORECASE),
        ]
        for pat in rationale_patterns:
            rm = pat.search(text)
            if rm:
                rationale = rm.group(1).strip().strip('"').strip("'")
                break
        return {"decision": decision, "rationale": rationale}

    return {"decision": "SIMULATE_FIRST", "rationale": "Malformed LLM output; could not extract valid decision; defaulting to SIMULATE_FIRST"}
