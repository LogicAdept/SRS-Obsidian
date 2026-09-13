<!--
reps: 0
priority: 0
-->
#MachineLearning/LLM #SRS

# What is the KV cache in LLM inference

> [!abstract] Short answer
> The KV cache stores the **keys and values of already-processed tokens** so that generating the next token does not recompute attention over the whole prefix. Autoregressive decoding adds one token at a time; with the cache, each step's new query attends to cached K/V of the past — turning per-token cost from "recompute everything" into "compute one step".

Mechanically: during the prefill (prompt processing), all positions' K and V are computed and stored per layer. Decode steps append each new token's K/V. Without the cache, generating token `t+1` would recompute attention for all `t` tokens — O(t²) work repeated; with it, each step costs one query against the cache — O(t) — and the model runs the new token only. The causal mask's "attend to prefix" semantics is exactly what makes the cache sound: [[What is causal masking in a transformer]].

## The memory bill

Cache size = `2 (K and V) × layers × heads × head_dim × seq_len × batch × bytes`. In fp16, a 7B model's cache runs ~0.5 MB per token — a 32k-token context on a batch of 8 is over 100 GB — the cache, not the weights, becomes the serving bottleneck for long contexts: [[Why does self-attention scale poorly with sequence length]]. Mitigations: **grouped-query attention** (fewer K/V heads shared across queries — smaller cache with minor quality cost), cache **quantization** (fp8/4-bit KV), **paged attention** (vLLM-style memory paging that removes fragmentation), and sliding-window or cache-eviction schemes.

```python
out = model.generate(**ids, max_new_tokens=256, use_cache=True)
# prefill: one forward over the prompt -> K/V cached per layer
# decode: 256 steps, each attends to cached K/V, appends its own K/V
```

**Listing 1.** `use_cache=True` is the default in HF generate; the split between one prefill pass and incremental decode steps is where serving latency lives.

## Prefill, decode, and serving consequences

* **Prefill** is compute-bound (parallel over prompt tokens); **decode** is memory-bandwidth-bound (one token, reading the whole cache) — batching many requests amortizes the weight reads, which is why serving stacks obsess over batch scheduling.
* **Long context** raises prefill cost quadratically and cache size linearly — prompt caching (reusing the prefix cache across requests with a shared system prompt) attacks exactly this.
* **Multi-tenant LoRA** serving pairs with paged caches so adapters share the base model's cache pool: [[What is LoRA]].

> [!warning] Interview trap
> "The KV cache stores embeddings." It stores per-layer keys and values — the intermediate attention material — not token embeddings, and it is per-request state you must manage (evict, page, batch). Second trap: "cache makes long contexts free" — it removes recomputation, but memory still grows linearly with context and batch; that growth is the constraint the mitigations above exist for.

> [!tip] Interview answer
> The KV cache keeps each layer's keys and values for processed tokens so decode steps compute one token at a time against the prefix instead of recomputing attention — prefill is compute-bound, decode is bandwidth-bound. The cost is linear-in-context memory that scales with batch, so serving uses grouped-query attention, quantized and paged caches, and prefix caching; causality is what makes the cache correct.

