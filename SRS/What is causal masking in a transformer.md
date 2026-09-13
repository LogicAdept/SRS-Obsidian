<!--
reps: 0
priority: 0
-->
#MachineLearning/DeepLearning/Transformers #SRS

# What is causal masking in a transformer

> [!abstract] Short answer
> Causal masking forbids attention to **future positions**: for autoregressive language modeling, token at position `t` may only attend to positions `≤ t`. It is implemented by setting the upper-triangular attention scores to −∞ before the softmax, so those pairs get zero weight. Without it, the model would peek at the answer it is supposed to predict.

The training objective — predict the next token from the left context — is only honest if the attention pattern enforces causality. The mask makes teacher-forced parallel training safe: all positions train simultaneously, each one blind to its future, so one forward pass yields every next-token prediction without leakage.

## Mechanics

```text
scores[i][j] = -inf  for j > i        # block the future
weights      = softmax(scores)        # future gets exactly 0
```

**Listing 1.** The mask is additive at the score level (−∞ before softmax), not a post-softmax zeroing — the distinction matters because softmax must still normalize over the allowed prefix only.

```python
import torch

n = x.size(1)
causal = torch.triu(torch.ones(n, n, dtype=torch.bool), diagonal=1)
scores = scores.masked_fill(causal, float("-inf"))
```

**Listing 2.** Upper-triangular boolean mask, `diagonal=1` keeps self-attention to the current token allowed.

```d2
direction: right
tok1: "token 1" { width: 120; height: 60 }
tok2: "token 2" { width: 120; height: 60 }
tok3: "token 3" { width: 120; height: 60 }
t1: "sees: 1" { width: 100; height: 55 }
t2: "sees: 1 2" { width: 110; height: 55 }
t3: "sees: 1 2 3" { width: 120; height: 55 }
tok1 -> t1; tok2 -> t2; tok3 -> t3
```

**Fig. 1.** Each position attends to a growing prefix — the triangular visibility that turns one parallel pass into training for every next-token prediction at once.

## Where masking applies and where it must not

Encoder–decoder models: the decoder is causal, the **encoder is not** — bidirectional context is legitimate when the task is not next-token generation (translation source, BERT-style MLM pretraining uses no causal mask at all). Prefix-LM variants expose a prompt bidirectionally and mask only the generated tail. During inference with a KV cache the mask is implicit: each new query attends to the cached prefix — [[What is the KV cache in LLM inference]]. Padding masks are a separate mechanism (blocking attention to pad tokens), and the two are combined additively in practice. Causality also interacts with positional encoding choice, since the mask plus relative encodings define what "left context" means numerically: [[What are positional encodings in a transformer]].

> [!warning] Interview trap
> "Causal masking slows training because of the triangular loop." It costs nothing extra computationally — it is one broadcast add before the softmax; the parallelism is untouched. The classic bug is the reverse: training a "language model" without the mask gives spectacular loss that is pure leakage — the model attends to the next token it is supposed to predict.

> [!tip] Interview answer
> Causal masking sets future-position attention scores to minus infinity before the softmax so each token sees only its prefix — enforcing the next-token objective while all positions still train in parallel. I would add that encoders and MLM pretraining intentionally skip it, that padding masks are a separate additive mask, and that at inference the KV cache makes causality implicit.

