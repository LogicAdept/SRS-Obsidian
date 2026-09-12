<!--
reps: 0
priority: 0
-->
#MachineLearning/LLM #SRS

# What is an AI hallucination

> [!abstract] Short answer
> A hallucination is a **fluent, confident output that is factually wrong or unsupported** — invented citations, nonexistent API methods, wrong dates, fabricated quotes. It is not a bug in the usual sense: next-token prediction optimized for plausible continuation will produce plausible falsehoods whenever training signal and truth diverge.

The mechanism: an LLM is a compressed statistical model of its training text — [[What is an LLM and what is a context window]]. When asked about something underrepresented, it interpolates: the result looks exactly like a real answer because it is built from the same patterns that produce real answers. Calibration is the core issue — the model does not reliably know what it does not know, and decoding parameters (high temperature, low top-p thresholds) modulate how strongly it commits: [[What is temperature in an LLM]].

## Mitigations that actually work

* **Grounding:** retrieval-augmented generation pins generation to retrieved sources; answers cite evidence instead of memory: [[What is retrieval augmented generation]].
* **Decoding discipline:** lower temperature for factual tasks; asking for "unknown" options in prompts reduces confident fabrication at the margins.
* **Verification passes:** self-check prompts, cross-model review, and program-of-thought — verify arithmetic and facts with tools, not with more generation.
* **Provenance and citation:** force claims to reference retrieved chunks; unverified claims get flagged — makes hallucinations detectable rather than invisible.
* **Fine-tuning with truthful refusal data** teaches calibrated abstinence — the RLHF flavor of honesty training: [[When do you fine-tune versus use RAG versus prompting]].

```text
user:  What is the return policy of store X?
risk:  model invents "30 days, no receipt needed"
grounded: retrieval finds policy doc -> answer cites it or says "not found"
```

**Listing 1.** The canonical fix pattern: for anything fact-bound and changeable, retrieval plus citation replaces memorized guessing.

## What hallucination is not

Not randomness (it is systematic interpolation), not always harmful (creative writing wants invention), and not eliminated by scale alone — larger models hallucinate more persuasively. The engineering posture is containment: constrain fact-bound flows with grounding and verification, measure hallucination rates on held-out evals: [[How do you evaluate an LLM]], and design products so a wrong answer is catchable before it is trusted — that monitoring discipline is [[How does LLMOps differ from MLOps]] territory.

> [!warning] Interview trap
> "Hallucinations mean the model was trained on bad data." Even perfect data leaves the problem: the objective rewards plausibility, not truth, and the model cannot introspect its own uncertainty reliably. Second trap: "RAG eliminates hallucinations" — it replaces memorization with retrieval, which introduces retrieval misses and misreadings; grounded models hallucinate less, not never.

> [!tip] Interview answer
> A hallucination is confident, fluent, false output — the natural product of next-token prediction when truth and training plausibility diverge. The realistic mitigations are grounding with retrieval and citations, conservative decoding for factual tasks, verification tooling, and honest-refusal fine-tuning. I would frame it as a containment and measurement problem, not a bug to patch: eval sets must measure it, products must catch it.

