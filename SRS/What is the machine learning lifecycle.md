<!--
reps: 0
priority: 0
-->
#MachineLearning/MLOps #SRS

# What is the machine learning lifecycle

> [!abstract] Short answer
> The ML lifecycle is the closed loop every production model lives in: **problem framing → data collection and labeling → feature engineering → training and evaluation → deployment → monitoring → retraining** — and back to data. Unlike a software release, the loop never "finishes": the world moves, labels arrive late, and the deployed model depreciates until re-fed.

The framing stage dominates outcomes and gets the least airtime: defining the target (and its proxy honesty), the unit of an observation, the cost of each error type, and the success metric — everything downstream inherits these choices: [[What is a target variable in machine learning]], [[What is the difference between precision and recall]].

## The stages and their artifacts

* **Framing:** metric definition, error-cost table, constraints (latency, fairness, budget).
* **Data:** collection, labeling, quality audit; the leakage and split discipline set here binds forever: [[What is data leakage in machine learning]], [[What is a train validation test split]].
* **Features:** pipelines that replay identically in training and serving: [[What is feature engineering]].
* **Train/evaluate:** baselines first, then candidates under cross-validation: [[What is cross-validation]]; hyperparameter search: [[What is hyperparameter tuning]].
* **Deploy:** staged rollout with shadow/canary and rollback — the operational machinery: [[What is MLOps]].
* **Monitor/retrain:** drift and outcome monitoring feeding triggers: [[How do you monitor a model in production]].

```d2
direction: right
f: "frame\nmetric + costs" { width: 140; height: 80 }
d: "data\ncollect, label" { width: 130; height: 80 }
fe: "features" { width: 110; height: 70 }
t: "train +\nevaluate" { width: 130; height: 80 }
dep: "deploy\nstaged" { width: 120; height: 75 }
mon: "monitor\ndrift + outcomes" { width: 150; height: 80 }
f -> d -> fe -> t -> dep -> mon
mon -> d: "retrain loop" { style.stroke: "#b71c1c" }
```

**Fig. 1.** The loop is the deliverable: every arrow is an automated, versioned handoff; the red edge is the retraining trigger that keeps the model alive.

## Why the loop framing matters

It reallocates effort: most teams over-invest in the train stage and under-invest in framing, data quality, and monitoring — where production value actually leaks. It also clarifies roles: data engineers own the data arrows, scientists the middle, platform engineers the deployment and monitoring rails — the collaboration map of [[What is MLOps]]. And it makes retirement a first-class decision: models get decommissioned when the loop's economics stop paying.

> [!warning] Interview trap
> "The lifecycle ends at deployment." Deployment starts the responsibility window: without the monitor-and-retrain edge, the diagram is a one-way road to silent decay. Second trap: jumping to training before framing — no model recovers from a wrong target or an unmeasurable success metric; the cheapest fix in ML is deciding the right question.

> [!tip] Interview answer
> The lifecycle is the closed loop: frame the problem and error costs, collect and split data honestly, engineer features, train and evaluate against baselines, deploy in stages, monitor drift and outcomes, and retrain on triggers. I would emphasize that framing and monitoring bookend the glamorous middle and decide its value, and that every arrow should be automated and versioned — the loop, run manually, is where models quietly die.

