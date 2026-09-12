<!--
reps: 0
priority: 0
-->
#MachineLearning/DeepLearning/Transformers #MachineLearning/DeepLearning/RNN #SRS

# Why did transformers replace RNNs

> [!abstract] Short answer
> Three reasons stacked: **parallel training** (all positions computed at once, no time-step dependency), **direct long-range access** (any token attends to any other in one hop, no state bottleneck), and **scale** (the architecture turned GPU parallelism and data into predictable quality gains). "Attention Is All You Need" (2017) removed recurrence; within three years recurrence was gone from state-of-the-art language models.

## The mechanics of the replacement

* **Sequential → parallel.** An RNN's step `t` waits for `t−1`, so training is bounded by sequence length. A transformer computes every position's representation in parallel: [[What is self-attention]]. Same hardware, orders-of-magnitude more tokens per second — which is what made pretraining on trillions of tokens economically possible.
* **State bottleneck → all-pairs access.** RNNs compress history into one fixed vector; information from 500 steps back must survive 500 updates. Attention compares current token with every token directly — the path length between any two positions is O(1) instead of O(n): [[What is an RNN and why do they struggle with long sequences]].
* **Order handled explicitly.** Recurrence encoded order implicitly; transformers must inject it via positional encodings: [[What are positional encodings in a transformer]] — a small price.

```text
RNN : h_t depends on h_{t-1}        -> training O(n) sequential steps
TRF : all tokens -> attention matrix -> one parallel matrix multiply set
```

**Listing 1.** The dependency structure change: from a chain to a single parallel computation with quadratic memory cost — [[Why does self-attention scale poorly with sequence length]].

## What RNNs did better — and the modern settlement

Per-step constant memory and streaming inference favored RNNs; quadratic attention cost is the transformer's real tax on very long contexts, and the efficient-attention line (sparse, linear, sliding-window) plus KV-cache engineering is the ongoing answer: [[What is the KV cache in LLM inference]]. State-space and linear-attention models partially revive recurrence ideas. But the practical verdict is settled for language at scale: pretraining economics, transfer ecosystems, and hardware fit all point one way: [[What is transfer learning]].

> [!warning] Interview trap
> "Transformers won because attention is mathematically superior." The deciding factors were parallelizable training and scale economics; attention's O(n²) cost is a genuine step back from RNN's O(n) sequential cost — the win is that GPUs parallelize it, not that it is cheaper. Saying "RNNs can't do long context" ignores that gated RNNs handled thousands of steps in production for years — just not competitively at scale.

> [!tip] Interview answer
> Transformers displaced RNNs because self-attention removed the sequential training dependency, gave every token direct access to every other — no fixed-state bottleneck — and turned sequence modeling into hardware-friendly parallel matrix math that scales predictably with data and compute. RNNs kept streaming and latency niches; the transformer's tax is quadratic attention, managed today by cache and efficient-attention engineering.

