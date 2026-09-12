<!--
reps: 0
priority: 0
-->
#MachineLearning/Regularization #SRS

# What is early stopping

> [!abstract] Short answer
> Early stopping halts training **when validation performance stops improving**: keep evaluating on a validation set during training, remember the best state, and stop after patience runs out — restoring the best weights at the end. It is regularization by limiting training time: the model is frozen near the generalization optimum, before it drifts into memorization.

Training loss falls monotonically, but validation loss bottoms out and then rises as the model starts fitting noise — the overfitting signature: [[What is overfitting]]. Early stopping rides that curve: patience (epochs to wait without improvement), min-delta (what counts as improvement), and restore-best are the knobs — the learning-curve diagnostic behind it: [[What is the bias-variance tradeoff]].

## Mechanics

```python
from sklearn.ensemble import GradientBoostingRegressor

reg = GradientBoostingRegressor(n_estimators=2000, learning_rate=0.05,
                                validation_fraction=0.15,
                                n_iter_no_change=25, random_state=0)
reg.fit(X_tr, y_tr)   # stops near the validation optimum, not at 2000

# Keras/PyTorch equivalent:
# EarlyStopping(monitor="val_loss", patience=25, restore_best_weights=True)
```

**Listing 1.** In scikit-learn, `n_iter_no_change` with `validation_fraction`; in deep frameworks, the callback with patience and best-weight restore — the semantics are identical across stacks.

## Why it doubles as an economics tool

Stopping early is free regularization — no penalty term, no architecture change — and it directly cuts compute: with a small learning rate and generous budget (the boosting recipe: [[What is gradient boosting]]), the validation curve decides the epoch count instead of a guess. It interacts with learning-rate schedules: decaying LR late in training flattens the validation curve, so patience must be set against the schedule, not against the raw epoch count — the schedule discussion in [[What is the difference between Adam and SGD]]. In LLM fine-tuning, early stopping on a held-out eval set guards against catastrophic overfit on small instruction sets: [[What is LoRA]], [[What is transfer learning]].

## Where it needs care

Noisy validation metrics (small sets, imbalance) make patience jittery — smooth with a moving average or evaluate on a larger slice: [[How do you handle class imbalance]]. With repeated restarts and re-tuning against the same validation data, the selection itself overfits: the test set remains the once-only arbiter: [[What is a train validation test split]]. And in constrained-latency serving, the best-validation checkpoint may not be the best cost/quality point — report both.

> [!warning] Interview trap
> "Early stopping prevents overfitting completely." It limits one axis — training duration; a leaky feature or a validation set contaminated by tuning will still look great while production decays — stopping cannot fix dishonest data: [[What is data leakage in machine learning]]. Second trap: stopping when training loss stalls — the signal is **validation** stalling; training loss can still be improving usefully.

> [!tip] Interview answer
> Early stopping monitors validation loss during training, keeps the best checkpoint, and halts after a patience window — restoring the best weights. It is free regularization and a compute saver: with a small learning rate and a big budget, validation decides the epochs. I would stress patience against the LR schedule, smoothing noisy validation signals, and that the sealed test set still certifies the result.

