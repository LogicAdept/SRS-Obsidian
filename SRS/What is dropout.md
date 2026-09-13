<!--
reps: 0
priority: 0
-->
#MachineLearning/Regularization #SRS

# What is dropout

> [!abstract] Short answer
> Dropout randomly **zeroes each activation with probability p during training** and scales the rest, forcing the network to not co-adapt: no single unit can be relied upon, so representations become redundant and robust — an ensemble of exponentially many thinned subnetworks sharing weights. At inference dropout is off; activations use the full network.

Training each step samples a different subnetwork; the shared weights must work under all of them — the ensemble view from the original paper (Srivastava et al., 2014). The scaling trick (inverted dropout) divides surviving activations by 1/(1−p) during training so inference needs no change — PyTorch's `nn.Dropout(p)` implements inverted dropout.

## Mechanics and usage

```python
import torch.nn as nn

net = nn.Sequential(
    nn.Linear(512, 256), nn.ReLU(),
    nn.Dropout(p=0.5),          # train: zero half, scale survivors
    nn.Linear(256, 10),
)
net.train()   # dropout active
net.eval()    # dropout disabled — the mode-switch bug classic
```

**Listing 1.** Typical p: 0.5 in fully connected layers, 0.1–0.3 in transformer attention and FFN blocks. `train()`/`eval()` toggles it — forgetting the switch corrupts validation metrics: [[What is batch normalization]] has the same trap.

## Where it helps and where it hurts

Helps: large fully connected layers on limited data, transformer fine-tuning (the standard 0.1), and as a cheap ensemble effect. Hurts or does nothing: convolutional front layers (spatial dropout variants exist for channels), small models that underfit already, and BN-heavy architectures where its role shrinks — the original BN paper argued batchnorm reduces the need for dropout: [[What is batch normalization]]. Related family: drop-path/label smoothing/stochastic depth — all inject noise to prevent co-adaptation; the regularization-term view connects them: [[What is a regularization term]].

> [!warning] Interview trap
> "Dropout makes the model more accurate." It regularizes — it trades a bit of fitting capacity for generalization; on an underfitting model it makes things worse. Second trap: "dropout is active at inference" — inverted dropout scales during training precisely so inference runs the plain network; if you see variance across identical inference calls, a train-mode layer is leaking somewhere.

> [!tip] Interview answer
> Dropout zeroes random activations during training with inverted scaling, so no unit can be secretly load-bearing — effectively averaging an ensemble of thinned subnetworks — and it is disabled at inference. I use 0.5 on dense heads, ~0.1 inside transformers, skip it when the model underfits, and always double-check train/eval mode because a leaking dropout silently corrupts validation numbers.

