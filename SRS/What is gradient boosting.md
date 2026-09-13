<!--
reps: 0
priority: 0
-->
#MachineLearning/Ensembles #SRS

# What is gradient boosting

> [!abstract] Short answer
> Gradient boosting builds an additive model **stage by stage: each new tree is fitted to the negative gradient of the loss with respect to current predictions** — a form of functional gradient descent. Start from a constant, compute residuals-like gradients, fit a small tree to them, take a small step (learning rate), repeat. Squared error makes the gradients literally residuals; other losses generalize the idea.

The insight: instead of optimizing parameters by gradient descent, optimize **the prediction function itself** — each tree is one gradient step in function space. This works with any differentiable loss: squared, absolute, Huber, cross-entropy, ranking losses — the loss-flexibility that bagged forests lack.

## The loop

```text
F0 = constant minimizing the loss
for m in 1..M:
    r_i = -[dL/dF(x_i)] at F_{m-1}(x_i)        # pseudo-residuals
    fit tree h_m to (x_i, r_i)                  # shallow tree, few leaves
    F_m = F_{m-1} + lr * h_m
```

**Listing 1.** The core loop: pseudo-residuals, a small tree fitted to them, a shrinkage step. Learning rate and M are in tension — small steps need more stages.

```python
from sklearn.ensemble import GradientBoostingRegressor

reg = GradientBoostingRegressor(
    n_estimators=300, learning_rate=0.05,
    max_depth=3, subsample=0.8, random_state=0,
).fit(X_tr, y_tr)
```

**Listing 2.** The canonical hyperparameters: shallow trees (depth 3), small learning rate with more stages, row subsampling (stochastic boosting) — and early stopping via `n_iter_no_change` for the modern variant, matching [[What is early stopping]].

## Why shallow trees and shrinkage

Weak learners (depth 3–6) keep each step conservative: the ensemble interpolates smoothly rather than memorizing. Shrinkage (learning rate < 0.1) plus more stages reliably outperforms big steps — the same bias-variance discipline as [[What is the bias-variance tradeoff]]. Subsampling rows decorrelates trees, borrowing a page from bagging: [[What is the difference between bagging and boosting]]. The production-grade implementations add second-order information and regularized objectives — that lineage is [[What is the difference between XGBoost LightGBM and CatBoost]].

> [!warning] Interview trap
> "Each tree predicts the target." No — each tree predicts the **gradient of the loss**, which under squared error happens to equal the residual; under cross-entropy it does not. Second trap: "more trees always help" — without shrinkage and early stopping, adding stages past the validation optimum keeps fitting noise; the validation curve turns up while train loss keeps dropping: [[What is overfitting]].

> [!tip] Interview answer
> Gradient boosting is functional gradient descent: start from a constant, repeatedly fit a shallow tree to the loss's negative gradient, and add it with a small learning rate. It accepts any differentiable loss, which is why one algorithm covers regression, classification, and ranking. The quality levers are shallow trees, shrinkage, subsampling, and early stopping — and its industrial-strength descendants are XGBoost, LightGBM, and CatBoost.

