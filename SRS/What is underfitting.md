<!--
reps: 0
priority: 0
-->
#MachineLearning/Regularization #SRS

# What is underfitting

> [!abstract] Short answer
> Underfitting is when the model is **too constrained to capture the pattern**: training error itself is high, and validation error tracks it closely. Unlike overfitting, the gap is small — the model is consistently wrong, not memorizing. The cures are capacity, better features, longer training, or weaker regularization.

The diagnosis is the mirror image of overfitting: train and validation curves move together but both plateau too high. The model has high bias: its hypothesis class or its training budget cannot represent the relationship — the left side of the U-curve: [[What is the bias-variance tradeoff]].

## Common causes in real projects

* **Model too simple for the structure** — linear model on strongly nonlinear data: [[What is the difference between linear regression and logistic regression]] shows the family trap; trees too shallow to find interactions: [[How does a decision tree work]].
* **Over-regularized:** λ too large, dropout on an already-small model, aggressive early stopping — regularization heals overfitting and causes underfitting when overdosed: [[What is a regularization term]], [[What is dropout]], [[What is early stopping]].
* **Starved training:** too few epochs, learning rate too small (or misconfigured optimizer: [[What is the difference between Adam and SGD]]), batch effects that stall convergence.
* **Feature poverty:** the signal is not expressible from the given inputs — no model capacity fixes missing information: [[What is feature engineering]].
* **Bad scaling or bugs:** unscaled inputs choking gradient methods, broken preprocessing — before blaming the model, verify the plumbing: [[What is a design matrix]].

```text
overfit: train 0.02  val 0.31   gap 0.29  -> regularize, more data
underfit: train 0.38  val 0.40  gap 0.02  -> capacity, features, epochs
```

**Listing 1.** The two-line differential diagnosis: similar magnitudes, opposite prescriptions — the gap separates the diseases.

## The subtle case

Underfitting hides behind imbalance and wrong metrics: a model predicting the majority class has low apparent "error" and zero skill — check the confusion matrix before calling a model well-fit: [[What is a confusion matrix]], [[How do you handle class imbalance]]. Also mind the ceiling: some datasets are simply noisy — when train error approaches the irreducible noise floor σ², further capacity buys nothing; that is convergence, not underfitting: [[What is mean squared error]] for how noise floors metrics.

> [!warning] Interview trap
> "High validation error means overfitting." Not necessarily — compare with training error first: high train error too means underfitting, and the fix is the opposite of regularization. Second trap: "just train longer" — with a too-small hypothesis class or missing features, epochs only polish a wrong shape; add capacity or signal, not time.

> [!tip] Interview answer
> Underfitting is high training error with a small train–validation gap — the model cannot represent the pattern, so it is uniformly wrong. I diagnose by comparing the two curves, then raise capacity, add or improve features, extend training, or dial back regularization — after checking that the metric, scaling, and class balance are not lying to me.

