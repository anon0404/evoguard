# EvoGuard

![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-research-orange)
![Benchmark](https://img.shields.io/badge/benchmark-Guardrails%20Gym-purple)
![Search](https://img.shields.io/badge/search-neurogenetic-red)
![Reproducible](https://img.shields.io/badge/reproducibility-simulation--based-brightgreen)

**EvoGuard** is a research framework for studying how **guardrail architectures** should be composed around conversational AI systems operating in regulated and high-risk environments.

This repository accompanies the anonymized submission:

> **EvoGuard: Neurogenetic Search of Guardrail Architectures for Risk-Aware Conversational AI Systems**

---

## System Overview

<p align="center">
  <img src="evoguard_system.png" width="850"/>
  <br/>
  <em>EvoGuard models conversational safety as a layered guardrail architecture optimized through neurogenetic search.</em>
</p>

---

## TL;DR

- Guardrails are treated as **systems, not filters**.
- Architectures are **evolved, not hand-designed**.
- Evaluation covers **healthcare, finance, and adversarial risk environments**.
- Metrics include **safety, compliance, utility, latency, cost, auditability, coverage, and stack quality**.
- Core results are **simulation-based** and require no external APIs.

---

## Overview

Modern conversational AI safety is not solely a property of the base model. In deployed systems, safety emerges from a surrounding **guardrail architecture** composed of heterogeneous controls.

EvoGuard introduces two linked components:

1. **Guardrails Gym** — a benchmark layer for evaluating guardrail stacks across regulated conversational scenarios.
2. **EvoGuard Search** — a neurogenetic search engine that evolves guardrail architectures under risk, deployment, and model-profile constraints.

The framework studies how different guardrail stacks should be composed around conversational systems as risk, autonomy, and deployment constraints increase.

---

## Key Contributions

- **Guardrail architecture as a first-class object**  
  Safety is modeled as a system-level property, not only a model-level property.

- **Neurogenetic search over guardrail stacks**  
  Guardrail configurations are evolved using mutation, crossover, and multi-objective selection.

- **Regulated benchmark environments**  
  Healthcare, finance, and adversarial settings with structured risk annotations.

- **Multi-dimensional evaluation**  
  Metrics include safety, compliance, utility, latency, cost, auditability, risk coverage, cognitive-role coverage, and stack coherence.

- **Model-conditioned simulation**  
  Evaluation across 19 model profiles spanning API, open-weight, and edge deployments.

---

## Repository Structure

~~~text
main/src/guardrail_gym/
  benchmark/          scenario definitions, expansion, and loading logic
  controls/           guardrail primitive registry and control logic
  eval/               simulation engine, metrics, coverage, complementarity
  search/             EvoGuard genotype, mutation, crossover, search, fitness
  profiles/           deployment/environment profiles and configuration
  models/             adapters and interfaces for real or simulated models

main/benchmark_data/
  regulated_v2/       benchmark scenario datasets and structured inputs

main/models_catalog/
  model_catalog.yaml  definitions of supported models and capabilities

main/environments/
  deployment_profiles.yaml   environment and deployment configurations

main/examples/
  benchmark.*.yaml
  search.*.yaml
  model_simulation_suite.yaml

main/risk_ontology/
  expanded_control_catalog.yaml
  guardrail_layers.yaml
  cognitive_roles.yaml
  vulnerability_classes.yaml
  canonical_taxonomy.yaml
  control_coverage_matrix.yaml

main/scripts/
  run_model_stack_simulations.py
  run_baseline_comparison.py
  export_evoguard_vs_baselines.py
  plot_model_stack_simulations.py
  run_neurogenetic_experiments.py
  run_transfer_matrix.py
  run_operator_ablation.py
  run_complexity_escalation.py

main/docs/
  benchmark_spec.md
  cards/              documentation for benchmark components and concepts

main/tests/
  test_benchmark_runner.py
  test_benchmark_expansion.py
  test_smoke.py

main/results/
  tables/
  plots/

~~~

---

## Installation

Requires Python 3.10+.

Clone the repository:

~~~bash
git clone https://github.com/anon0404/evoguard.git
cd evoguard
~~~

Create and activate a virtual environment:

~~~bash
python -m venv .venv
source .venv/bin/activate
~~~

Install in editable mode:

~~~bash
python -m pip install -e ".[dev]"
~~~

Run tests:

~~~bash
pytest -q
~~~

---

## Quick Start

Run the main simulation pipeline:

~~~bash
python scripts/split_regulated_benchmark.py
python scripts/run_model_stack_simulations.py
python scripts/export_model_stack_simulation_table.py
python scripts/run_baseline_comparison.py
python scripts/export_evoguard_vs_baselines.py
python scripts/plot_model_stack_simulations.py
~~~

Expected outputs:

~~~text
results/tables/model_stack_simulation_summary.csv
results/tables/baseline_comparison.csv
results/tables/evoguard_vs_baselines.csv
results/plots/
~~~

---

## Main Result Files

The paper-facing result tables are generated at:

~~~text
results/tables/model_stack_simulation_summary.csv
results/tables/baseline_comparison.csv
results/tables/evoguard_vs_baselines.csv
~~~

These outputs support:

- EvoGuard vs static guardrail baselines
- environment-specific evolved guardrail stacks
- 17-model simulation analysis
- vulnerability and risk-domain coverage analysis
- stack-order and layer-diversity analysis
- auditability, latency, cost, and deployment trade-off analysis

---

## Benchmark Design

### Environments

The main experiments use three regulated environments:

1. **Healthcare strict**  
   Safety-critical, escalation-heavy scenarios involving medical urgency, personal health information, vulnerable users, and audit requirements.

2. **Finance consumer**  
   Suitability, fairness, financial vulnerability, consumer protection, and compliance constraints.

3. **Adversarial**  
   Jailbreak, prompt injection, misuse, abuse-resilience, and policy-evasion scenarios.

### Scenario Annotations

Each scenario may include:

- risk domains
- vulnerability factors
- system mode: chat, retrieval-augmented generation, or agentic workflow
- escalation requirements
- prohibited behaviors
- disclosure requirements
- metadata describing environment and deployment setting

---

## Guardrail Architecture Space

EvoGuard composes controls across multiple layers.

### Deterministic controls

- regex filters
- deny lists
- schema validators
- deterministic blocking or routing rules

### ML-based classifiers

- vulnerability classifiers
- medical urgency classifiers
- financial vulnerability classifiers
- embedding-based risk matchers

### LLM-based judges

- policy compliance judges
- grounding judges
- clinical scope judges
- suitability judges

### Graph-based controllers

- policy routers
- finite-state controllers
- tool approval graphs

### Neurosymbolic controls

- adaptive risk controllers
- constraint solver gates
- knowledge-grounding modules

### Human oversight

- escalation gates
- human review triggers
- high-risk handoff mechanisms

### Audit and monitoring

- audit logging
- session anomaly monitoring
- traceability mechanisms

---

## Evaluation Metrics

### Core metrics

- Safety
- Compliance
- Utility
- Latency
- Cost
- Auditability

### Coverage metrics

- Vulnerability coverage
- Risk-domain coverage
- Cognitive-role coverage

### Architecture metrics

- Layer diversity
- Stack-order score

### Deployment metrics

- Deployment feasibility
- Quantization feasibility
- Deployment cost penalty

---

## Baselines

Static baselines include:

- **Unguarded**: no guardrails
- **Rules-only**: deterministic filters and validators
- **Judge-only**: LLM-judge-style output evaluation
- **Graph-only**: policy graph routing
- **Hybrid manual**: hand-designed rules + judge + graph + audit stack

EvoGuard is compared against these baselines under identical simulation settings.

---

## Model Simulation

Model profiles are defined in:

~~~text
examples/model_simulation_suite.yaml
~~~

The current suite contains 17 model profiles grouped into:

- API frontier
- API fast / cost-optimized
- open-weight large
- open-weight medium
- edge-small

Profiles encode:

- simulated capability
- safety prior
- latency
- cost
- deployment mode
- quantization support

No external model APIs are required for the core experiments.

---

## Neurogenetic Experiments

Additional experiments study environment-specific evolution, transfer, operator ablations, and complexity escalation:

~~~bash
python scripts/run_neurogenetic_experiments.py
python scripts/run_transfer_matrix.py
python scripts/run_operator_ablation.py
python scripts/run_complexity_escalation.py
python scripts/plot_neurogenetic_results.py
~~~

Expected outputs:

~~~text
results/neurogenetic/summary.json
results/neurogenetic/transfer_matrix.csv
results/neurogenetic/operator_ablation.csv
results/neurogenetic/complexity_escalation.csv
results/plots/neurogenetic_*.png
~~~

---

## Optional Real Model Adapters

Optional adapters are included for:

- OpenAI-compatible models
- Google Gemini
- Anthropic Claude
- local Hugging Face models

Install optional dependencies:

~~~bash
python -m pip install openai anthropic google-generativeai transformers accelerate
~~~

Set relevant API keys if needed:

~~~bash
export OPENAI_API_KEY="..."
export GOOGLE_API_KEY="..."
export ANTHROPIC_API_KEY="..."
~~~

Run smoke tests:

~~~bash
python scripts/real_multi_model_smoke.py
python scripts/run_real_multi_model_subset.py
~~~

These adapters are not required for reproducing the main simulation results.

---

## Reproducibility Checklist

This repository is designed to support reproducible paper results.

### Environment

- Python 3.10+
- Dependencies specified in `pyproject.toml`
- CPU sufficient for core simulations
- GPU not required

### Data

- Benchmark scenarios are included in `examples/`
- Search configurations are included in `examples/`
- Risk and guardrail ontologies are included in `risk_ontology/`
- No external datasets are required for core results

### Main experiment commands

~~~bash
python scripts/split_regulated_benchmark.py
python scripts/run_model_stack_simulations.py
python scripts/export_model_stack_simulation_table.py
python scripts/run_baseline_comparison.py
python scripts/export_evoguard_vs_baselines.py
python scripts/plot_model_stack_simulations.py
~~~

### Expected output files

~~~text
results/tables/model_stack_simulation_summary.csv
results/tables/baseline_comparison.csv
results/tables/evoguard_vs_baselines.csv
~~~

### Determinism

- Core experiments are simulation-based
- No API calls are required for main results
- Benchmark inputs are versioned in the repository
- Search settings are controlled through YAML configuration files

### Hardware

- CPU-only execution is sufficient for main simulation experiments
- Optional real-model adapters may require API access or local GPU depending on model choice

### External dependencies

- None required for core simulation results
- Optional dependencies required only for real-model adapter experiments

---

## Paper Alignment

This repository maps directly to the paper structure:

- **Methodology**: `src/guardrail_gym/search/`, `src/guardrail_gym/eval/`
- **Benchmark setup**: `examples/benchmark.*.yaml`
- **Guardrail architecture space**: `risk_ontology/`
- **Experiments**: `scripts/run_model_stack_simulations.py`, `scripts/run_baseline_comparison.py`
- **Results**: `results/tables/`, `results/plots/`

---

## Limitations

The primary results are simulation-based. Model profiles do not replace full live model behavior. Control effects and interactions are approximated through structured simulation rules.

The framework is intended to support:

- large-scale guardrail architecture search in simulation
- controlled comparison across risk environments
- subsequent validation on real model outputs

---

## Anonymity

This repository is anonymized for peer review. It avoids author names, affiliations, personal paths, and non-anonymous commit history.

---

## License

MIT
