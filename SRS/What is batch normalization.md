<!--
reps: 0
priority: 0
-->
#MachineLearning/DeepLearning #SRS

# What is batch normalization

> [!abstract] Short answer
> Batch normalization **standardizes each activation channel across the current mini-batch** (subtract batch mean, divide by batch standard deviation), then rescales with two learnable parameters: `y = γ·(x − μ_B)/σ_B + β`. It stabilizes and accelerates training, permits higher learning rates, and adds mild regularization; at inference the running statistics replace the batch statistics.

The mechanism keeps each layer's input distribution from drifting as earlier layers update — the "internal covariate shift" framing from the original paper, later debated; the pragmatic consensus: BN smooths and re-centers the optimization landscape, making gradients better behaved — related dynamics in [[What are vanishing and exploding gradients]].

## Train vs inference — the part that breaks deployments

During training, statistics come from the current batch, and the layer maintains **running averages** of mean and variance. At inference, the batch may be a single sample, so the layer uses the frozen running statistics. Forgetting this (e.g. batch statistics at inference, or an untrained running buffer) produces models that work in training scripts and break in serving — a classic deployment bug, cousin of preprocessing skew: [[What is MLOps]].

```python
import torch.nn as nn

net = nn.Sequential(
    nn.Conv2d(3, 32, 3, padding=1),
    nn.BatchNorm2d(32),      # per-channel normalize + learnable gamma, beta
    nn.ReLU(),
)
net.eval()                    # switch: use frozen running stats, no batch stats
```

**Listing 1.** `model.train()` vs `model.eval()` decides which statistics BatchNorm uses — the single most common silent bug in PyTorch validation code.

## Limits and the alternatives

Batch statistics make BN batch-size sensitive: tiny batches (large models, per-sample medical data) give noisy estimates — LayerNorm (per-sample, per-layer statistics) replaces it in transformers: [[What is self-attention]]; GroupNorm splits the difference for small-batch vision. BN also interacts with dropout — stacking both aggressively can hurt: [[What is dropout]]; the original paper even argues BN can make dropout unnecessary. And BN adds train/serve state — the running buffers must be saved with the weights, part of the artifact discipline in [[What is a model in machine learning]].

> [!warning] Interview trap
> "BatchNorm is just preprocessing." It is a **learned** layer with train/inference duality and its own state — treat it as part of the model contract. The deployment trap: evaluating with `model.train()` still on gives batch-dependent, wrong metrics that look fine if your eval batch is large — always eval in eval mode, and know that BN (unlike LayerNorm) changes behavior with batch size.

> [!tip] Interview answer
> Batch normalization standardizes each channel over the mini-batch and rescales with learnable gamma and beta, which smooths optimization, allows bigger learning rates, and slightly regularizes. At inference it uses frozen running statistics — the train/eval mode split is where real bugs live. For tiny batches or transformers, LayerNorm replaces it because it needs no batch statistics at all.

