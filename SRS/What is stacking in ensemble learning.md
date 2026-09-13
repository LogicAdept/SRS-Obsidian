<!--
reps: 0
priority: 0
-->
#MachineLearning/Ensembles #SRS

# What is stacking in ensemble learning

> [!abstract] Short answer
> Stacking (stacked generalization) trains **a meta-model to combine the predictions of diverse base models**: base learners make out-of-fold predictions, and a meta-learner is fitted on those predictions (as features) to learn who to trust, when, and how to interpolate their errors. Unlike bagging and boosting, the combination is learned, not fixed by averaging or addition.

The diversity requirement is the point: stacking pays off when base models are **different in kind** (linear, k-NN, boosted trees, neural net) and fail on different rows. Stacking five gradient boosting variants with different seeds buys almost nothing; stacking trees + linear + neighbors buys calibration and boundary-shape complementarity.

## The leak-free training loop

Naive stacking leaks: if the meta-model trains on base predictions made on rows the base models saw, those predictions are overfit-optimistic and the meta-learner learns garbage weights. The fix is **out-of-fold (OOF) prediction**: split training data into K folds; for each fold, train base models on the other K−1 folds and predict the held-out fold; stack those OOF predictions as the meta-training set.

```text
for fold k in 1..K:
    fit base models on data minus fold k
    predict fold k -> OOF matrix Z_k
meta_model.fit(Z[all folds], y)        # same rows, base-unseen predictions
at serving: base models (refit on full train) -> their predictions -> meta_model
```

**Listing 1.** The K-fold OOF scheme: every meta-training row was predicted by base models that never trained on it — the same discipline as [[What is cross-validation]].

```d2
direction: right
x: "X train" { width: 120; height: 60 }
b1: "base: linear" { width: 140; height: 70 }
b2: "base: GBM" { width: 120; height: 70 }
b3: "base: k-NN" { width: 120; height: 70 }
z: "OOF predictions Z\n(n x 3)" { width: 170; height: 80 }
m: "meta-model\nlogistic / ridge" { width: 160; height: 80 }
x -> b1; x -> b2; x -> b3
b1 -> z; b2 -> z; b3 -> z
z -> m
```

**Fig. 1.** Heterogeneous base learners emit out-of-fold predictions; the meta-model learns the combination on those honest predictions.

## Practice notes

The meta-model is deliberately simple (logistic regression or ridge) — its job is calibration of trust, not another round of pattern-mining on a tiny feature space. Refit base models on the full training set before serving; the meta-model consumes their predictions exactly as trained. Cost: K× the base training, double the evaluation surface — worth it in competitions and high-stakes scoring, often not in latency-sensitive production where a single well-tuned GBM plus calibration is competitive — see [[What is gradient boosting]] and [[What is the machine learning lifecycle]].

> [!warning] Interview trap
> "Stacking leaks, so it is unsafe" — only naive stacking leaks; OOF stacking is the standard cure. The subtler trap: computing OOF predictions but then fitting the meta-model on **test-fold** predictions of base models refit per fold while serving refits on full data — distribution mismatch between Z and serving predictions; the standard mitigation is refitting base learners on full train and (optionally) blending with OOF-fitted meta weights.

> [!tip] Interview answer
> Stacking learns a meta-model on base learners' out-of-fold predictions, so the combination weights are fitted leak-free on predictions made by models that never saw those rows. I would stress diversity of base models as the source of the gain, simplicity of the meta-learner, refitting bases on full data before serving, and that the K-fold cost buys accuracy mainly in competitions and high-value scoring.

