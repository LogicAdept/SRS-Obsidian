<!--
reps: 0
priority: 0
-->
#MachineLearning/LLM #MachineLearning/MLOps #SRS

# How does LLMOps differ from MLOps

> [!abstract] Short answer
> Same skeleton — versioning, deployment, monitoring, retraining — but the object differs: LLMOps manages **frozen foundation models adapted by prompts, retrieval, and light fine-tunes**, evaluated by rubric-based and human judgment rather than single metrics, monitored for hallucination, injection, and cost/latency budgets, with evaluation pipelines and prompt/version governance replacing big training runs as the core activity.

In classic MLOps the team trains the model; in LLMOps the model is usually someone else's — the engineering moves to the surrounding system: prompts, retrieval corpora, guardrails, caching, routing between models. The unit under version control widens: prompt templates, retrieval indexes, adapter weights, and eval suites all become versioned artifacts — the artifact view of [[What is a model in machine learning]] stretched to its logical end.

## What changes concretely

* **Evaluation.** No single accuracy: layered evals — task metrics where verifiable, LLM-as-judge with rubrics, human review — run as regression suites on every prompt or model change: [[How do you evaluate an LLM]]. The eval set is the new test set, and prompt iteration is the new hyperparameter tuning: [[What is hyperparameter tuning]] analog.
* **Knowledge management.** Fresh and private knowledge arrives via retrieval, not retraining — index pipelines, chunking quality, and retrieval metrics become production concerns: [[What is retrieval augmented generation]].
* **Adaptation weight.** Fine-tuning shrinks to LoRA-scale adapters: [[What is LoRA]] — cheap, swappable, but creating a fleet-versioning problem (base model × adapter × prompt).
* **Safety and security.** Prompt injection, jailbreaks, and unsafe outputs join the threat model as first-class monitored failure classes: [[What is prompt injection]]; hallucination rate is a tracked quality metric: [[What is an AI hallucination]].
* **Cost and latency engineering.** Token-priced APIs make cost a first-class SLO; KV-cache management, batching, caching, and model routing (small model first, escalate) are the performance levers: [[What is the KV cache in LLM inference]].
* **Monitoring.** Beyond drift: output quality sampling, refusal rates, injection attempts, per-tenant spend — [[How do you monitor a model in production]] with LLM-specific signals.

```d2
direction: right
mlops: "MLOps\ntrain -> deploy -> monitor\nmodel = your weights" {
  width: 260; height: 100
}
llmops: "LLMOps\nprompt + retrieval + guardrails -> deploy -> eval\nmodel = frozen base + artifacts" {
  width: 300; height: 100
}
mlops -> llmops: "foundation models" { }
```

**Fig. 1.** The center of gravity moves from training pipelines to evaluation and governance around a frozen base.

> [!warning] Interview trap
> "LLMOps replaces MLOps." The underlying disciplines — versioning, staged rollout, drift response, governance — carry over; what changes is the object and the failure classes. Second trap: "no training means no data problems" — retrieval corpora quality, chunking, and label-lagged feedback on outputs are the new data engineering, and retrieval drift is the new data drift.

> [!tip] Interview answer
> LLMOps keeps the MLOps skeleton but moves the work: the base model is frozen, so versioning and iteration shift to prompts, retrieval indexes, adapters, and guardrails; evaluation becomes layered rubric and human-in-the-loop regression testing; monitoring adds hallucination, injection, and cost per request alongside drift. Training shrinks to light adaptation — the heavy lifting is evaluation, knowledge pipelines, and governance.

