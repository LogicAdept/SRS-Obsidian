<!--
reps: 0
priority: 0
-->
#MachineLearning/Regularization #SRS

# What is a regularization term

> [!abstract] Short answer
> A regularization term is a **penalty added to the training loss that grows with model complexity** — typically the sum of squared or absolute weights. The optimizer now trades fit against size, which shrinks coefficients, damps overfitting, and turns ill-posed problems into solvable ones.

The objective becomes `average loss + λ · penalty(θ)`. The weight `λ` is a hyperparameter: zero recovers pure fitting, large `λ` forces a nearly empty model. The two canonical penalties are the L2 norm (ridge, squares of weights) and the L1 norm (lasso, absolute values, which zeroes parameters outright) — compared in [[What is the difference between L1 and L2 regularization]].

## Why it works

Overfitting often manifests as huge coefficients that twist the model to chase noise: a tiny training loss bought with wild parameters. The penalty makes wild parameters expensive, so the optimizer prefers the smoothest function consistent with the data — an implementation of Occam's razor that is actually differentiable and tunable. The capacity story behind it is [[What is the bias-variance tradeoff]]; the symptom it treats is [[What is overfitting]].

```python
from sklearn.linear_model import Ridge, Lasso

ridge = Ridge(alpha=1.0).fit(X_tr, y_tr)    # alpha = lambda, L2 penalty
lasso = Lasso(alpha=0.1).fit(X_tr, y_tr)    # L1: many coefs become exactly 0
import numpy as np
print("ridge |w|:", np.abs(ridge.coef_).max(), "lasso zeros:", (lasso.coef_ == 0).sum())
```

**Listing 1.** Same data, two penalties: ridge shrinks all coefficients, lasso drives a subset to exactly zero and thus performs selection.

## Beyond linear-model penalties

The idea generalizes: weight decay in neural networks is L2 by another name (and in frameworks like PyTorch, `weight_decay` lives in the optimizer), dropout adds noise rather than a norm term but serves the same goal — [[What is dropout]]; early stopping caps complexity over training time — [[What is early stopping]]; tree methods penalize leaf counts and leaf values — gradient boosting's regularized objective is central to [[What is gradient boosting]] and [[What is the difference between XGBoost LightGBM and CatBoost]].

```d2
direction: right
loss: "Data loss\nfit the sample" { width: 160; height: 80 }
pen: "Penalty lambda * R(theta)\npunish complexity" { width: 190; height: 80 }
obj: "Objective\nloss + penalty" { width: 170; height: 80 }
fit: "Small bias\nhigh variance" { width: 160; height: 70 }
bal: "Balanced fit\nregularized" { width: 160; height: 70 }
loss -> obj; pen -> obj; obj -> bal
loss -> fit { style.stroke: "#b71c1c" }
```

**Fig. 1.** Data loss alone chases the sample (red path); adding the complexity penalty balances fit against variance.

> [!warning] Interview trap
> "Regularization always improves the test score." It improves it up to a point; too large a `λ` underfits as surely as none overfits — the term trades bias for variance, see [[What is underfitting]]. Also, penalties operate on scale: features must be standardized or the penalty silently punishes some coefficients merely because of units.

> [!tip] Interview answer
> A regularization term is a complexity penalty appended to the loss, weighted by lambda — L2 shrinks weights smoothly, L1 zeroes them for feature selection. I would connect it to the bias-variance tradeoff, note that neural networks get the same effect via weight decay, dropout, and early stopping, and remind that features must be scaled for the penalty to be fair.

