<!--
reps: 0
priority: 0
-->
#MachineLearning/Metrics #SRS

# What is the difference between precision and recall

> [!abstract] Short answer
> Precision answers **"of what I flagged, how much was right?"** — TP / (TP + FP). Recall answers **"of what existed, how much did I catch?"** — TP / (TP + FN). Precision penalizes false alarms; recall penalizes misses. They trade against each other through the decision threshold, and which one dominates is a business question, not a modeling preference.

The confusion quadrants: true positives (flagged and real), false positives (flagged, wrong — precision's cost), false negatives (missed, real — recall's cost), true negatives. Raising the threshold makes the model pickier: precision rises, recall falls. Lower it and the directions reverse — the full curve view is in [[What is ROC AUC]] and [[When is PR AUC better than ROC AUC]].

## The cost framing decides

* **Precision-critical:** spam filtering (a lost letter is worse than a spam in inbox), auto-moderation with irreversible bans, automated payouts — every false positive has a real victim.
* **Recall-critical:** cancer screening, fraud detection, safety incidents — a missed case is the disaster; false alarms only cost review effort.
* **Balanced:** F1 = harmonic mean of the two — punishes lopsided results more than the arithmetic mean; but F1 is a convention, not a goal: state which error hurts and by how much.

```python
from sklearn.metrics import precision_score, recall_score, f1_score, precision_recall_curve

print(precision_score(y_te, pred), recall_score(y_te, pred), f1_score(y_te, pred))
probs = clf.predict_proba(X_te)[:, 1]
prec, rec, thr = precision_recall_curve(y_te, probs)
# pick the threshold that matches the business tolerance, not 0.5 by default
```

**Listing 1.** Metrics come from scikit-learn; the threshold choice via the PR curve is where the business decision lives — 0.5 is a default, not a decision.

```d2
direction: right
all: "all actual positives" { width: 200; height: 70 }
tp: "flagged correctly\n(TP)" { width: 170; height: 70 }
fn: "missed\n(FN)" { width: 130; height: 70 }
flag: "everything flagged" { width: 190; height: 70 }
all -> tp; all -> fn { style.stroke: "#b71c1c" }
flag -> tp
```

**Fig. 1.** Recall is the solid path into TP out of all positives; precision is the share of TP inside everything flagged — the red edge is the miss recall punishes.

> [!warning] Interview trap
> "High precision means a good model." At a brutal threshold, precision approaches 1 while recall approaches 0 — you flag one easy case and stop. Any single one of the two is gameable; only the pair (or a curve) tells the story. Second trap: quoting precision/recall without the class base rate — on 1%-positive data, 95% precision is impressive, 95% **recall with 30% precision** may be worthless: [[How do you handle class imbalance]].

> [!tip] Interview answer
> Precision is the purity of what I flagged, recall is the coverage of what exists; they trade through the threshold. I would anchor with the business cost — false alarms versus misses — say F1 is a shorthand, not a goal, and mention that I choose the operating threshold from the precision-recall curve against that cost, never by defaulting to 0.5.

