<!--
reps: 0
priority: 0
-->
#MachineLearning/LLM #SRS

# What is temperature in an LLM

> [!abstract] Short answer
> Temperature is a **sampling parameter that rescales logits before softmax** — dividing by T. T < 1 sharpens the distribution (more deterministic, more repetitive), T > 1 flattens it (more diverse, more risk of nonsense), T → 0 approximates greedy argmax decoding. It changes generation behavior only — nothing about the model's weights or its judgments elsewhere in the pipeline.

Mechanically: probabilities become `softmax(z/T)`. At T = 0.1 the top token's mass dominates; at T = 1.5 the tail gets real probability. Note it is **not** "randomness added to the model" — it reshapes an existing distribution, then sampling draws from it. Frameworks expose it in generation configs (`temperature` in the HF `GenerationConfig`, `temperature` in the OpenAI-style APIs).

## Choosing a value

* **Factual, structured, extraction, code** — low temperature (0–0.3): you want the argmax, reproducibility for tests, and minimal fabrication pressure: hallucination risk rises with diversity: [[What is an AI hallucination]].
* **Creative generation, brainstorming, marketing copy** — moderate to high (0.7–1.2) with top-p as a companion control (nucleus sampling truncates the tail regardless of temperature).
* **Diversity-driven methods** (self-consistency, candidate ranking) — higher temperature to diversify candidates, then vote or verify: [[How do you evaluate an LLM]].

```python
from transformers import AutoModelForCausalLM, AutoTokenizer

model, tok = AutoModelForCausalLM.from_pretrained("gpt2"), AutoTokenizer.from_pretrained("gpt2")
ids = tok("The capital of France is", return_tensors="pt")
out = model.generate(**ids, max_new_tokens=5, do_sample=True,
                     temperature=0.2, top_p=0.9)
```

**Listing 1.** Low-temperature sampling for factual completion; `do_sample=False` ignores temperature entirely and goes greedy — a common confusion in reviews.

## Temperature and calibration

Temperature at generation time is decoupled from model calibration: a miscalibrated model stays miscalibrated at any T; confidence-adjusting temperature scaling is a separate calibration technique applied to logits for probability quality. Also note temperature interacts with the KV-cache decoding loop only through the sampling step — it has no cost implications: [[What is the KV cache in LLM inference]]. For agents, high temperature compounds over steps — each sampling error becomes context for the next decision.

> [!warning] Interview trap
> "Temperature makes the model smarter or dumber." It changes sampling sharpness only; quality differences come from when each setting is appropriate. Second trap: "temperature 0 guarantees the same output every time" — roughly yes for a fixed stack, but batch nondeterminism, hardware, and version changes can still flip tokens; reproducibility needs pinned seeds, versions, and greedy decoding.

> [!tip] Interview answer
> Temperature divides logits before the sampling softmax: below one sharpens toward argmax, above one flattens toward diversity, zero is greedy. I set it near zero for extraction, code, and factual answers, mid-range with top-p for creative generation, and I would stress it is a decoding knob — it neither improves the model nor guarantees byte-exact reproducibility at zero.

