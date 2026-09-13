<!--
reps: 0
priority: 0
-->
#MachineLearning/Supervised #SRS

# What is a regression problem in machine learning

> [!abstract] Short answer
> A regression problem is supervised learning where the **target is a continuous number** — price, demand, duration, probability-like scores. The model outputs a real value and is judged by how close it lands, using distance-based losses and metrics rather than exact-match correctness.

Regression contrasts with classification, where the output is a discrete class. The boundary is about the target's nature, not the model: a "probability of churn" between 0 and 1 is still typically trained as a classification problem (the label is a class, the score is a byproduct), while "days until churn" is regression. Choosing wrong wastes modeling effort and produces dishonest metrics.

## Losses and metrics for regression

The standard training loss is squared error; its robustness issues (squared error punishes outliers quadratically) motivate absolute error and Huber loss. Evaluation uses MAE, RMSE, and R² — the specifics are in [[What regression metrics do you use in machine learning]], the generic loss discussion in [[What is a loss function]]. MSE itself gets a dedicated card: [[What is mean squared error]].

```python
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, r2_score

reg = Ridge(alpha=1.0).fit(X_tr, y_tr)      # y_tr: continuous, e.g. price
pred = reg.predict(X_te)
print(mean_absolute_error(y_te, pred), r2_score(y_te, pred))
```

**Listing 1.** A regression fit and honest scoring: predictions are numbers, and closeness is measured with distance-based metrics.

## What regression is not

Not "any model that outputs a number" — a softmax classifier outputs numbers too; the difference is that its target is a class index. Not necessarily linear: gradient-boosted trees and neural networks solve regression routinely (with squared-error objectives). And not automatically interpretable — coefficients only mean what they mean in linear models, which is compared in [[What is the difference between linear regression and logistic regression]].

> [!warning] Interview trap
> "Regression means linear regression." The term defines the target type, not the model class; saying "I'll use regression" answers nothing about the estimator. Second trap: heavy-tailed targets (income, order value) make squared-error training chase outliers — log-transform the target or switch to Huber/absolute loss, then evaluate on the business-relevant scale.

> [!tip] Interview answer
> A regression problem is a supervised task with a continuous target, trained with distance-based losses like squared error and evaluated with MAE, RMSE, and R². I would distinguish it from classification by the target's nature, name outlier sensitivity of squared error as the classic practical issue, and note that the model class is a separate choice — trees and neural nets do regression too.

