<!--
reps: 0
priority: 0
-->
#MachineLearning/DeepLearning/Transformers #SRS

# What are positional encodings in a transformer

> [!abstract] Short answer
> Self-attention is **permutation-invariant** — shuffle the input tokens and, without help, the outputs shuffle identically: no notion of order exists inside the mechanism. Positional encodings inject position information by adding position-dependent vectors to token embeddings, restoring sequence order to the model.

The original transformer used **sinusoidal encodings**: fixed functions of sine and cosine at different frequencies, added to embeddings — attractive because values are bounded, each position gets a unique signature, and relative offsets generalize to unseen lengths. Learned absolute embeddings (BERT-era) are a table indexed by position — simple, but capped at the trained maximum length.

## The family tree

* **Absolute added encodings:** sinusoidal or learned tables added to token embeddings — the baseline.
* **Relative encodings:** attention scores modified by pairwise position differences (T5-style biases, rotary embeddings/RoPE) — rotate Q and K so their dot product depends on relative offset; the modern default for LLMs and the trick that makes context extension plausible: [[What is the KV cache in LLM inference]].
* **Architectural:** ALiBi adds linear distance penalties to attention scores; some architectures dispense with explicit encodings via local structure (convolutional patches in ViT).

```python
import numpy as np

def sinusoidal(max_len, d_model):
    pos = np.arange(max_len)[:, None]
    i = np.arange(d_model)[None, :]
    angle = pos / np.power(10000, 2 * (i // 2) / d_model)
    enc = np.zeros((max_len, d_model))
    enc[:, 0::2], enc[:, 1::2] = np.sin(angle[:, 0::2]), np.cos(angle[:, 0::2])
    return enc
```

**Listing 1.** Sinusoidal positional encoding: paired sine/cosine frequencies give every position a unique, smoothly varying vector.

## Why order matters at all

"Dog bites man" versus "man bites dog": bag-of-words content is identical; meaning lives in order. Attention itself computes content-addressed mixtures — position enters only through these encodings, which is why removing them collapses transformers on language. Relative schemes matter for length generalization: absolute encodings trained at 4k positions do not transfer to 32k, while rotary schemes interpolate or extend with modest fine-tuning — directly relevant to LLM context windows: [[What is an LLM and what is a context window]].

> [!warning] Interview trap
> "Positional encodings are fed through a separate layer." The classic ones are **added to input embeddings** before the first block — no separate processing stage. Second trap: "attention handles order itself" — it provably does not; permutation invariance is a theorem, not a quirk. And sinusoidal versus learned is not settled religion — relative/RoPE-style schemes are what modern LLMs actually ship.

> [!tip] Interview answer
> Self-attention is permutation-invariant, so the transformer must inject order explicitly: position-dependent vectors added to embeddings in the original design, pairwise-relative biases or rotary encodings in modern models. I would name sinusoidal and learned absolute encodings as the classics, note RoPE as the current LLM default because it encodes relative offsets and supports context extension, and stress that without any of this, attention is a bag-of-words mixer.

