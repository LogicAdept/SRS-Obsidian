<!--
reps: 0
priority: 0
-->
#MachineLearning #SRS

# What is a model parameter

> [!abstract] Short answer
> Model parameters are the **numbers inside the model that training adjusts** — regression coefficients, tree split thresholds, neural network weights and biases. They are not chosen by you; they are the output of fitting. At inference, the parameters are all that matters: the frozen values plus the input define the prediction.

Parameters are contrasted with hyperparameters, which you set before training: [[What is a model hyperparameter]]. The count of parameters is the model's "size" — thousands for a linear model, hundreds of billions for frontier LLMs — and it drives memory, inference latency, and overfitting capacity.

## Where parameters live

* Linear / logistic regression: one coefficient (and bias) per feature after encoding — parameter count scales with dimensionality of the design matrix: [[What is a design matrix]].
* Decision trees: split feature, threshold, and leaf values at every node — fitted by greedy impurity reduction, not by gradient descent: [[How does a decision tree work]].
* Neural networks: weight matrices and bias vectors per layer; fitted by backpropagation: [[What is backpropagation]].
* Embedding tables: one row per vocabulary or category item: [[What is an embedding]].

```python
from sklearn.linear_model import LinearRegression
import numpy as np

reg = LinearRegression().fit(X_tr, y_tr)
print(reg.coef_, reg.intercept_)       # <- the fitted parameters theta-hat
print("params:", X_tr.shape[1] + 1)    # p coefficients + bias
```

**Listing 1.** After fit, `coef_` and `intercept_` hold the learned parameters; the same API convention (trailing underscore = fitted attribute) runs through scikit-learn.

## Why the concept matters operationally

Parameter count is a capacity dial: more parameters mean more ability to fit noise, which is why regularization, which shrinks or constrains parameters, exists — [[What is the bias-variance tradeoff]]. In production, parameter count determines serving footprint; LoRA-style methods avoid retraining all of them: [[What is LoRA]]. Versioning fitted parameters correctly is deployment hygiene — see [[What is a model in machine learning]].

> [!warning] Interview trap
> "Parameters are the settings I configure." That is hyperparameters — the classic junior mix-up, tested in every interview. In sklearn's `LogisticRegression(C=1.0)`, `C` is a hyperparameter; the learned `coef_` afterwards are parameters. Related trap: "more parameters always mean a better model" — they mean more capacity, not more correctness: [[What is overfitting]].

> [!tip] Interview answer
> Parameters are the values fitted from data — coefficients, thresholds, weights — and they are what inference actually uses. I would contrast them with hyperparameters set before training, connect parameter count to model capacity and the bias-variance story, and mention that in neural nets parameters are the weight matrices updated by backpropagation.

