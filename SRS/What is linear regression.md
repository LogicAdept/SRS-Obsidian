<!--
reps: 0
priority: 0
-->
#MachineLearning/Supervised #SRS

# What is linear regression

> [!abstract] Short answer
> Linear regression predicts a continuous target as a **weighted sum of features plus a bias**: `ŷ = w·x + b`. Training picks the weights that minimize squared error — either in closed form (normal equations / least squares) or by gradient descent. It is the baseline regression model you should beat before anything fancier earns its complexity.

"Linear" refers to the parameters: the model is linear in `w`, even if features themselves are transformed (polynomials, splines). The fitted coefficients are interpretable — each `wⱼ` says how much the prediction moves per unit of feature `j`, holding others fixed — which is why linear models remain the default in regulated and scientific settings.

## How fitting works

Minimizing mean squared error `Σ(yᵢ − w·xᵢ − b)²` has a convex landscape: one global optimum. With `n ≥ p` and non-collinear columns, the closed-form least-squares solution exists; otherwise the problem is ill-posed and regularization fixes it — [[What is the difference between L1 and L2 regularization]]. Assumptions worth remembering: errors roughly centered and homoscedastic for the statistical guarantees; features not perfectly collinear for identifiability — the design matrix view is in [[What is a design matrix]].

```python
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline

reg = make_pipeline(StandardScaler(), LinearRegression())
reg.fit(X_tr, y_tr)
# ill-conditioned data (collinear features) -> prefer the penalized twin:
ridge = make_pipeline(StandardScaler(), Ridge(alpha=1.0)).fit(X_tr, y_tr)
```

**Listing 1.** Ordinary least squares and its ridge sibling; scaling the features keeps coefficients comparable and the solve numerically stable.

## Where it fails and what to do

Non-linear relationships need feature transforms or a different model class. Outliers drag the squared-error fit hard — see the loss alternatives in [[What is a loss function]]. Correlated features make individual coefficients unstable while predictions stay fine. And extrapolation beyond the training feature range is silent guesswork. For the classification counterpart and where the two diverge, see [[What is the difference between linear regression and logistic regression]].

> [!warning] Interview trap
> "Linear regression cannot fit curves." Wrong — fit a polynomial or spline basis and the model is still linear regression in its parameters. The real limitations are sensitivity to outliers, collinearity blowing up coefficient variance, and extrapolation. Also, R² alone does not prove the fit is good: a strong trend with terrible residuals can still post a high R².

> [!tip] Interview answer
> Linear regression models the target as a weighted sum of features, fitted by minimizing squared error with a convex, closed-form or gradient solution. I would stress interpretability of coefficients, that collinearity and outliers are its practical weak spots, that feature engineering keeps it linear-in-parameters but not linear-in-reality, and that it is the baseline every regression model must justify itself against.

