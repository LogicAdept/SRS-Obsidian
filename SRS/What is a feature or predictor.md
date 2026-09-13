<!--
reps: 0
priority: 0
-->
#MachineLearning #SRS

# What is a feature or predictor

> [!abstract] Short answer
> A feature (predictor, input variable, covariate) is **one measurable attribute of an observation that the model consumes as input**. Features are the columns of the design matrix; everything the model can possibly learn is a function of them, which is why feature choice and construction bound model quality.

"Predictor" emphasizes the role: inputs used to predict the target. The same raw column can be used raw, transformed, or combined — those are all features. The craft of turning raw domain data into informative model inputs is [[What is feature engineering]].

## What a feature must be

* **Available at prediction time.** A feature computed after the answer is known is leakage, not signal: [[What is data leakage in machine learning]].
* **Consistently defined.** Same units, same scale, same meaning across train and future data; otherwise you get training-serving skew.
* **Informative for the target** — directly or through interactions a model can exploit.

```python
import pandas as pd

df["tenure_days"] = (df["snapshot_date"] - df["signup_date"]).dt.days
df["amount_z"] = (df["amount"] - df["amount"].mean()) / df["amount"].std()
df = pd.get_dummies(df, columns=["country"], drop_first=True)
X = df[["tenure_days", "amount_z", "country_DE", "country_RU"]]
```

**Listing 1.** Raw columns become features: a duration, a standardized amount, one-hot encoded categories. The transformations are part of the model and must be replayed identically at serving time.

## Feature vs raw data

Raw logs, text, and images are not features yet — they are sources. A feature is the result of a deterministic preparation step: extracting, aggregating, encoding, scaling. For categorical variables the encoding decision is itself modeling: one-hot versus learned vectors is compared in [[What is one-hot encoding versus embeddings]]. Redundant or irrelevant features mostly cost variance; dimensionality reduction like [[What is PCA]] trades interpretability for compactness.

> [!warning] Interview trap
> "More features never hurt." They do: irrelevant features add variance, blur distance metrics, and increase overfitting risk, especially with small `n` and flexible models. And the strongest-looking feature is often the deadliest — anything computed with knowledge of the target (post-outcome aggregates, future timestamps) inflates offline scores and collapses in production.

> [!tip] Interview answer
> A feature is one input attribute of an observation after all preparation — the columns the model actually sees. I would say the two failure modes to check are availability at prediction time (leakage) and stable definition between training and serving, and that feature engineering usually beats algorithm tweaking when quality is capped.

