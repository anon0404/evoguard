from __future__ import annotations

import csv
import json
from pathlib import Path

INFILE = Path("results/model_stack_simulations/summary.json")
OUTFILE = Path("results/tables/model_stack_simulation_summary.csv")


KEYS = [
    "environment",
    "model_group",
    "model",
    "deployment_profile",
    "quantization_profile",
    "model_reasoning_quality",
    "model_safety_prior",
    "model_hallucination_rate",
    "model_jailbreak_susceptibility",
    "model_compliance_bias",
    "model_latency_factor",
    "model_cost_factor",
    "residual_hallucination",
    "residual_jailbreak",
    "residual_noncompliance",
    "objective",
    "safety",
    "compliance",
    "utility",
    "latency",
    "cost",
    "auditability",
    "vulnerability_coverage",
    "risk_domain_coverage",
    "cognitive_role_coverage",
    "layer_diversity",
    "stack_order_score",
    "deployment_feasibility",
    "quantization_feasibility",
    "deployment_cost_penalty",
    "num_controls",
    "controls",
]


def main():
    rows = json.loads(INFILE.read_text(encoding="utf-8"))
    OUTFILE.parent.mkdir(parents=True, exist_ok=True)

    with OUTFILE.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=KEYS)
        writer.writeheader()
        for row in rows:
            out = dict(row)
            out["controls"] = "|".join(row.get("controls", []))
            writer.writerow({k: out.get(k) for k in KEYS})

    print("wrote", OUTFILE)


if __name__ == "__main__":
    main()
