<!--
reps: 0
priority: 0
-->
#MachineLearning/DeepLearning/RNN #SRS

# What is an RNN and why do they struggle with long sequences

> [!abstract] Short answer
> A recurrent neural network processes a sequence **one element at a time, carrying a hidden state** that summarizes everything seen so far: `h_t = f(W_x x_t + W_h h_{t-1} + b)`. The same weights apply at every step. The struggle: training unrolls the recurrence through time, and gradients multiplied across many steps either vanish or explode — so vanilla RNNs forget long-range dependencies.

The hidden state is a fixed-size bottleneck: information from step 1 must survive hundreds of multiplicative updates to influence step 500. Backpropagation through time multiplies Jacobians of the recurrent map — the same product structure that plagues deep nets, concentrated in one recurrent weight matrix: [[What are vanishing and exploding gradients]]. Exploding is handled by clipping; **vanishing is structural** — a fixed-size state with repeated squashing cannot hold long histories reliably.

## Consequences in practice

Effective memory horizon is short: token 500 barely sees token 5. Gradient signal from late losses to early inputs decays, so early-token representations stay near-random. Sequential computation — step `t` needs `t−1` — blocks parallel training, making RNNs slow on modern hardware precisely where transformers excel: [[Why did transformers replace RNNs]].

```python
import torch.nn as nn

rnn = nn.RNN(input_size=128, hidden_size=256, num_layers=2, batch_first=True)
# forward: outputs, h_n = rnn(x, h0)
# x: (batch, seq_len, 128); the same cell weights act at every step
```

**Listing 1.** The recurrent cell contract: identical weights across time steps, state threading through the sequence — elegant and exactly the source of its limits.

## What was built on top

Gating fixes the gradient path: LSTMs and GRUs add learnable gates that keep a cell-state highway with near-identity gradients — long memory becomes trainable: [[What is an LSTM]]. Bidirectional variants read both directions for offline tasks. And the architectural endpoint: replace the recurrence with attention over all positions — the transformer — which removes the state bottleneck and the sequential training constraint entirely: [[What is the difference between a CNN RNN and a transformer]].

> [!warning] Interview trap
> "RNNs remember long sequences via the hidden state." In theory the state has capacity; in practice gradients from far steps vanish and the state is dominated by recent inputs — that is the failure, not a design choice. Second trap: "exploding gradients make RNNs untrainable" — clipping solves those; the hard problem is vanishing, which is why gated cells were invented.

> [!tip] Interview answer
> An RNN applies the same cell across time steps, compressing the past into a running hidden state. Its two structural problems are vanishing gradients over long unrolls — hence short effective memory — and sequential training that cannot parallelize. Gated cells mitigate the memory issue, and the transformer removed the bottleneck by replacing recurrence with attention.

