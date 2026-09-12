<!--
reps: 0
priority: 0
-->
#MachineLearning/Optimization #SRS

# What is a model hyperparameter

> [!abstract] Short answer
> A hyperparameter is a **configuration value you choose before training** — learning rate, tree depth, number of neighbors, regularization strength, number of clusters. It controls the training process and model complexity, but is not fitted by it. Hyperparameter choice is a search problem, and honest search needs its own data split.

The boundary rule: if the optimizer learns it from the training data, it is a parameter ([[What is a model parameter]]); if you must set it, it is a hyperparameter. Some values blur the line in practice (k in k-means could be a business constraint), but the training-time test above settles it.

## Typical knobs

* **Capacity:** tree `max_depth` / `min_samples_leaf`, polynomial degree, number of layers, `k` in k-NN.
* **Optimization:** learning rate, batch size, epochs — see [[What is the difference between batch SGD and mini-batch gradient descent]] and [[What is the difference between Adam and SGD]].
* **Regularization:** `C` and penalty in linear models, dropout rate, early-stopping patience — see [[What is the difference between L1 and L2 regularization]] and [[What is early stopping]].
* **Structure:** number of clusters in k-means, number of trees and learning rate in boosting — [[How do you choose k in k-means]], [[What is a random forest]].

```python
from sklearn.model_selection import GridSearchCV, StratifiedKFold
from sklearn.ensemble import RandomForestClassifier

grid = {"n_estimators": [100, 300], "max_depth": [None, 10, 20],
        "min_samples_leaf": [1, 5]}
search = GridSearchCV(RandomForestClassifier(random_state=0), grid,
                      cv=StratifiedKFold(5), scoring="roc_auc", n_jobs=-1)
search.fit(X_tr, y_tr)   # best hyperparameters picked by CV, not test
print(search.best_params_)
```

**Listing 1.** Hyperparameter search via cross-validation on the training set; the test set stays untouched until the final report — the tuning procedure is [[What is hyperparameter tuning]].

## The honest-selection problem

Every hyperparameter chosen by looking at validation data consumes a little of that data's honesty. Nested cross-validation exists for when that cost must be accounted properly; leaking the test set into the search silently inflates the final score — [[What is data leakage in machine learning]]. Search cost explodes combinatorially, hence random and Bayesian search — covered in [[What is hyperparameter tuning]].

> [!warning] Interview trap
> "The best hyperparameters are the ones that maximize validation score, so search hard and report that score." Searching many configurations and reporting the best validation number is selection bias unless the final estimate comes from fresh data. Second trap: "learning rate is a parameter" — no; the optimizer nudges parameters by it; the rate itself is yours to set: [[What is gradient descent]].

> [!tip] Interview answer
> Hyperparameters are pre-training choices that shape capacity and training dynamics, while parameters are what fitting produces. I would give tree depth and learning rate as canonical examples, say selection is done by cross-validation on the training portion with the test set sealed, and mention that aggressive search on a small validation set is itself a source of optimistic bias.

