<!--
reps: 0
priority: 0
-->
#MachineLearning/Optimization #SRS

# What is the difference between Adam and SGD

> [!abstract] Short answer
> SGD steps every parameter by the same learning rate scaled only by the gradient (plus momentum). **Adam adds per-parameter adaptivity**: it keeps running first and second moments of gradients and divides the step by √v̂, so parameters with noisy or sparse gradients get larger effective steps and vice versa — `lr ≈ 1e-3` by default versus SGD's tuned 0.1-and-down.

The mechanics: Adam maintains `m̂` (smoothed gradient — momentum-like) and `v̂` (smoothed squared gradient — scale estimate), updating with `m̂/(√v̂ + ε)`, with bias-corrected defaults β₁ = 0.9, β₂ = 0.999, ε = 1e-8 (the values from the original paper, Kingma & Ba 2014). Effect: a rough per-coordinate automatic learning rate. SGD with momentum, by contrast, moves in a smoothed gradient direction with one global step size.

## The practical trade-offs

* **Adam:** fast early progress, tolerant of hyperparameter neglect, the default for transformers and LLM fine-tuning (AdamW variant — decoupled weight decay, the honest L2: [[What is the difference between L1 and L2 regularization]]); costs two extra state buffers per parameter — the memory bill that LoRA-style methods shrink: [[What is LoRA]].
* **SGD + momentum:** often **better final generalization** in vision (the classic result: tuned SGD beats Adam on ImageNet classification), cheaper memory, more sensitive to LR schedule — which is also its strength: schedules compose cleanly.
* **Convergence quality:** Adam's adaptive scaling can settle into sharper basins; SGD's noise acts as implicit regularization: [[What is the bias-variance tradeoff]].

```python
import torch

adam = torch.optim.AdamW(model.parameters(), lr=1e-3,
                         betas=(0.9, 0.999), weight_decay=0.01)
sgd = torch.optim.SGD(model.parameters(), lr=0.1, momentum=0.9,
                      weight_decay=5e-4)
```

**Listing 1.** The two calls: Adam(W) with its moment betas, SGD with momentum — same training loop outside, different step shaping inside.

## How to choose

Transformers, LLMs, sparse embeddings, quick prototyping: Adam/AdamW — near-mandatory in the LLM stack: [[What is an LLM and what is a context window]]. CNNs from scratch, long training runs with a crafted cosine/step schedule, memory-limited settings: SGD + momentum still competitive. If in doubt: Adam for iteration speed, then test whether tuned SGD buys final quality — and warmup plus decay apply to both, via [[What is gradient descent]]'s η story.

> [!warning] Interview trap
> "Adam is always better because it is adaptive." Adaptivity trades away the noise benefits of SGD and often generalizes worse on large vision tasks when both are tuned — the choice is empirical, not ideological. Second trap: calling AdamW "Adam with L2" — the W is precisely the **decoupled** weight decay; grafting L2 into Adam's gradient path behaves differently and worse.

> [!tip] Interview answer
> SGD applies one global learning rate in the smoothed gradient direction; Adam keeps per-parameter first and second gradient moments and divides the step by the root of the second — automatic per-coordinate step sizes, betas 0.9 and 0.999 by default. I reach for AdamW on transformers and fast iteration, SGD plus momentum and a schedule when final generalization and memory matter, and I tune learning rate either way.

