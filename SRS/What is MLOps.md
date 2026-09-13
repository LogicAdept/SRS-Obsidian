<!--
reps: 0
priority: 0
-->
#MachineLearning/MLOps #SRS

# What is MLOps

> [!abstract] Short answer
> MLOps is the engineering discipline that runs machine learning **as a repeatable production system**: versioned data and models, automated training and deployment pipelines, monitoring of drift and quality, and a retraining loop — the ML-specific extension of DevOps, where the artifact misbehaves statistically, not just functionally.

The difference from classic DevOps: the deployed artifact is a function **fitted to data**, so its correctness is statistical (accuracy degrades), its inputs shift under it (drift), its build needs datasets and experiments rather than just source, and its failures are silent — no exception, just quietly worse predictions. Google's "Rules of Machine Learning" frames the same idea: the infrastructure and monitoring around the model matter more to outcomes than the model's cleverness.

## The pillars

* **Versioning and lineage:** data, features, code, and model weights versioned together; a prediction must be traceable to the exact training snapshot — the artifact view in [[What is a model in machine learning]].
* **Pipelines:** automated train–evaluate–register–deploy flows (with experiment tracking such as MLflow), reproducible builds, CI tests for data schemas and model quality gates.
* **Deployment discipline:** staged rollouts, shadow and canary modes, instant rollback — deployment strategies shared with DevOps, plus ML-specific shadow scoring to compare models on live traffic.
* **Monitoring and retraining:** drift detection, quality metrics, alerting, and a decided retraining policy — see [[What is data drift]] and [[How do you monitor a model in production]].
* **Governance:** feature stores for train/serve consistency, model registry with approvals, audit trails.

```d2
direction: right
data: "data + features\nversioned" { width: 160; height: 80 }
train: "train + eval\nexperiment tracking" { width: 170; height: 80 }
reg: "model registry\nquality gates" { width: 160; height: 80 }
dep: "deploy\nshadow/canary" { width: 150; height: 80 }
mon: "monitor\ndrift + quality" { width: 160; height: 80 }
data -> train -> reg -> dep -> mon
mon -> data: "retrain trigger" { style.stroke: "#b71c1c" }
```

**Fig. 1.** The MLOps loop: versioned data through gated deployment, monitored in production, feeding retraining — automation at every arrow is what separates MLOps from notebooks.

## Where it pays and where it stalls

Pays: any model with real users, especially with feedback loops, regulations, or fast-drifting inputs (fraud, recommendations, pricing). Stalls: one-off analyses and static domains where a yearly manual retrain is honest — MLOps machinery is not a virtue by itself. The lifecycle framing that orders these stages is [[What is the machine learning lifecycle]]; the LLM-specific variant is [[How does LLMOps differ from MLOps]].

> [!warning] Interview trap
> "MLOps is just CI/CD for models." CI/CD is one pillar; the harder parts are data versioning, train/serve consistency, and statistical monitoring — the failure modes (drift, leakage, skew) have no analog in classic software deployment. Second trap: "a deployed model is done" — a frozen model on a moving world is a depreciating asset; the retraining policy is part of shipping it.

> [!tip] Interview answer
> MLOps runs ML as a production system: versioned data and models, automated training and gated deployment pipelines, monitoring for drift and quality, and a retraining loop. I would stress what differs from DevOps — statistical correctness, silent failures, train/serve consistency — and say the maturity signal is automation of the loop, not the fanciness of any single model.

