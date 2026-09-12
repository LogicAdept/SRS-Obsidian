<!--
reps: 0
priority: 0
-->
#MachineLearning #SRS

# What is machine learning

> [!abstract] Short answer
> Machine learning is a family of algorithms that **choose their behavior from data instead of being programmed rule by rule**. You give the algorithm examples (features plus, usually, outcomes), it tunes internal numbers to minimize a loss, and the result is a model that predicts or decides on inputs it has never seen.

The classical definition is Tom Mitchell's: a program learns from experience E with respect to task T and performance measure P if its performance at T, measured by P, improves with E. In practice E is the training set, T is prediction or decision-making, and P is a metric such as accuracy, log loss, or revenue uplift.

## Where the line with programming sits

In traditional software the developer writes the function `f` by hand: input goes in, deterministic rules produce output. In ML you write the **shape** of `f` (a linear model, a tree ensemble, a neural network) and the training procedure, and data determines the actual parameters. This is why ML quality is dominated by data quality and coverage rather than by clever code: a garbage training set produces a confidently wrong model, not an exception.

## The three families

* **Supervised** — you have labeled pairs `(x, y)` and learn a mapping. Classification and regression live here.
* **Unsupervised** — you have only `x` and look for structure: clusters, dimensions, densities.
* **Reinforcement** — an agent acts in an environment and learns from delayed reward signals.

The split matters because it decides what loss you can even define. See [[What is the difference between supervised unsupervised and reinforcement learning]] for the trade-offs.

## The production loop

```d2
direction: right
data: "Collect & label\ndata" { width: 170; height: 80 }
train: "Train model\nminimize loss" { width: 160; height: 80 }
eval: "Evaluate on\nheld-out data" { width: 160; height: 80 }
deploy: "Deploy &\nserve predictions" { width: 170; height: 80 }
monitor: "Monitor drift\n& metrics" { width: 160; height: 80 }
data -> train -> eval -> deploy -> monitor
monitor -> data: "retrain loop" { style.stroke: "#b71c1c" }
```

**Fig. 1.** A deployed model is not the end: monitoring feeds back into data collection and retraining, because the world keeps moving under a frozen model.

A one-shot demo notebook is not machine learning in production; the loop above is. The operational half of the loop is covered in [[What is the machine learning lifecycle]] and [[What is MLOps]].

> [!warning] The popular lie
> "ML is AI that figures everything out by itself." It does not. The learning objective, the features, the evaluation protocol, and the deployment plan are all human decisions, and each of them is a standard failure point. A model optimizes exactly the loss you gave it, not the outcome you meant — see [[What is data leakage in machine learning]] for the classic way this goes wrong.

> [!tip] Interview answer
> Machine learning means systems that improve at a task from data by optimizing an explicit objective, rather than following hand-written rules. I would frame it as supervised, unsupervised, and reinforcement settings sharing one core loop: fit parameters to data, evaluate on data the model never saw, deploy, and monitor. The hard part in production is rarely the algorithm — it is data quality, drift, and honest evaluation.

