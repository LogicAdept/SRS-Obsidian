<!--
reps: 0
priority: 0
-->
#MachineLearning/Regularization #SRS

# What is the bias-variance tradeoff

> [!abstract] Short answer
> Expected prediction error decomposes into **bias** (systematic error from a model too simple for the pattern), **variance** (sensitivity to the particular training sample — a model too flexible chases noise), and irreducible noise. Increasing capacity lowers bias and raises variance; the craft is choosing the capacity point — and the regularization — that minimizes their sum.

Concretely: fitting a linear model to a curved relationship gives high bias — the shape cannot be represented regardless of data. Fitting a deep tree to a small noisy sample gives high variance — a different sample yields a different tree. The decomposition: error = bias² + variance + σ², where σ² is noise no model removes.

## Reading it in practice

* **Symptom of high bias:** train and validation errors both high and close — the model cannot fit even the training data: [[What is underfitting]].
* **Symptom of high variance:** train error low, validation error high and the gap large — memorization: [[What is overfitting]].
* **The levers for variance:** more data (the only real cure), regularization — [[What is the difference between L1 and L2 regularization]], [[What is dropout]], [[What is early stopping]], ensembling — [[What is a random forest]].
* **The levers for bias:** richer model class, better features — [[What is feature engineering]], more training.

```d2
direction: right
under: "simple model\nhigh bias, low variance\nunderfits" { width: 200; height: 90 }
sweet: "right capacity\nbalanced\nminimum total error" { width: 200; height: 90 }
over: "complex model\nlow bias, high variance\noverfits" { width: 200; height: 90 }
under -> sweet -> over
```

**Fig. 1.** Total error is U-shaped in capacity: bias falls on the left, variance rises on the right; the goal is the valley, found via validation.

## Modern nuances worth saying

Deep learning blurs the classical picture: over-parameterized networks trained with SGD can have low test error despite theoretically huge variance — the "double descent" phenomenon, where the U-curve dips again past the interpolation threshold. Implicit regularization of optimizers (SGD noise, early stopping) and explicit regularization co-exist. Still, as a diagnostic frame — "is my gap a fit problem or a data problem?" — the tradeoff remains the first tool reached for, and cross-validation is how the valley is located empirically: [[What is cross-validation]].

> [!warning] Interview trap
> "More data fixes everything." More data tames variance, not bias — a model family that cannot represent the pattern stays wrong no matter how many rows you feed it. Second trap: "regularization is always good" — regularization adds bias by design; overdo it and you slide from overfitting into underfitting, which is the same U-curve read backwards.

> [!tip] Interview answer
> Expected error splits into bias, variance, and noise: capacity reduces the first and amplifies the second, and validation finds the valley. I diagnose by the train–validation gap — both high means bias, a wide gap means variance — then pick levers accordingly: features and model class for bias, more data, regularization, ensembling, and early stopping for variance. I would mention double descent as the modern caveat without discarding the frame.

