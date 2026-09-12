<!--
reps: 0
priority: 0
-->
#MachineLearning/Optimization #SRS

# What is the difference between batch SGD and mini-batch gradient descent

> [!abstract] Short answer
> The difference is the **gradient's sample size per step**: batch (full-batch) descent uses the entire dataset — exact gradient, one step per epoch. "Pure" SGD uses one sample — maximally noisy. Mini-batch uses a chunk (32–10k rows) — a noisy but GPU-parallel gradient estimate; it is what every modern framework means by "SGD" in practice.

Noise is the axis: the full-batch gradient is deterministic and slow per unit of progress; single-sample gradients are wild but cheap and numerous; mini-batches average the noise down while keeping the stochastic benefits — cheap steps, escape from saddle regions, and an implicit regularization effect: [[What is gradient descent]].

## Why mini-batch won

* **Hardware:** GPUs are throughput machines — a 256-row batch uses them fully; one row at a time idles them.
* **Time to convergence:** per-epoch progress with mini-batches is dramatically higher; wall-clock to a good model shrinks by orders of magnitude.
* **Noise as a feature:** gradient noise helps escape sharp, poorly-generalizing minima and plateaus; too large a batch reduces noise and often needs LR scaling and warmup to recover quality — the large-batch generalization gap.
* **Memory:** the full dataset rarely fits; batches make training memory tractable — activation storage per batch is the memory driver: [[What is backpropagation]].

```text
full-batch : 1 step / epoch, exact grad, GPU-idle-small, deterministic
single SGD : n steps / epoch, pure noise, no vectorization
mini-batch : n/B steps / epoch, averaged noise, GPU-full  <- the standard
```

**Listing 1.** The three regimes; "SGD" in library names (`torch.optim.SGD`) is the update rule, not a promise of batch size one.

## Choosing the batch size

Batch size is a hyperparameter coupled to the learning rate: doubling the batch roughly licenses doubling the LR (linear scaling rule, with warmup for big batches). Small batches (32–128) favor generalization and fit small GPUs; large batches favor throughput and stability for LLM pretraining — with warmup compensating the lost noise: [[What is the difference between Adam and SGD]]. Batch-norm statistics also depend on the batch — tiny batches degrade them: [[What is batch normalization]]. The trade sits inside the broader tuning loop: [[What is hyperparameter tuning]].

> [!warning] Interview trap
> "SGD means batch size 1." Historically yes; in modern usage SGD names the plain momentum update rule and runs on any batch size — assuming one-sample updates will lose you the interview's practical credibility. Second trap: "larger batch only changes speed" — it changes gradient noise, effective learning dynamics, and often final generalization; it is a quality knob, not just a throughput knob.

> [!tip] Interview answer
> The variants differ in how many samples define each step's gradient: the full batch is exact but slow, single-sample SGD is pure noise, and mini-batches average noise down while using GPUs fully — which is why mini-batch is the default everywhere. Batch size couples to learning rate and gradient noise: small batches regularize, large ones need LR scaling and warmup, and batchnorm makes tiny batches statistically shaky.

