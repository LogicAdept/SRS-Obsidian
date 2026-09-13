<!--
reps: 0
priority: 0
-->
#MachineLearning/DeepLearning/Transformers #SRS

# What is multi-head attention

> [!abstract] Short answer
> Multi-head attention runs **several self-attention operations in parallel subspaces**: the model dimension is split into `h` heads, each head computes its own attention with its own projections, and the outputs are concatenated and mixed by an output projection. Different heads learn different relation types — syntax, coreference, positional patterns — instead of averaging them into one attention distribution.

Why split? One attention distribution must average all relation types into a single weighted mix; a head focused on adjacency cannot also track long-range coreference at full strength. Splitting into subspaces (each of dimension `d_model/h`) lets each head specialize while total compute stays close to one full-dimensional attention.

## The computation

```text
head_i = Attention(Q W_i^Q, K W_i^K, V W_i^V)     # d_k = d_model / h
MHA(X) = Concat(head_1..head_h) W^O
```

**Listing 1.** Per-head projections, independent attention, concatenation, output mixing. Note the budget: with `d_k = d_model/h`, total cost matches single-head attention of the same width — the specialization is nearly free.

```python
import torch.nn as nn

mha = nn.MultiheadAttention(embed_dim=512, num_heads=8, batch_first=True)
out, attn = mha(query=x, key=x, value=x)   # self-attention with 8 heads
```

**Listing 2.** The PyTorch call; eight heads of dimension 64 over a 512-wide model is the canonical BERT-era configuration — [[What is self-attention]] holds per head unchanged, including scaling by `√d_k`.

## What heads actually learn

Empirically (BERTology-style probing): some heads track adjacent tokens, some attend to punctuation and sentence boundaries, some capture syntactic relations or rare-token links; many heads are prunable with little loss — the specialization is real but uneven. Heads also give the only interpretable window into attention (attention maps per head), with the caveat that attention weights are not explanations by themselves. Transformers stack multiple MHA layers so lower layers can handle local patterns and higher ones composition: [[What is the difference between a CNN RNN and a transformer]].

```d2
direction: right
x: "input X" { width: 120; height: 60 }
h1: "head 1\nlocal relations" { width: 150; height: 80 }
h2: "head 2\nlong-range" { width: 140; height: 80 }
h3: "head 3..h\nspecialized" { width: 140; height: 80 }
cat: "concat" { width: 110; height: 60 }
proj: "output proj W^O" { width: 160; height: 70 }
x -> h1; x -> h2; x -> h3
h1 -> cat; h2 -> cat; h3 -> cat
cat -> proj
```

**Fig. 1.** Parallel heads over projection subspaces, concatenated and mixed — specialization without extra width.

> [!warning] Interview trap
> "Multi-head attention is more expensive than single-head." With the standard split (`d_k = d_model/h`) the parameter and FLOP budgets are comparable — you buy diversity, not capacity. Second trap: "more heads are always better" — beyond the model width, heads shrink per-head dimension and dilute expressiveness; head count scales with `d_model` and is routinely pruned.

> [!tip] Interview answer
> Multi-head attention runs h parallel self-attentions on projected subspace slices, concatenates them, and mixes with an output projection — letting different heads capture different relation types simultaneously. The split keeps compute roughly equal to single-head attention. I would mention learned head specialization, that head count trades against per-head width, and that this sits at the center of every transformer layer.

