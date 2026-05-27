
import json
import csv
import random
import os


def main():
    # Load datasets
    semireal_path = "/workspace/benchmark/semireal/affective_agent_safety_300.json"
    external_path = "/workspace/benchmark/external_style/agent_safety_stress_150.json"

    with open(semireal_path, "r") as f:
        semireal_data = json.load(f)

    with open(external_path, "r") as f:
        external_data = json.load(f)

    # Sample 60 from semireal, 40 from external
    random.seed(42)
    sampled_semireal = random.sample(semireal_data, 60)
    sampled_external = random.sample(external_data, 40)

    all_samples = sampled_semireal + sampled_external
    random.shuffle(all_samples)

    # Prepare CSV
    csv_path = "/workspace/papers/sci_affective_safety_calibration/annotation_reliability/blind_annotation_sample_100.csv"

    with open(csv_path, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = [
            "case_id",
            "source_dataset",
            "source_type",
            "user_request",
            "task_context",
            "trace_steps",
            "risk_context_summary",
            "pressure_context_summary",
            "annotator_label",
            "annotator_rationale",
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for sample in all_samples:
            source_dataset = "Semi-Real-300" if sample.get("case_id", "").startswith("SR-") else "External-Style-150"

            # Extract fields
            case_id = sample.get("case_id", "")
            source_type = sample.get("source_type", "")
            user_request = sample.get("user_request", "")
            task_context = sample.get("task_context", "")
            trace_steps = json.dumps(sample.get("trace_steps", []), ensure_ascii=False)

            # Risk context summary
            risk_ctx = sample.get("risk_context", {})
            risk_parts = []
            if risk_ctx.get("destructive"):
                risk_parts.append("destructive")
            if risk_ctx.get("sensitive_data"):
                risk_parts.append("sensitive_data")
            if risk_ctx.get("security_related"):
                risk_parts.append("security_related")
            if risk_ctx.get("production_environment"):
                risk_parts.append("production_environment")
            if risk_ctx.get("irreversible"):
                risk_parts.append("irreversible")
            risk_context_summary = ", ".join(risk_parts) if risk_parts else "none"

            # Pressure context summary
            pressure_ctx = sample.get("pressure_context", {})
            if pressure_ctx:
                pressure_summary = f"urgency={pressure_ctx.get('urgency', 0)}, trust_pressure={pressure_ctx.get('trust_pressure', 0)}"
            else:
                # For semireal, map affective_pressure_label
                aff_pressure = sample.get("affective_pressure_label", "low")
                pressure_summary = f"affective_pressure_label={aff_pressure}"

            writer.writerow({
                "case_id": case_id,
                "source_dataset": source_dataset,
                "source_type": source_type,
                "user_request": user_request,
                "task_context": task_context,
                "trace_steps": trace_steps,
                "risk_context_summary": risk_context_summary,
                "pressure_context_summary": pressure_summary,
                "annotator_label": "",
                "annotator_rationale": "",
            })

    print(f"Blind annotation sample generated at {csv_path}")


if __name__ == "__main__":
    main()
