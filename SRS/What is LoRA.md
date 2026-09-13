<!--
reps: 0
priority: 0
-->
#MachineLearning/LLM #SRS

# What is LoRA

> [!abstract] Short answer
> LoRA (Low-Rank Adaptation) fine-tunes a large model by **freezing all pretrained weights and training small low-rank update matrices**: instead of updating a `d × k` weight matrix W, it learns `ΔW = B·A` where `A` is `r × k` and `B` is `d × r` with a tiny rank `r` (often 8–64). Trainable parameters drop by orders of magnitude; at inference `ΔW` merges into W, adding zero latency.

The insight from "LoRA: Low-Rank Adaptation of Large Language Models" (Hu et al., 2021): fine-tuning updates are effectively **low-rank** — most of the needed change lives in a small subspace. So the update is parameterized as a product of two skinny matrices; initialization keeps `A` random, `B` zero, so the adapted model starts identical to the pretrained one.

## Why it dominates practical LLM fine-tuning

* **Memory:** with rank 16 on a 7B model, trainable parameters fall from 7B to tens of millions — the optimizer state (Adam moments, the real memory hog: [[What is the difference between Adam and SGD]]) shrinks with them, so one consumer GPU can fine-tune what full fine-tuning could not.
* **Swappable adapters:** the frozen base model stays on disk once; per-task LoRA modules are megabytes — switching tasks is loading a different adapter, not a different model: the deployment story in [[What is a model in machine learning]].
* **No inference cost:** adapters merge into the base weights (`W' = W + B·A`), or stay separate for multi-tenant serving — both supported by common stacks (PEFT, vLLM-style LoRA serving).
* **Quality:** on instruction tuning and domain adaptation, LoRA typically matches full fine-tuning at modest ranks; higher ranks only matter for tasks far from pretraining.

```python
from peft import LoraConfig, get_peft_model
import transformers

cfg = LoraConfig(r=16, lora_alpha=32, lora_dropout=0.05,
                 target_modules=["q_proj", "v_proj"])
model = get_peft_model(base_model, cfg)   # only A, B matrices trainable
model.print_trainable_parameters()        # ~0.5% of parameters
```

**Listing 1.** The PEFT recipe: rank 16, scaling `alpha/r = 2`, attention projections as targets. `lora_alpha` scales the update: effective step is `alpha/r · B·A`.

## Scope and limits

LoRA targets **adaptation**, not knowledge injection: large-scale new knowledge is better served by continued pretraining or retrieval — [[When do you fine-tune versus use RAG versus prompting]], [[What is retrieval augmented generation]]. Quantized variants (QLoRA) push memory further by keeping the frozen base in 4-bit. Beyond LLMs the same recipe adapts diffusion models and vision backbones — the transfer-learning spectrum in [[What is transfer learning]] with a parameter-efficient middle rung.

> [!warning] Interview trap
> "LoRA reduces inference latency." The opposite is its selling point: merged LoRA adds **zero** latency and unmerged adds a tiny matmul — it reduces training cost, not inference cost. Second trap: "rank is the only knob" — `alpha`, target module choice, and dropout matter as much; targeting all linear layers usually beats attention-only at the same rank.

> [!tip] Interview answer
> LoRA freezes the pretrained weights and learns low-rank update matrices BA per targeted layer, cutting trainable parameters by two orders of magnitude while matching full fine-tuning on typical adaptation tasks. Adapters merge into the weights for zero-latency inference or stay hot-swappable per task. I would add alpha-over-rank scaling, choosing target modules, and that LoRA adapts behavior — new knowledge still needs retrieval or continued pretraining.

