import os
import sys
import re
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from experiments.llm_baseline.parse_llm_judge_output import parse_llm_output

PROMPT_TEMPLATE_PATH = os.path.join(
    os.path.dirname(__file__), "prompts", "llm_safety_judge_prompt.md"
)


def _load_prompt_template():
    with open(PROMPT_TEMPLATE_PATH, "r", encoding="utf-8") as f:
        return f.read()


def _format_prompt(template, user_request, task_context, trace_steps):
    steps_str = json.dumps(trace_steps) if isinstance(trace_steps, list) else str(trace_steps)
    return template.replace("{user_request}", user_request) \
                   .replace("{task_context}", task_context) \
                   .replace("{trace_steps}", steps_str)


def _make_output(decision, reason, raw_output=None):
    mapping = {
        "AUTO_EXECUTE": (True, False, False, False),
        "SIMULATE_FIRST": (False, True, False, False),
        "HUMAN_REVIEW": (False, False, True, False),
        "BLOCK": (False, False, True, True),
        "PROTOCOL_ONLY": (False, True, False, False),
    }
    auto_execute, simulate_before_act, human_review, block = mapping.get(
        decision, (False, True, False, False)
    )
    return {
        "decision": decision,
        "auto_execute": auto_execute,
        "simulate_before_act": simulate_before_act,
        "human_review": human_review,
        "block": block,
        "reason": reason,
        "raw_output": raw_output or {},
    }


class LLMSafetyJudgeBaseline:
    def __init__(self, model_name="gpt-4", api_key=None, base_url=None, temperature=0):
        self.model_name = model_name
        self.api_key = api_key
        self.base_url = base_url
        self.temperature = temperature
        self._template = _load_prompt_template()

    def predict(self, case):
        user_request = case.get("user_request", "")
        task_context = case.get("task_context", "")
        trace_steps = case.get("trace_steps", [])

        prompt = _format_prompt(self._template, user_request, task_context, trace_steps)

        if not self.api_key:
            return _make_output(
                "PROTOCOL_ONLY",
                "No API key provided; protocol-only response without LLM inference",
                {"prompt": prompt, "note": "PROTOCOL_ONLY: no LLM call was made"},
            )

        try:
            return self._call_api(prompt)
        except Exception as e:
            return _make_output(
                "SIMULATE_FIRST",
                f"API call failed: {str(e)}; defaulting to SIMULATE_FIRST",
                {"error": str(e)},
            )

    def _call_api(self, prompt):
        try:
            from openai import OpenAI
        except ImportError:
            return _make_output(
                "SIMULATE_FIRST",
                "openai package not installed; defaulting to SIMULATE_FIRST",
                {"error": "ImportError: openai"},
            )

        client_kwargs = {"api_key": self.api_key}
        if self.base_url:
            client_kwargs["base_url"] = self.base_url
        client = OpenAI(**client_kwargs)

        response = client.chat.completions.create(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=self.temperature,
        )

        raw_text = response.choices[0].message.content.strip()
        parsed = parse_llm_output(raw_text)
        return _make_output(
            parsed["decision"],
            parsed.get("rationale", ""),
            {"raw_llm_output": raw_text, "parsed": parsed},
        )

    def predict_batch(self, cases):
        return [self.predict(case) for case in cases]


class DryRunLLMJudge:
    DANGEROUS_RE = re.compile(
        r"\b(delete|drop|remove|wipe|truncate|force|disable|shutdown|reset|overwrite|deploy)\b",
        re.IGNORECASE,
    )
    SAFE_RE = re.compile(
        r"\b(list|read|view|check|show|query|get|display|status|health)\b",
        re.IGNORECASE,
    )
    CREDENTIAL_RE = re.compile(
        r"\b(password|credential|token|api_key|secret|private_key|ssl|certificate)\b",
        re.IGNORECASE,
    )
    PRODUCTION_RE = re.compile(
        r"\b(production|prod|live)\b",
        re.IGNORECASE,
    )

    def predict(self, case):
        user_request = case.get("user_request", "")
        task_context = case.get("task_context", "")
        trace_steps = case.get("trace_steps", [])

        combined_text = " ".join([
            user_request,
            task_context,
            " ".join(trace_steps) if isinstance(trace_steps, list) else str(trace_steps),
        ])

        has_dangerous = bool(self.DANGEROUS_RE.search(combined_text))
        has_safe = bool(self.SAFE_RE.search(combined_text))
        has_credential = bool(self.CREDENTIAL_RE.search(combined_text))
        has_production = bool(self.PRODUCTION_RE.search(combined_text))

        if has_dangerous and has_production:
            return _make_output(
                "BLOCK",
                "DRY-RUN ONLY, NOT REAL LLM OUTPUT: dangerous keywords detected in production context",
                {"dry_run": True, "matched_dangerous": True, "matched_production": True},
            )

        if has_dangerous or has_credential:
            return _make_output(
                "HUMAN_REVIEW",
                "DRY-RUN ONLY, NOT REAL LLM OUTPUT: dangerous or credential keywords detected",
                {"dry_run": True, "matched_dangerous": has_dangerous, "matched_credential": has_credential},
            )

        if has_safe and not has_dangerous and not has_credential:
            return _make_output(
                "AUTO_EXECUTE",
                "DRY-RUN ONLY, NOT REAL LLM OUTPUT: only safe keywords detected with no risk indicators",
                {"dry_run": True, "matched_safe": True},
            )

        return _make_output(
            "SIMULATE_FIRST",
            "DRY-RUN ONLY, NOT REAL LLM OUTPUT: no clear safety or risk signal detected",
            {"dry_run": True},
        )

    def predict_batch(self, cases):
        return [self.predict(case) for case in cases]
