<!--
reps: 0
priority: 0
-->
#MachineLearning/Supervised #SRS

# What is an SVM

> [!abstract] Short answer
> A support vector machine finds the **maximum-margin boundary between classes**: the hyperplane that separates the classes with the widest possible buffer. Only the points closest to the boundary — the support vectors — determine it. Kernels extend this to non-linear boundaries, and the soft-margin parameter `C` trades margin width against violations.

The maximum-margin idea is why SVMs generalize well in medium-dimensional spaces: instead of any separating plane, they demand the thickest one, which is a form of capacity control built into the objective: hinge loss plus an L2 penalty on weights — the regularized-loss pattern from [[What is a loss function]] and [[What is a regularization term]].

## Mechanics

Training solves a convex quadratic program: minimize `½||w||² + C Σ ξᵢ` subject to `yᵢ(w·xᵢ + b) ≥ 1 − ξᵢ`. Slack variables `ξᵢ` allow margin violations; `C` prices them — large `C` hates violations (narrow margin, overfit risk), small `C` tolerates them. Points with `ξ = 0` strictly outside the margin do not affect the solution at all — that is the sparsity of support vectors.

The **kernel trick** replaces inner products `x·z` with a kernel `K(x, z)` (RBF, polynomial), implicitly mapping data into a higher-dimensional space without computing it: an RBF-SVM draws smooth closed boundaries in the original space. scikit-learn's `SVC(kernel="rbf", gamma="scale", C=1.0)` is the canonical call.

```python
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline

clf = make_pipeline(
    StandardScaler(),                  # distances drive kernels: scale!
    SVC(kernel="rbf", C=1.0, gamma="scale"),
).fit(X_tr, y_tr)
```

**Listing 1.** The RBF-kernel SVM recipe; `gamma="scale"` sizes the kernel width from the data, and scaling is not optional because kernels compute distances.

## When SVMs shine and when they lose

Shine: small-to-medium datasets, high-dimensional but not huge sample counts, clear-margin problems, text with linear kernels. Lose: very large `n` (training scales worse than linear models or trees — kernel SVMs are superlinear), noisy overlapping classes (margin is everything, outliers hurt), and when you need calibrated probabilities (SVM outputs distances; Platt scaling is a bolt-on). Gradient-boosted trees beat kernel SVMs on most tabular problems today: [[What is gradient boosting]].

> [!warning] Interview trap
> "SVMs are obsolete." Linear SVMs remain strong baselines for high-dimensional sparse text. The more common trap: forgetting to scale features — for kernels, unscaled data silently warps distances and the model underperforms mysteriously. And "support vectors are the misclassified points" is wrong: they are the points **on or inside the margin** that pin the boundary.

> [!tip] Interview answer
> An SVM learns the maximum-margin hyperplane with hinge loss and L2 penalty, where only the support vectors define the boundary and C prices margin violations. Kernels like RBF give non-linear boundaries implicitly, which makes feature scaling critical. I would position it: excellent on medium-sized, high-dimensional problems, weak on huge n and noisy overlap, and usually outclassed on tabular data by gradient boosting.

