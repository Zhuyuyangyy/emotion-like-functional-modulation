
import csv
import json
import os
from collections import defaultdict

VALID_LABELS = {"AUTO_EXECUTE", "SIMULATE_FIRST", "HUMAN_REVIEW", "BLOCK"}
LABELS_LIST = sorted(VALID_LABELS)
LABEL_TO_IDX = {label: idx for idx, label in enumerate(LABELS_LIST)}


def main():
    input_path = "blind_annotation_sample_100_completed.csv"
    output_path = "annotation_kappa_result.json"

    if not os.path.exists(input_path):
        print(f"Error: File {input_path} not found.")
        return

    annotator1_labels = []
    annotator2_labels = []

    with open(input_path, "r", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            label1 = row.get("annotator1_label", "").strip()
            label2 = row.get("annotator2_label", "").strip()

            if label1 not in VALID_LABELS:
                print(f"Warning: Invalid label '{label1}' for annotator 1 in case {row.get('case_id', 'unknown')}")
            if label2 not in VALID_LABELS:
                print(f"Warning: Invalid label '{label2}' for annotator 2 in case {row.get('case_id', 'unknown')}")

            annotator1_labels.append(label1)
            annotator2_labels.append(label2)

    if len(annotator1_labels) != 100 or len(annotator2_labels) != 100:
        print("Error: Expected 100 annotated cases.")
        return

    n = 100
    cm = [[0] * len(LABELS_LIST) for _ in range(len(LABELS_LIST))]
    for a1, a2 in zip(annotator1_labels, annotator2_labels):
        if a1 in LABEL_TO_IDX and a2 in LABEL_TO_IDX:
            i = LABEL_TO_IDX[a1]
            j = LABEL_TO_IDX[a2]
            cm[i][j] += 1

    po = sum(cm[i][i] for i in range(len(LABELS_LIST))) / n

    row_totals = [sum(row) for row in cm]
    col_totals = [sum(cm[i][j] for i in range(len(LABELS_LIST))) for j in range(len(LABELS_LIST))]
    pe = sum(row_totals[i] * col_totals[i] for i in range(len(LABELS_LIST))) / (n * n)

    if pe == 1.0:
        kappa = 1.0
    else:
        kappa = (po - pe) / (1 - pe)

    result = {
        "observed_agreement": po,
        "cohens_kappa": kappa,
        "confusion_matrix": cm,
        "labels": LABELS_LIST,
        "total_cases": 100
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"Results saved to {output_path}")
    print(f"Observed agreement: {po:.4f}")
    print(f"Cohen's kappa: {kappa:.4f}")


if __name__ == "__main__":
    main()
