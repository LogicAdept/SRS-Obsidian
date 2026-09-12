<!--
reps: 0
priority: 0
-->
#MachineLearning/Supervised #SRS

# What is the difference between linear regression and logistic regression

> [!abstract] Short answer
> Linear regression predicts a **continuous value** as `w·x + b` and is trained on squared error. Logistic regression predicts a **class probability** by squashing `w·x + b` through the sigmoid and is trained on cross-entropy. Despite the name, logistic regression is a **classification** algorithm; the two share the linear-scoring skeleton but differ in output, loss, and assumptions.

The name trap is the point of the question: "regression" in logistic regression refers to regressing on the **log-odds**, not to predicting a continuous target. Both models are linear in the parameters — the logit is a linear model of log-odds, coefficients stay interpretable as log-odds shifts.

## Mechanically

```text
linear    : yhat = w·x + b                      loss: (y - yhat)^2
logistic  : p    = sigmoid(w·x + b)             loss: -[y log p + (1-y) log(1-p)]
            class = 1 if p >= threshold
```

**Listing 1.** The same linear score, two different heads and losses: identity plus squared error, sigmoid plus cross-entropy.

```python
from sklearn.linear_model import LinearRegression, LogisticRegression

LinearRegression().fit(X, price)        # target: continuous number
LogisticRegression(C=1.0).fit(X, churn) # target: 0/1 -> outputs probability
```

**Listing 2.** In scikit-learn the target type and the estimator class must match; `predict_proba` gives the calibrated-ish probability, `predict` the thresholded class.

## Consequences of the difference

Linear regression on a 0/1 target produces unbounded predictions — probabilities below 0 and above 1 — which is exactly why the sigmoid head exists. Conversely, using classification on a true amount throws away magnitude information. Threshold choice (default 0.5) is a business decision and should be tuned for the metric that matters: [[What is the difference between precision and recall]], [[What is ROC AUC]]. Both models need the same care around collinearity, scaling, and regularization: [[What is the difference between L1 and L2 regularization]].

> [!warning] Interview trap
> "Logistic regression is for regression because of the name." It is a binary classifier; multiclass is handled by one-vs-rest or multinomial (softmax) formulations. Second trap: "logistic regression outputs calibrated probabilities out of the box" — the sigmoid output is only as calibrated as the data allows; under imbalance or distribution shift it needs recalibration, not blind trust.

> [!tip] Interview answer
> Both are linear-in-parameters models; linear regression fits continuous targets with squared error, logistic regression squashes the linear score into a probability with the sigmoid and fits it with cross-entropy for classification. I would name the naming trap, explain that regressing 0/1 with a linear model yields out-of-range predictions, and mention that threshold tuning and probability calibration are where logistic regression's real-world quality is decided.

