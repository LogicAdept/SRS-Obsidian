<!--
reps: 0
priority: 0
-->
#MachineLearning #SRS

# What is a design matrix

> [!abstract] Short answer
> The design matrix `X` is the **`n × p` numeric table where each of the `n` observations is one row and each of the `p` features is one column**. Almost every classical estimator is literally a function of `X` and the target vector `y`, so the design matrix is the concrete interface between your data preparation and the model.

The term comes from statistics (designed experiments) but the object is universal: scikit-learn estimators take exactly `X` of shape `(n_samples, n_features)` and `y` of shape `(n_samples,)`. What "numeric" means is a hard constraint — the matrix holds numbers, so categories, text, and dates must be encoded before they enter it.

## Shape and the standard contract

Row `i` is observation `i`; column `j` is feature `j`. With an intercept term, a column of ones is prepended, making the linear model's matrix `Xβ` well-defined without special-casing the bias. A column of ones is often called `x₀ = 1`.

```python
import numpy as np
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer

ct = ColumnTransformer([
    ("num", StandardScaler(), ["amount", "tenure_days"]),
    ("cat", OneHotEncoder(drop="first"), ["country"]),
])
X = ct.fit_transform(df)          # shape (n_samples, n_features)
assert X.shape[0] == len(y)       # rows align with the target vector
```

**Listing 1.** Building the design matrix with scikit-learn: heterogeneous raw columns are encoded and scaled into one numeric table aligned row-by-row with `y`.

## Why the concept earns its keep

Reasoning about shapes catches bugs early: predictions have shape `(n,)`, one per observation; a `(n, 1)` target with a `(n,)` API call is the classic silent-shape bug. Rank and collinearity of `X` decide whether linear coefficients are even identifiable — two perfectly correlated columns make the solution non-unique, which regularization handles: [[What is the difference between L1 and L2 regularization]]. Dimensionality reduction operates on `X` directly: [[What is PCA]].

```d2
direction: right
raw: "Raw table\nmixed types" { width: 150; height: 80 }
prep: "Encode, scale\nalign rows" { width: 160; height: 80 }
X: "Design matrix X\n(n x p) numeric" { width: 170; height: 80 }
y: "Target vector y\n(n,)" { width: 140; height: 70 }
est: "Estimator\nfit(X, y)" { width: 140; height: 70 }
raw -> prep -> X -> est
y -> est
```

**Fig. 1.** The estimator contract: one numeric matrix `X` and one aligned vector `y` — everything else must have been converted before this boundary.

> [!warning] Interview trap
> "The design matrix is just the dataframe." It is not: the dataframe can hold strings, dates, and NaNs, while the design matrix is the post-encoding numeric artifact with a fixed shape. Statements like "logistic regression requires the design matrix to be full rank" or "standardize columns of X" are about this object, not about your raw table — and every [[What is a model parameter]] count follows from `p` in `X`.

> [!tip] Interview answer
> The design matrix is the numeric n-by-p table the estimator consumes: rows are observations, columns are features, aligned with the target vector y. I would mention the intercept column convention, that encoding and scaling live between the raw table and X, and that rank, collinearity, and shape of X explain a surprising number of modeling bugs.

