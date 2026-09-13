<!--
reps: 0
priority: 0
-->
#MachineLearning/DeepLearning/CNN #MachineLearning/DeepLearning/RNN #MachineLearning/DeepLearning/Transformers #SRS

# What is the difference between a CNN RNN and a transformer

> [!abstract] Short answer
> They are three ways to **connect information across positions**. CNN: local shared filters, spatial structure, parallel training. RNN: a recurrent state consumed token by token, sequential by nature. Transformer: self-attention lets every position look at every other in one step — global context, fully parallel training, quadratic cost in length.

## One table, three architectures

```text
CNN        local window, shared weights    O(k * n)     images, audio grids
RNN        sequential state update          O(n) steps   streaming, low-latency
transformer attention over all pairs      O(n^2) steps  language, vision (ViT)
```

**Listing 1.** Connectivity implies cost: local windows are cheap, all-pairs attention pays quadratically — see [[Why does self-attention scale poorly with sequence length]].

* **CNN** assumes locality and stationarity: great for grids ([[What is a convolutional neural network]]), weak for long-range token dependencies unless stacked deep.
* **RNN** carries a hidden state through time; it handles unbounded length in principle, but sequential training and fading gradients over long spans are its structural limits: [[What is an RNN and why do they struggle with long sequences]], fixed by gating in [[What is an LSTM]].
* **Transformer** drops recurrence entirely: self-attention compares all positions directly — [[What is self-attention]] — with positional encodings supplying order: [[What are positional encodings in a transformer]].

```d2
direction: right
c: "CNN\nlocal windows\nparallel, translation-aware" { width: 230; height: 90 }
r: "RNN\nstate through time\nsequential, O(n) memory" { width: 220; height: 90 }
t: "Transformer\nall-pairs attention\nparallel training, O(n^2)" { width: 240; height: 90 }
c -> t: "global context needed" { }
r -> t: "parallelization + long range" { }
```

**Fig. 1.** The transformer subsumes both predecessors' goals — local patterns via convolutions replaced by attention, recurrence replaced by position encodings and global context.

## How to answer "which to use"

Grid data with local structure: CNN (still king in vision baselines; ViT competes at scale). Streaming or strict-latency token processing: RNN/GRU variants still viable at the edge. Language, long-range dependencies, transfer learning at scale: transformer — the pretraining ecosystem alone decides most practical cases: [[What is transfer learning]]. The transformer's dominance is engineering plus scale, not a law of nature — its cost profile and data hunger are real limits.

> [!warning] Interview trap
> "Transformers replaced CNNs everywhere." Vision transformers need far more data or heavy pretraining to match CNN inductive biases on small datasets — locality is a strong prior, not a weakness. Reverse trap: "RNNs are dead" — they survive in streaming, low-resource, and latency-critical niches where quadratic attention is unacceptable.

> [!tip] Interview answer
> The difference is information flow: CNNs use local shared filters on spatial grids, RNNs thread a hidden state through time, and transformers attend across all positions at once with positional encodings standing in for order. Costs follow: convolution is linear, recurrence is inherently sequential, attention is quadratic but parallel. I would map each to its natural data — grids, streams, and language at scale respectively.

