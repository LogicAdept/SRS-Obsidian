<!--
reps: 0
priority: 0
-->
#MachineLearning/MLOps #SRS

# How do you monitor a model in production

> [!abstract] Short answer
> Monitor four layers: **system health** (latency, errors, throughput), **input data** (drift and schema violations: [[What is data drift]]), **model behavior** (score distributions, prediction rates per segment), and **outcomes** (business metrics and delayed ground truth). Add alerting with thresholds someone owns, and a retraining/rollback runbook the alerts trigger.

The layers exist because failures announce themselves at different speeds: infrastructure breaks loudly and instantly; drift degrades silently over weeks; outcome decay surfaces last — when the business feels it. A monitoring stack that only watches system metrics is blind to exactly the failures unique to ML.

## The stack

* **System:** p50/p99 latency, error rates, GPU utilization, queue depths — standard observability, still the first pager.
* **Data quality and drift:** schema checks (nulls, ranges, categories), PSI/KS per feature, embedding drift for text/image inputs; upstream-change detection ("did the app release change event shapes?").
* **Model behavior:** prediction distribution and calibration over time; per-segment prediction rates; confidence histograms — a shift in scores without an input shift is its own red flag.
* **Outcomes:** label-grounded quality when labels arrive (conversion, fraud confirmed, churn realized) — plus **proxy metrics** (acceptance rate, manual-review rate, downstream corrections) to bridge label lag.
* **Fairness slices:** monitor group-level metrics where fairness matters — the bias topic has its own card: [[How do you handle bias and fairness in a model]].

```d2
direction: right
sys: "system\nlatency, errors" { width: 150; height: 75 }
in: "inputs\ndrift, schema" { width: 140; height: 75 }
beh: "predictions\ndistributions, segments" { width: 180; height: 85 }
out: "outcomes\nlabels, business KPI" { width: 160; height: 80 }
sys -> beh { style.stroke: "#9e9e9e" }
in -> beh { style.stroke: "#9e9e9e" }
beh -> out
```

**Fig. 1.** Signals flow left to right, alarm speed flows right to left: system alerts fire in seconds, outcome decay in weeks — the stack must watch all of them.

## Alerts that someone can act on

Every alert needs an owner, a threshold with known false-positive cost, and a runbook action: check pipeline, roll back model, trigger retrain, or freeze. Shadow deployment and A/B with guardrail metrics catch regressions before full rollout — the deployment half of [[What is MLOps]]. Log enough to replay decisions: inputs, versions, scores — the lineage requirement of [[What is the machine learning lifecycle]] — because the first question after any incident is "what did the model see?"

> [!warning] Interview trap
> "We monitor model accuracy in production." Accuracy needs labels; production labels are delayed, partial, and sometimes biased by the model's own decisions — monitoring only what is easy (system metrics) or only what is late (accuracy) both leave the gap where ML failures live. Second trap: aggregate dashboards — a stable overall rate routinely hides a dead segment; slice or miss.

> [!tip] Interview answer
> I monitor system health, input drift and schema, prediction distributions by segment, and outcomes with delayed labels plus proxy metrics in between. Each alert has an owner, a threshold, and a runbook — rollback, retrain, or pipeline check. I would stress segmentation and the label-lag problem: the stack must catch silent statistical decay, not just crashes, and every alert must map to an action someone can execute.

