<!--
reps: 0
priority: 0
-->
#MachineLearning/Supervised #SRS

# What is feature engineering

> [!abstract] Short answer
> Feature engineering is **transforming raw data into model inputs that make the pattern easy to learn**: aggregations, ratios, date decompositions, encodings, domain ratios, interaction terms. The features bound what any model can extract, so on tabular problems thoughtful engineering often beats algorithm swaps.

The core question is always: "what representation would make the relationship nearly linear / nearly monotone / nearly separable?" For linear models the answer is transformations that linearize; for trees the answer is less (trees find splits themselves, but still benefit from aggregations and ratios they cannot invent); for neural networks, normalization and meaningful embeddings.

## The standard toolkit

* **Aggregations over history:** mean spend per user per 30 days, counts, rates, time-since-last-event. This is where most tabular signal lives.
* **Decomposition:** dates into day-of-week, hour, holiday flags; strings into lengths, categories, flags.
* **Encoding:** one-hot for low-cardinality categories, target/CatBoost-style encodings carefully (with leakage guards), embeddings for high cardinality — [[What is one-hot encoding versus embeddings]].
* **Scaling and transforms:** standardization, log-transforms for heavy tails — needed for distance- and gradient-based models; see [[What is a design matrix]].
* **Interactions:** products and ratios of features the model cannot combine on its own (linear models especially).

```python
df["spend_30d"] = df.groupby("user_id")["amount"].transform(
    lambda s: s.rolling("30D").sum())
df["is_weekend"] = df["ts"].dt.dayofweek >= 5
df["log_amount"] = np.log1p(df["amount"])
df["spend_per_visit"] = df["spend_30d"] / df["visits_30d"].clip(lower=1)
```

**Listing 1.** Typical engineered features: a rolling aggregate, calendar flags, a stabilizing log, and a ratio — each encodes a hypothesis about the target.

## The production half

Every engineered feature must be computable **at scoring time from data available then**, using only the past — otherwise it is leakage: [[What is data leakage in machine learning]]. Features must be defined identically in training and serving or you get skew; keeping those definitions in sync is an MLOps problem — [[What is MLOps]], [[What is the machine learning lifecycle]]. Aggregates over drifting windows also need point-in-time correctness to be reproducible.

> [!warning] Interview trap
> "Deep learning made feature engineering obsolete." For raw perception (images, audio, text) representations are learned; for tabular business data, engineered aggregates, recency, and ratios remain the main lever — gradient-boosted trees over engineered features still beat generic nets there. Opposite trap: engineering features on the full dataset before splitting (fitting encoders or aggregations with future rows) — that is textbook leakage.

> [!tip] Interview answer
> Feature engineering is building inputs that expose the signal: historical aggregates, calendar decompositions, encodings, ratios, and interactions. I would say it is hypothesis-driven — each feature encodes a belief about the target — that tabular problems are usually won here rather than by exotic models, and that the two disciplines are availability at prediction time and identical definitions in training and serving.

