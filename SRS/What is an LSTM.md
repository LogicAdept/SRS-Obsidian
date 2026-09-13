<!--
reps: 0
priority: 0
-->
#MachineLearning/DeepLearning/RNN #SRS

# What is an LSTM

> [!abstract] Short answer
> A Long Short-Term Memory network is a gated RNN cell that **maintains a separate cell state as a gradient highway**, updated through learnable input, forget, and output gates. The gates decide what to write, what to erase, and what to expose — making long-range dependencies trainable where vanilla RNNs forget.

The design insight: instead of forcing every history through a squashed hidden state, keep an additive cell state `c_t` — `c_t = f_t ⊙ c_{t-1} + i_t ⊙ g_t` — where the forget gate `f_t` near one lets information flow across hundreds of steps with almost no gradient decay. The hidden state `h_t = o_t ⊙ tanh(c_t)` is the exposed view of the cell.

## The gates

* **Forget gate** `f_t = σ(W_f·[h_{t-1}, x_t])` — what fraction of old cell state to keep; per-dimension, so the cell can selectively erase.
* **Input gate** `i_t` plus candidate `g_t = tanh(...)` — what new content to write.
* **Output gate** `o_t` — what part of the cell state to reveal as `h_t`.

All gates are small neural layers with sigmoid/tanh activations — cheap, and the additive cell-state update is what breaks the multiplicative gradient chain: [[What are vanishing and exploding gradients]].

```python
import torch.nn as nn

lstm = nn.LSTM(input_size=128, hidden_size=256, num_layers=2,
               batch_first=True, bidirectional=False)
# out, (h_n, c_n) = lstm(x)      # c_n is the cell state highway
```

**Listing 1.** PyTorch's LSTM returns both the hidden and cell states; the cell state is the long-memory channel the gates maintain.

## Where LSTMs stand now

Before transformers, LSTMs owned sequence modeling — translation, speech, time series — and still hold niches: streaming and low-latency inference (constant memory per step), small-data regimes, time series with modest horizons. Their sequential nature keeps training non-parallel — the structural reason transformers displaced them at scale: [[Why did transformers replace RNNs]]. Gated linear units and state-space models inherit the gating idea in modern form; the architectural comparison is in [[What is the difference between a CNN RNN and a transformer]].

> [!warning] Interview trap
> "LSTM solves vanishing gradients." It **mitigates** them along the additive cell-state path; gradients through the gate paths still shrink, and very long dependencies (thousands of steps) remain hard — attention replaced recurrence precisely for unbounded-context tasks. Second trap: "the cell state and hidden state are the same thing" — no; `c_t` is the protected memory, `h_t` is its gated readout.

> [!tip] Interview answer
> An LSTM is a gated recurrent cell: forget, input, and output gates control a separate cell state that updates additively, giving gradients a near-identity path across many steps. That is what made long-range sequence learning practical pre-transformer. Today it survives in streaming and low-latency settings, while transformers took large-scale sequence modeling because they parallelize and attend over full context.

