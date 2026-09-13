<!--
reps: 0
priority: 0
-->
#MachineLearning/Ensembles #SRS

# What is the difference between bagging and boosting

> [!abstract] Short answer
> Bagging trains **many independent base models in parallel on random resamples** and averages them — it attacks variance. Boosting trains **weak learners sequentially, each focusing on the errors of the previous ones** and adds them up — it attacks bias. Random forest is bagging; gradient boosting and AdaBoost are boosting.

## Mechanics side by side

**Bagging** (bootstrap aggregating) draws bootstrap samples (rows with replacement), fits one model per sample, and averages predictions (regression) or votes (classification). Because the base models are decorrelated, their errors cancel: variance drops roughly with the correlation between members. Random forest sharpens this by sampling a random feature subset at every split — decorrelation is deliberate: [[What is a random forest]].

**Boosting** fits models one after another; each new model targets what the ensemble still gets wrong. AdaBoost reweights misclassified rows; gradient boosting — the modern form — fits each new tree to the **negative gradient of the loss**: [[What is gradient boosting]]. Members are weak (shallow trees) and the ensemble is a weighted sum.

```text
bagging : T1, T2, ..., TM independent (bootstraps) -> average / vote
boosting: T1 -> fix errors -> T2 -> fix errors -> ... -> weighted sum
```

**Listing 1.** Parallel decorrelated averaging versus sequential error correction — the architectural difference in one line.

```d2
direction: right
bag: "Bagging\nparallel, independent\nlow bias, high variance members" {
  width: 250; height: 100
}
boost: "Boosting\nsequential, dependent\neach fixes predecessors" {
  width: 250; height: 100
}
var: "variance ↓\nbias ~same" { width: 150; height: 70 }
bias: "bias ↓\nvariance managed\nby shrinkage" { width: 170; height: 80 }
bag -> var; boost -> bias
```

**Fig. 1.** Bagging reduces variance of strong base learners; boosting reduces bias of weak ones — overfitting discipline differs accordingly.

## Practical consequences

Bagging tolerates noisy labels better (a poisoned bootstrap corrupts one member of many); boosting fits residuals and will chase outliers and label noise hard — regularization and early stopping are mandatory: [[What is early stopping]]. Bagging members are trained independently — embarrassingly parallel; boosting is inherently sequential. Boosting usually wins accuracy on clean tabular data; bagging is the safer default when data is noisy and tuning budget is small — see [[What is the bias-variance tradeoff]] for the underlying frame.

> [!warning] Interview trap
> "Boosting always outperforms bagging." On noisy data or with careless learning rates, boosting overfits while a random forest just works. Also do not say bagging "reduces bias" — averaging decorrelated estimators attacks variance; the base models must already have low bias (deep trees), which is why forests grow them deep while boosting uses stumps.

> [!tip] Interview answer
> Bagging fits many strong models independently on bootstrap resamples and averages them to cut variance — random forest, plus random feature subsets for decorrelation. Boosting fits weak models sequentially, each correcting the ensemble's remaining error via the loss gradient, cutting bias with shrinkage — gradient boosting. I would add: bagging is parallel and noise-robust, boosting is sequential, usually more accurate, and needs learning-rate and early-stopping discipline.

