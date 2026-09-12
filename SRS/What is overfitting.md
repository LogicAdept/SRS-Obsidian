<!--
reps: 0
priority: 0
-->
#MachineLearning/Regularization #SRS

# What is overfitting

> [!abstract] Short answer
> Overfitting is when a model **fits the training sample's noise instead of the underlying pattern**: training error keeps falling while error on unseen data rises. The model memorized the sample; the skill does not transfer. Detection is the train–validation gap, and the cures are data, regularization, and capacity control.

The mechanism: finite samples contain both signal and noise; a flexible model has enough capacity to reduce training error by encoding noise — coefficients, splits, or weights that match quirks of the particular rows. The more parameters relative to independent observations, the wider the memorization channel — parameter-count framing in [[What is a model parameter]], capacity framing in [[What is the bias-variance tradeoff]].

## How to see it and what to do

```text
epoch 1 : train 0.42  val 0.41   <- both improving: healthy
epoch 20: train 0.05  val 0.31   <- gap opens: overfitting
epoch 40: train 0.01  val 0.38   <- val worsens: pure memorization
```

**Listing 1.** The learning-curve signature: divergence of train and validation loss; validation bottoming out before training loss — the classic elbow that early stopping watches: [[What is early stopping]].

The remedies, in order of honesty: **more data** (the only true cure — variance shrinks with sample size), **data augmentation** when the domain allows it, **regularization** — L1/L2: [[What is the difference between L1 and L2 regularization]], dropout: [[What is dropout]], **capacity limits** — depth, width, tree depth, **early stopping**, and **ensembling** — [[What is a random forest]]. First, though, rule out the impostor: a train–validation gap can be **distribution mismatch or leakage cleanup**, not model pathology — fixing "overfitting" with regularization when the real bug is a leak is a classic misdiagnosis: [[What is data leakage in machine learning]].

## Overfitting beyond the model

The concept generalizes to decisions: hyperparameter sets tuned by replayed validation searches overfit the validation set ([[What is hyperparameter tuning]]), features selected by test-set peeking overfit the test set, and prompt iteration on a fixed eval set overfits it in the LLM era: [[How do you evaluate an LLM]]. Any adaptive loop that reads a finite dataset repeatedly consumes its honesty.

> [!warning] Interview trap
> "Overfitting means high training accuracy." Overfitting is defined by the **gap**, not the level — training accuracy is supposed to be high; the disease is validation falling behind. Reverse trap: "deep learning does not overfit because of double descent" — large nets still memorize noisy labels; the phenomenology is subtler, the responsibility is not gone.

> [!tip] Interview answer
> Overfitting is the train–validation divergence: the model encodes sample-specific noise, so training loss falls while held-out loss rises. I detect it with learning curves, rule out leakage and distribution shift before blaming capacity, then fight it with more or augmented data, regularization, capacity limits, early stopping, and ensembling — in that spirit, not by turning every knob at once.

