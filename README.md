# EvoGuard

**EvoGuard** is a research framework for studying how **guardrail architectures** should be composed around conversational AI systems operating in regulated and high-risk environments.

This repository accompanies the paper:

> *EvoGuard: Neurogenetic Search of Guardrail Architectures for Risk-Aware Conversational AI Systems*

---

## Overview

Modern conversational AI safety is not solely a property of the base model. In deployed systems, safety emerges from a surrounding **guardrail architecture** composed of heterogeneous controls.

EvoGuard introduces:

- a **benchmark** for evaluating guardrail stacks across regulated risk scenarios  
- a **neurogenetic search algorithm** for evolving guardrail compositions  
- a **multi-objective evaluation framework** incorporating safety, compliance, utility, and deployment constraints  

The system treats guardrails as **composable primitives across layers**, and optimizes their structure under environment-specific constraints.

---

## Key Contributions

- **Guardrail architecture as a first-class object**  
  Safety is modeled as a system-level property, not a model-level property.

- **Neurogenetic search over guardrail stacks**  
  Guardrail configurations are evolved using mutation, crossover, and multi-objective selection.

- **Regulated benchmark environments**  
  Healthcare, finance, and adversarial settings with structured risk annotations.

- **Multi-dimensional evaluation**  
  Metrics include safety, compliance, utility, latency, cost, auditability, and coverage.

- **Model-conditioned simulation**  
  Evaluation across 17 model profiles spanning API, open-weight, and edge deployments.

---

## Repository Structure

```text
src/guardrail_gym/
  benchmark/          scenario definitions and loading
  controls/           guardrail primitive registry
  eval/               simulation and metrics
  search/             EvoGuard evolutionary search
  profiles/           deployment and model profiles
  models/             optional adapters for real models

examples/
  benchmark.*.yaml
  search.*.yaml
  model_simulation_suite.yaml

scripts/
  run_model_stack_simulations.py
  run_baseline_comparison.py
  export_evoguard_vs_baselines.py
  plot_model_stack_simulations.py

results/
  tables/
  plots/
```

---

## Installation

Requires Python 3.10+.

Clone the repository:

```bash
git clone https://github.com/anon0404/evoguard.git
cd evoguard
```

Create environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install:

```bash
python -m pip install -e ".[dev]"
```

Run tests:

```bash
pytest -q
```

---

## Quick Start

Run the full experiment pipeline:

```bash
python scripts/split_regulated_benchmark.py
python scripts/run_model_stack_simulations.py
python scripts/export_model_stack_simulation_table.py
python scripts/run_baseline_comparison.py
python scripts/export_evoguard_vs_baselines.py
python scripts/plot_model_stack_simulations.py
```

---

## Outputs

Main results are written to:

```text
results/tables/model_stack_simulation_summary.csv
results/tables/baseline_comparison.csv
results/tables/evoguard_vs_baselines.csv
```

Plots are saved to:

```text
results/plots/
```

---

## Benchmark Design

### Environments

- **Healthcare (strict)**  
  Safety-critical, escalation-heavy

- **Finance (consumer)**  
  Compliance, fairness, vulnerability-aware

- **Adversarial**  
  Prompt injection, jailbreaks, misuse scenarios

---

### Scenario Annotations

Each scenario includes:

- risk domains  
- vulnerability factors  
- system mode (chat / RAG / agentic)  

---

## Guardrail Architecture Space

EvoGuard composes controls across multiple layers:

### Deterministic
- regex filters  
- schema validators  

### ML-based
- vulnerability classifiers  
- risk detectors  

### LLM-based
- policy judges  
- grounding evaluators  

### Graph-based
- policy routing  
- workflow control  

### Neurosymbolic
- adaptive controllers  
- constraint solvers  

### Oversight
- human escalation gates  

### Monitoring
- audit logging  
- anomaly detection  

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

### Architecture metrics
- Layer diversity  
- Stack-order score  
- Cognitive role coverage  

---

## Baselines

- Unguarded  
- Rules-only  
- Judge-only  
- Graph-only  
- Hybrid manual  

EvoGuard is compared against these baselines under identical evaluation settings.

---

## Model Simulation

We evaluate across 17 model profiles:

- API frontier  
- API cost-optimized  
- Open-weight large  
- Open-weight medium  
- Edge-small  

Models are simulated using:

- capability priors  
- latency and cost models  
- deployment constraints  

No external APIs are required for core experiments.

---

## Optional Real Model Adapters

Adapters are included for:

- OpenAI-compatible models  
- Google Gemini  
- Anthropic Claude  
- Hugging Face models  

Install optional dependencies:

```bash
pip install openai anthropic google-generativeai transformers accelerate
```

---

## Limitations

- Results are primarily simulation-based  
- Control interactions are approximated  
- Real-time conversational dynamics are not fully modeled  

The framework is designed for scalable architecture search, with real-model validation as a subsequent step.

---

## Reproducibility

All results in the paper can be reproduced with:

```bash
python scripts/run_model_stack_simulations.py
python scripts/run_baseline_comparison.py
```

---

## Anonymity

This repository is anonymized for peer review.

All identifying information, commit history, and metadata have been removed.

---

## License

MIT
