<!--
reps: 0
priority: 0
-->
#MachineLearning/DeepLearning/Transformers #SRS

# What is self-attention

> [!abstract] Short answer
> Self-attention lets every token build its representation by **querying all other tokens**: each token projects to a query, key, and value vector; scores are `QKᵀ/√d_k`, normalized by softmax, and the output is the weighted sum of the values. "Self" means the sequence attends to itself — relations between tokens are computed, not walked through a state.

The roles: **query** — what I am looking for; **key** — what I advertise; **value** — what I contribute if selected. The dot product of a query with every key scores relevance; softmax turns scores into weights; the weighted value sum is the new representation. Scaling by `√d_k` keeps the dot products' variance from saturating the softmax — a two-word answer with real consequences: unscaled high-dimensional dot products push softmax into one-hot regions and kill gradients.

## The computation

```text
scores    = Q @ K^T / sqrt(d_k)          # (n, n) relevance matrix
weights   = softmax(scores, axis=-1)     # rows sum to 1
output    = weights @ V                  # contextualized representations
```

**Listing 1.** Scaled dot-product attention; masking happens before the softmax — see [[What is causal masking in a transformer]].

```python
import torch, torch.nn.functional as F

def self_attention(Q, K, V, mask=None):
    scores = Q @ K.transpose(-2, -1) / Q.size(-1) ** 0.5
    if mask is not None:
        scores = scores.masked_fill(mask, float("-inf"))
    return F.softmax(scores, dim=-1) @ V
```

**Listing 2.** The whole mechanism in PyTorch: project, score, mask, softmax, mix. Parameter count: three projection matrices of `d_model × d_k` — plus an output projection in the multi-head version: [[What is multi-head attention]].

```d2
direction: right
q: "Q: what I seek" { width: 160; height: 70 }
k: "K: what I offer" { width: 160; height: 70 }
s: "QK^T / sqrt(d_k)\nrelevance scores" { width: 200; height: 80 }
w: "softmax\nattention weights" { width: 170; height: 70 }
v: "V: content to mix" { width: 160; height: 70 }
out: "weighted sum\ncontextual output" { width: 190; height: 70 }
q -> s; k -> s; s -> w; w -> out; v -> out
```

**Fig. 1.** Queries and keys produce weights; values are mixed by those weights — the output for a token is a content-addressed combination of the sequence.

## Why it took over

One hop between any two positions (no recurrence chain), full parallelism over positions, and content-based routing — each token's mixture is decided by the data, not by a fixed connectivity pattern. The costs are the quadratic score matrix — [[Why does self-attention scale poorly with sequence length]] — and the loss of order information, patched by positional encodings: [[What are positional encodings in a transformer]]. This mechanism, stacked with feed-forward blocks and residuals, is the entire transformer: [[What is the difference between a CNN RNN and a transformer]].

> [!warning] Interview trap
> "Self-attention means the model attends to itself at the same position." It means sources and destinations are the same sequence — every token attends to all positions including itself, versus cross-attention where queries come from one sequence and keys/values from another. Second trap: forgetting the `√d_k` scale or the pre-softmax masking order — both are standard follow-up probes.

> [!tip] Interview answer
> Self-attention projects each token to query, key, and value; scales the query-key dot products by root d-k, applies causal or padding masking, softmaxes into weights, and outputs a weighted mix of values. It gives one-hop global context and full parallelism, which is the core of the transformer; the costs are the quadratic score matrix and needing explicit positional information.

