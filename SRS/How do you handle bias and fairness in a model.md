<!--
reps: 0
priority: 0
-->
#MachineLearning/MLOps #SRS

# How do you handle bias and fairness in a model

> [!abstract] Short answer
> Fairness work starts with naming the harm and the groups: audit **performance and error rates per group**, choose a fairness criterion appropriate to the decision (equalized error rates, calibration within groups, demographic parity where it legally applies), mitigate through data, training, and thresholds, and keep monitoring group metrics in production. Fairness is a specification, not a vibe — every criterion is a mathematical constraint, some mutually exclusive.

Bias sources: historical labels encode past decisions (a hiring model trained on past hires learns past discrimination), sampling under-covers groups, measurement differs across groups (proxy variables: ZIP code for race, part-time for gender), and feedback loops amplify: the model's decisions create the next training data.

## The criteria problem — the heart of the topic

* **Independence (demographic parity):** positive rates equal across groups — appropriate when the decision itself is questionable; ignores legitimate differences.
* **Separation (equalized odds):** equal error rates across groups given the true label — appropriate when the ground truth is meaningful; usually violates parity when base rates differ.
* **Calibration within groups:** a 0.7 means 0.7 in every group — appropriate for risk communication; incompatible with equalized odds when prevalence differs (the impossibility results).

You must pick, justify, and document — the choice is ethical and legal, not technical optimization. Legal context (US disparate treatment/impact, EU/GDPR and the AI Act) may constrain which criteria and mitigations are even permitted; "fairness through unawareness" (dropping the protected attribute) fails because proxies reconstruct it.

## The engineering loop

1. **Audit:** per-group confusion matrices and calibration: [[What is a confusion matrix]]; compare error directions — who gets false positives (over-policed, denied) and who gets false negatives (overlooked, under-served): [[What is the difference between precision and recall]].
2. **Mitigate by stage:** data (rebalance sampling, reweigh labels), representation (avoid proxy features where justified), training (fairness-constrained or adversarial debiasing objectives, group-aware losses), post-processing (group-specific thresholds where legally permissible).

```text
audit:   confusion matrix + calibration per group
fix:     data -> representation -> training -> thresholds
monitor: group metrics dashboards + drift alerts + model card updates
```

**Listing 1.** The fairness loop as an operational checklist: audit per group, mitigate by stage, keep watching — it is a lifecycle, not a patch.

3. **Monitor in production:** fairness metrics as first-class dashboards with alerting — drift is not distribution-neutral: [[How do you monitor a model in production]]; the governance wrap is [[What is MLOps]].
4. **Document:** model cards / datasheets recording data provenance, intended use, evaluated groups, and known gaps — [[What is the machine learning lifecycle]] accountability.

> [!warning] Interview trap
> "Removing the protected attribute makes the model fair." Proxies (ZIP, device, name embeddings) restore the signal, and the model still inherits label bias — unawareness is not fairness. Second trap: "there is one fairness metric; we optimized it" — the criteria conflict mathematically; claiming a single number "fair" without stating the chosen criterion and its trade-offs is exactly the answer interviewers are trained to reject.

> [!tip] Interview answer
> I start by naming the harm and choosing a fairness criterion explicitly — parity of outcomes, equalized error rates, or within-group calibration — because they are mutually incompatible and the choice is a policy decision. Then audit per-group errors and calibration, mitigate across data, training, and thresholds, and monitor group metrics in production with documentation. Dropping the protected attribute is not a mitigation; proxies and label bias remain.

