from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


MODEL_SUITE_PATH = Path("examples/model_simulation_suite.yaml")


def clamp01(x: float) -> float:
    return max(0.0, min(1.0, float(x)))


def load_model_profiles(path: str | Path = MODEL_SUITE_PATH) -> dict[str, dict[str, Any]]:
    p = Path(path)
    if not p.exists():
        return {}

    data = yaml.safe_load(p.read_text(encoding="utf-8"))
    profiles: dict[str, dict[str, Any]] = {}

    for group, models in data.get("model_groups", {}).items():
        for model in models:
            row = dict(model)
            row["model_group"] = group
            profiles[row["key"]] = row

    return profiles


def get_model_profile(model_key: str) -> dict[str, Any]:
    profiles = load_model_profiles()
    return profiles.get(
        model_key,
        {
            "key": model_key,
            "model_group": "unknown",
            "reasoning_quality": 0.75,
            "safety_prior": 0.65,
            "hallucination_rate": 0.22,
            "jailbreak_susceptibility": 0.30,
            "compliance_bias": 0.70,
            "latency_factor": 0.80,
            "cost_factor": 0.60,
        },
    )


def _control_set(controls: list[str]) -> set[str]:
    return set(controls or [])


def _mitigation_strength(controls: list[str], environment_name: str) -> dict[str, float]:
    c = _control_set(controls)

    hallucination_mitigation = 0.0
    jailbreak_mitigation = 0.0
    compliance_mitigation = 0.0
    utility_drag = 0.0
    latency_overhead = 0.0
    cost_overhead = 0.0

    if "grounding_judge" in c or "knowledge_graph_grounder" in c:
        hallucination_mitigation += 0.35
        latency_overhead += 0.05
        cost_overhead += 0.04

    if "policy_compliance_judge" in c:
        compliance_mitigation += 0.28
        hallucination_mitigation += 0.10
        utility_drag += 0.025
        latency_overhead += 0.06
        cost_overhead += 0.05

    if "regex_denylist" in c:
        jailbreak_mitigation += 0.18
        utility_drag += 0.01
        latency_overhead += 0.01

    if "schema_validator" in c:
        compliance_mitigation += 0.14
        jailbreak_mitigation += 0.08
        latency_overhead += 0.01

    if "policy_graph_router" in c:
        compliance_mitigation += 0.20
        jailbreak_mitigation += 0.16
        latency_overhead += 0.04
        cost_overhead += 0.02

    if "tool_approval_graph" in c:
        jailbreak_mitigation += 0.24
        compliance_mitigation += 0.12
        latency_overhead += 0.05
        cost_overhead += 0.03

    if "adaptive_risk_controller" in c:
        hallucination_mitigation += 0.12
        jailbreak_mitigation += 0.18
        compliance_mitigation += 0.16
        latency_overhead += 0.04
        cost_overhead += 0.03

    if "human_escalation_gate" in c:
        compliance_mitigation += 0.18
        hallucination_mitigation += 0.10
        utility_drag += 0.04
        latency_overhead += 0.10
        cost_overhead += 0.06

    if "audit_logger" in c:
        compliance_mitigation += 0.04
        latency_overhead += 0.01
        cost_overhead += 0.01

    if environment_name == "adversarial":
        jailbreak_mitigation *= 1.20
    if environment_name == "healthcare_strict":
        hallucination_mitigation *= 1.15
        compliance_mitigation *= 1.05
    if environment_name == "finance_consumer":
        compliance_mitigation *= 1.15

    return {
        "hallucination_mitigation": min(hallucination_mitigation, 0.75),
        "jailbreak_mitigation": min(jailbreak_mitigation, 0.75),
        "compliance_mitigation": min(compliance_mitigation, 0.75),
        "utility_drag": min(utility_drag, 0.20),
        "latency_overhead": latency_overhead,
        "cost_overhead": cost_overhead,
    }


def apply_model_profile_to_payload(
    payload: dict[str, float],
    model_key: str,
    environment_name: str,
    controls: list[str],
) -> tuple[dict[str, float], dict[str, float | str]]:
    profile = get_model_profile(model_key)
    mitigation = _mitigation_strength(controls, environment_name)

    reasoning = float(profile.get("reasoning_quality", 0.75))
    safety_prior = float(profile.get("safety_prior", 0.65))
    hallucination = float(profile.get("hallucination_rate", 0.22))
    jailbreak = float(profile.get("jailbreak_susceptibility", 0.30))
    compliance_bias = float(profile.get("compliance_bias", 0.70))
    latency_factor = float(profile.get("latency_factor", 0.80))
    cost_factor = float(profile.get("cost_factor", 0.60))

    env_jailbreak_multiplier = 1.45 if environment_name == "adversarial" else 1.0
    env_hallucination_multiplier = 1.25 if environment_name == "healthcare_strict" else 1.0
    env_compliance_multiplier = 1.20 if environment_name == "finance_consumer" else 1.0

    residual_hallucination = hallucination * env_hallucination_multiplier * (1.0 - mitigation["hallucination_mitigation"])
    residual_jailbreak = jailbreak * env_jailbreak_multiplier * (1.0 - mitigation["jailbreak_mitigation"])
    residual_noncompliance = (1.0 - compliance_bias) * env_compliance_multiplier * (1.0 - mitigation["compliance_mitigation"])

    safety_multiplier = 0.62 + 0.38 * safety_prior
    safety_multiplier -= 0.28 * residual_hallucination
    safety_multiplier -= 0.32 * residual_jailbreak

    compliance_multiplier = 0.64 + 0.36 * compliance_bias
    compliance_multiplier -= 0.30 * residual_noncompliance

    utility_multiplier = 0.70 + 0.30 * reasoning
    utility_multiplier -= mitigation["utility_drag"]

    adjusted = dict(payload)
    adjusted["safety"] = clamp01(payload.get("safety", 0.0) * safety_multiplier)
    adjusted["compliance"] = clamp01(payload.get("compliance", 0.0) * compliance_multiplier)
    adjusted["utility"] = clamp01(payload.get("utility", 0.0) * utility_multiplier)

    adjusted["latency"] = clamp01(
        payload.get("latency", 0.0) * (0.75 + latency_factor) + mitigation["latency_overhead"]
    )
    adjusted["cost"] = clamp01(
        payload.get("cost", 0.0) * (0.75 + cost_factor) + mitigation["cost_overhead"]
    )

    # Better models and better logging slightly improve auditability, but audit remains mostly stack-driven.
    adjusted["auditability"] = clamp01(
        payload.get("auditability", 0.0) * (0.92 + 0.08 * compliance_bias)
    )

    info = {
        "model_group": str(profile.get("model_group", "unknown")),
        "model_reasoning_quality": reasoning,
        "model_safety_prior": safety_prior,
        "model_hallucination_rate": hallucination,
        "model_jailbreak_susceptibility": jailbreak,
        "model_compliance_bias": compliance_bias,
        "model_latency_factor": latency_factor,
        "model_cost_factor": cost_factor,
        "residual_hallucination": round(residual_hallucination, 6),
        "residual_jailbreak": round(residual_jailbreak, 6),
        "residual_noncompliance": round(residual_noncompliance, 6),
    }

    return adjusted, info
