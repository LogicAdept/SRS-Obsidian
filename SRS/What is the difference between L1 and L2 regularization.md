<!--
reps: 0
priority: 0
-->
#MachineLearning/Regularization #SRS

# What is the difference between L1 and L2 regularization

> [!abstract] Short answer
> L2 (ridge) penalizes the **sum of squared weights** — it shrinks all coefficients smoothly toward zero but rarely to exactly zero. L1 (lasso) penalizes the **sum of absolute weights** — its geometry drives a subset of coefficients to exactly zero, performing feature selection. Both add `λ · penalty` to the loss; the shape of the penalty decides the behavior.

Why L1 zeros and L2 only shrinks: at w = 0, the L1 penalty has constant-magnitude gradient (sign(w)) that pushes exactly to zero and holds; L2's gradient (2w) vanishes near zero, so it decelerates and never quite arrives. Geometrically, the L1 ball's corners intersect the loss contours at sparse solutions; the L2 ball is round and touches them generically off-axis.

## Consequences in practice

* **Feature selection:** L1 zeroes noise features — interpretable sparse models; but among correlated features it picks one arbitrarily (unstable selection), while L2 spreads weight across them — more stable, less sparse.
* **Collinearity:** L2 handles correlated features gracefully (ridge is well-conditioned even with collinear columns); L1 oscillates between correlated twins.
* **Elastic net** mixes both (`l1_ratio` in scikit-learn) — sparsity with group stability.
* **Scaling:** both penalties are unit-sensitive — standardize features or the penalty punishes some coefficients for their units: [[What is a design matrix]].

```python
from sklearn.linear_model import Lasso, Ridge, ElasticNet

lasso = Lasso(alpha=0.1).fit(X_tr, y_tr)          # L1: sparse coefs
ridge = Ridge(alpha=1.0).fit(X_tr, y_tr)          # L2: shrunk coefs
enet = ElasticNet(alpha=0.1, l1_ratio=0.5).fit(X_tr, y_tr)  # mix
import numpy as np
print((lasso.coef_ == 0).sum(), (ridge.coef_ == 0).sum())
```

**Listing 1.** Same data, three penalties; the zero-count line is the whole story — L1 produces zeros, L2 does not.

## Beyond linear models

The same dichotomy runs through deep learning: weight decay is L2 (in optimizers like AdamW it is decoupled from the gradient step — [[What is the difference between Adam and SGD]]), while true L1 sparsity is rare in neural nets because exact zeros need subgradient mechanics. Tree ensembles regularize differently — leaf count and leaf magnitudes — the gradient-boosting objective: [[What is gradient boosting]], [[What is the difference between XGBoost LightGBM and CatBoost]]. The capacity frame behind both penalties: [[What is the bias-variance tradeoff]], and λ is tuned like any hyperparameter: [[What is hyperparameter tuning]].

> [!warning] Interview trap
> "L1 does feature selection, so it is the better regularizer." Selection is a feature, not a free lunch: with correlated features L1 is unstable and can drop the more useful twin; for prediction-only quality, L2 or elastic net usually wins. Second trap: adding L1 to unscaled features — coefficients are then penalized for their units, silently zeroing the wrong features.

> [!tip] Interview answer
> L2 squares the weights and shrinks everything smoothly — stable with correlated features, no zeros; L1 takes absolute values and drives a subset of coefficients exactly to zero — built-in selection but unstable among correlated features. Elastic net mixes both. I standardize features first, tune lambda on validation, and reach for L1 when sparsity and interpretability are the deliverable.

