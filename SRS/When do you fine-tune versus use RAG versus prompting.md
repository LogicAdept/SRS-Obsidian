<!--
reps: 0
priority: 0
-->
#MachineLearning/LLM #SRS

# When do you fine-tune versus use RAG versus prompting

> [!abstract] Short answer
> Pick by **what is missing**. Prompting: the model already knows and can do the task — you only need to instruct. RAG: the missing piece is **knowledge** — fresh, private, or voluminous beyond the weights. Fine-tuning: the missing piece is **behavior** — style, format, latency-cheap skill, or task competence the base model lacks. They compose: mature systems combine two or three.

The decision is not about "which is more advanced" — it is a diagnosis. Wrong diagnosis, wasted months: fine-tuning to inject changing facts (RAG's job) or building RAG to fix a format-compliance problem that a few-shot prompt solves.

## The decision table

```text
missing:  instruction/clarity        -> prompting (few-shot, CoT, schemas)
missing:  fresh/private knowledge    -> RAG  (citations, updates, access control)
missing:  behavior/style/format      -> fine-tuning (LoRA; SFT; preference tuning)
missing:  both knowledge + behavior  -> RAG + fine-tuning (composed)
```

**Listing 1.** Knowledge lives outside the weights (RAG); behavior lives inside them (fine-tuning); instruction is free (prompting).

## The trade-offs that decide it

* **Prompting** costs nothing but window tokens and iteration; fragile to model updates and long-context dilution: [[What is an LLM and what is a context window]]. Start here, always.
* **RAG** adds an infrastructure surface (indexing, retrieval quality, rerankers) and buys freshness, provenance, and access control: [[What is retrieval augmented generation]]. Its failure mode is retrieval quality, not model quality.
* **Fine-tuning** (via LoRA: [[What is LoRA]]) buys consistent behavior at low inference cost — shorter prompts, tighter formats, domain styles; costs a training pipeline, versioning, and re-tuning on every base-model upgrade: [[What is transfer learning]]. Its failure mode is treating it as a knowledge dump — a fine-tuned model still needs retrieval for changing facts.

```d2
direction: right
p: "Prompting\ninstruct only\nzero training" { width: 190; height: 90 }
r: "RAG\nknowledge + citations\nindex infra" { width: 200; height: 90 }
f: "Fine-tune\nbehavior + format\ntraining pipeline" { width: 200; height: 90 }
p -> r: "facts change,\nneed provenance" { }
r -> f: "output must obey\na strict behavior" { }
```

**Fig. 1.** The escalation path: prompt first, add retrieval for knowledge, add fine-tuning for behavior — and expect the end state to combine them.

> [!warning] Interview trap
> "Fine-tune on your documents so the model knows them." Knowledge injection by fine-tuning is lossy, un-citable, and stale the day your documents change — that is RAG's job; fine-tuning teaches skill and format, not a changelog. Reverse trap: "just prompt harder" — some behaviors (strict schemas, niche styles, latency-critical short outputs) are genuinely cheaper and more reliable after light fine-tuning than after a page of instructions.

> [!tip] Interview answer
> I diagnose what is missing: instructions — prompt; knowledge — RAG; behavior — fine-tune; often both RAG and light LoRA. Prompting first because it is free and fast, RAG when freshness, citations, or access control matter, fine-tuning when behavior must be consistent and prompt-cheap. The two compose, and every choice is revisited on base-model upgrades.

