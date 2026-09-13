<!--
reps: 0
priority: 0
-->
#MachineLearning/DeepLearning #SRS

# Why do neural networks need nonlinear activations

> [!abstract] Short answer
> Without a nonlinear activation between layers, a stack of linear layers **collapses into one linear layer**: composition of affine maps is affine, so depth would buy nothing beyond a single matrix multiply. The activation is what lets depth compose simple nonlinearities into arbitrarily complex functions.

A layer computes `z = Wx + b`, then `a = f(z)`. Stack two layers without `f`: `W2(W1x + b1) + b2 = (W2W1)x + (W2b1 + b2)` — one affine map, provably as limited as a single layer. With `f` non-linear, each layer transforms the space, and the universal-approximation theorem says even one wide hidden layer with a standard activation can approximate continuous functions on compact sets — depth just does it with exponentially fewer parameters.

## The activation roster

* **ReLU** `max(0, z)` — the default: cheap, non-saturating for positive inputs, sparse gradients. Failure mode: dead units stuck at zero output (high learning rates kill them) — addressed by LeakyReLU (small slope for negatives), GELU (smooth, standard in transformers: [[What is self-attention]]), ELU.
* **Sigmoid** `1/(1+e^-z)` — squashes to (0,1); saturates at both tails, killing gradients — mostly demoted to output gates and binary heads: [[What is the difference between linear regression and logistic regression]].
* **Tanh** — zero-centered, still saturating; common in RNN inner gates: [[What is an LSTM]].
* **Softmax** — converts a score vector to a probability distribution at the output: [[What is softmax]].

```python
import torch, torch.nn as nn

mlp = nn.Sequential(
    nn.Linear(256, 128), nn.ReLU(),      # nonlinearity between layers
    nn.Linear(128, 64),  nn.GELU(),
    nn.Linear(64, 10),                   # logits; softmax applied by loss
)
```

**Listing 1.** Activations live between linear layers; the output layer stays raw (logits) because `CrossEntropyLoss` fuses softmax internally — a small but classic interview point.

## Why "just make it nonlinear" is the whole game

The activation's gradient properties decide trainability: saturating functions multiply many near-zero derivatives through the chain rule and stall deep networks — the vanishing-gradient problem: [[What are vanishing and exploding gradients]]. ReLU's piecewise linearity keeps gradients alive, which is a major reason deep nets became practical. Initialization and normalization interact with the same dynamics: [[How does weight initialization affect training]], [[What is batch normalization]].

> [!warning] Interview trap
> "Nonlinearity lets networks do more computation." More precisely: it lets depth represent **composition** — without it, ten layers are provably one layer. Second trap: "ReLU is always the best choice" — dead-unit pathology and negative-side information loss are real; LeakyReLU/GELU exist because of them. And softmax is not a hidden-layer activation — it is a distribution head.

> [!tip] Interview answer
> Activation functions break the affine-composition collapse: without them any depth reduces to one linear map, so nonlinearity is what makes depth meaningful. ReLU-family choices dominate because they avoid saturation and keep gradients flowing; sigmoid and tanh survive in gates and outputs. I would connect activation choice to gradient health and mention that final layers output logits with softmax handled inside modern losses.

