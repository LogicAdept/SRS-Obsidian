<!--
reps: 0
priority: 0
-->
#MachineLearning/MLOps #SRS

# What is data drift

> [!abstract] Short answer
> Data drift is a **change in the input distribution** the model serves — P(X) moves away from training P(X). Concept drift is the deeper cousin: the input–output relationship P(y|X) changes (same-looking customers, different churn behavior). Both silently degrade a frozen model, because a model is only as valid as the distribution it was fitted on.

Distinguish the flavors: covariate shift (inputs move), label shift (class proportions move), concept drift (the mapping moves), and upstream data changes — a renamed field, a new app version, a broken sensor, which masquerades as drift but is a data bug. The remedy differs: bugs need fixes, drift needs retraining policies, concept drift needs model or feature redesign.

## How it is detected

* **Input monitoring:** compare live feature distributions to training references — PSI (population stability index), KL/JS divergence, Kolmogorov–Smirnov tests per feature, embedding-distance methods for unstructured inputs.
* **Prediction monitoring:** score distributions shift before outcomes do; a sudden change in predicted-positive rate is an early alarm.
* **Outcome monitoring (the honest one):** actual labels when they arrive — delayed ground truth (chargebacks, churn) turns quality monitoring into a lagging indicator; proxy metrics fill the gap: [[How do you monitor a model in production]].
* **Segmented monitoring:** aggregate stability hides per-segment collapse; slice by geography, device, product line.

```python
import numpy as np

def psi(expected, actual, bins=10):
    edges = np.quantile(expected, np.linspace(0, 1, bins + 1))
    e = np.histogram(expected, edges)[0] / len(expected)
    a = np.histogram(actual, edges)[0] / len(actual)
    e, a = np.clip(e, 1e-6, None), np.clip(a, 1e-6, None)
    return float(np.sum((a - e) * np.log(a / e)))
# PSI < 0.1 stable, 0.1-0.25 watch, > 0.25 action
```

**Listing 1.** PSI in ten lines: the workhorse scalar for feature drift, with the conventional action thresholds.

## What to do when it fires

Triage first: bug (schema, pipeline), drift, or concept drift — the retraining reflex without triage bakes bugs into the next model. Then retrain on recent data with the same discipline as the original — the loop of [[What is the machine learning lifecycle]]; tighten features if the shift broke their meaning; and set explicit retraining cadence or trigger thresholds as a policy, not a panic response: [[What is MLOps]]. Watch feedback loops too — the model's own actions change the data it later sees (a fraud model that blocks patterns makes them rarer), which is drift with an agency twist.

> [!warning] Interview trap
> "Data drift and concept drift are the same." Inputs moving and the input–target relationship moving are different failures: retraining on fresh data fixes the first, and can be useless against the second if the target semantics changed. Second trap: "we monitor accuracy" — with delayed labels, accuracy is weeks late; input and prediction monitors exist because ground truth lags, and precision in the wild is the thing dying quietly.

> [!tip] Interview answer
> Data drift is the input distribution moving away from training; concept drift is the target relationship changing — different failures with different remedies. I monitor inputs with PSI-style statistics and embedding distances, watch prediction distributions for early warning, and reconcile with delayed labels where possible — segmented, not just aggregate. On trigger I triage bug versus drift before retraining, and the retraining policy itself is written down, not improvised.

