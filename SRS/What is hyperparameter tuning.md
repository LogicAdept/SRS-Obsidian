<!--
reps: 0
priority: 0
-->
#MachineLearning/Optimization #SRS

# What is hyperparameter tuning

> [!abstract] Short answer
> Hyperparameter tuning is **searching the configuration space** (learning rate, depth, regularization, batch size…) for the validation-optimal setting — via grid search (exhaustive over a small grid), random search (sampled, better in high dimensions), Bayesian optimization (model-guided sampling), or successively halving/Hyperband (kill losers early). All of it runs inside cross-validation, never touching the test set.

The search budget question dominates: a grid over 5 hyperparameters with 5 values each is 3125 fits — random search covers the space better per fit because it explores each axis independently; Bayesian methods (Optuna, scikit-optimize) model the score surface and pick promising points; halving methods allocate more epochs to promising candidates: [[What is early stopping]] logic applied to search.

## The honest-search protocol

1. **Define the search space from the literature and defaults**, log-scaled for LRs and penalties.
2. **Run the search inside CV on the training set:** every configuration scored by the same folds: [[What is cross-validation]].
3. **Select and refit** the winner on the full training set.
4. **Report the sealed test-set score once.** Repeated test peeks convert test into validation — the leak of selection: [[What is data leakage in machine learning]]; nested CV measures the optimism when needed: [[What is a train validation test split]].

```python
import optuna
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import GradientBoostingClassifier

def objective(trial):
    params = {"learning_rate": trial.suggest_float("lr", 0.01, 0.3, log=True),
              "max_depth": trial.suggest_int("depth", 2, 8),
              "subsample": trial.suggest_float("subsample", 0.6, 1.0)}
    clf = GradientBoostingClassifier(**params, n_estimators=300)
    return cross_val_score(clf, X_tr, y_tr, cv=5, scoring="roc_auc").mean()

study = optuna.create_study(direction="maximize")
study.optimize(objective, n_trials=60)
```

**Listing 1.** Bayesian (Optuna) search over a log-scaled space, scored by cross-validation — the objective returns validation quality only; the test set stays outside the function.

## Priorities and discipline

Not all knobs deserve equal budget: learning rate and regularization dominate most surfaces; batch size couples to LR: [[What is the difference between batch SGD and mini-batch gradient descent]]; architectural knobs cost the most to search. Overfitting applies to the search itself: trying 500 configurations on a small validation set and reporting the best is optimism by selection — report how many were tried and at what spread: [[What is overfitting]]. And automation without reproducibility is waste: log every trial (params, folds, seed, score) — the experiment-tracking discipline of [[What is MLOps]] and the lifecycle's versioned loops: [[What is the machine learning lifecycle]].

> [!warning] Interview trap
> "Grid search is the standard." Grids waste fits on redundant axis combinations once dimensions exceed ~3 — random and Bayesian search dominate in practice; grids survive only for tiny, well-understood spaces. Second trap: "tune on the test set for realism" — that is not realism, that is leakage; the test set's value is precisely that the search never saw it.

> [!tip] Interview answer
> I tune inside cross-validation on the training set: random or Bayesian search over a log-scaled space, prioritizing learning rate and regularization, with trials logged for reproducibility. Select the winner, refit on full training data, and score the sealed test set once. I would stress search overfitting — the more configurations tried on a small validation set, the more optimistic the reported number — and nested CV when that bias must be quantified.

