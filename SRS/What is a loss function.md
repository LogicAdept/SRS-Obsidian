<!--
reps: 0
priority: 0
-->
#MachineLearning/Optimization #SRS

# What is a loss function

> [!abstract] Short answer
> A loss function maps a prediction and the truth to a **single non-negative number saying how bad the prediction is**. Training is minimizing the average loss over the data; the whole optimization machinery — gradient descent and its variants — exists to reduce this number, so the loss literally defines what "learning" means for a given problem.

Pick the wrong loss and you get a well-trained model of the wrong thing: the optimizer is obedient, not wise. This is why loss choice is a modeling decision that comes before algorithm choice, and why proxy losses (cross-entropy instead of accuracy) are normal — differentiability and smoothness matter during training.

## The standard losses

* **Squared error** `(ŷ − y)²` — regression default; smooth, differentiable, outlier-sensitive.
* **Absolute error / Huber** — regression when outliers should not dominate; Huber is quadratic near zero, linear in the tails.
* **Cross-entropy / log loss** — classification default; punishes confident wrong answers asymptotically hard: [[What is cross-entropy loss]].
* **Hinge loss** — max-margin classification, the SVM objective: [[What is an SVM]].
* **Regularized objectives** — loss plus a penalty term controlling complexity: [[What is a regularization term]].

```text
L_sq(y, yhat)   = (y - yhat)^2                       # regression
L_log(y, yhat)  = -(y*log(yhat) + (1-y)*log(1-yhat)) # binary classification
L_hinge(y, t)   = max(0, 1 - y*t)                    # SVM, labels +-1
objective(theta) = mean_i L(f(x_i; theta), y_i) + lambda * penalty(theta)
```

**Listing 1.** Canonical losses; the training objective is usually the average loss plus a regularization penalty weighted by lambda.

## Loss vs metric

A metric is for humans reading reports; a loss is for the optimizer to differentiate. They often disagree on purpose: you serve accuracy but train with cross-entropy, because accuracy is piecewise-constant and gives no gradient. Knowing which losses are differentiable where, and which metric your loss secretly optimizes, is core interview territory — see [[What is gradient descent]] for why the gradient must exist.

> [!warning] Interview trap
> "Lower training loss means a better model." Training loss can always be pushed down by memorizing; the question is validation loss — and even that is honest only if the split discipline is. See [[What is overfitting]]. Second trap: class imbalance makes plain average loss quietly optimize the majority class; weighting or resampling changes what the loss means — [[How do you handle class imbalance]].

> [!tip] Interview answer
> A loss function scores one prediction against the truth, and training is minimization of its average plus a penalty. I would name squared error, absolute/Huber, cross-entropy, and hinge as the canonical set, stress that loss choice encodes what mistakes should cost, and note that losses must be differentiable while metrics need not be — which is why we often train on one and report the other.

