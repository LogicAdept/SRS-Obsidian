<!--
reps: 0
priority: 0
-->
#MachineLearning/LLM #MachineLearning/Metrics #SRS

# How do you evaluate an LLM

> [!abstract] Short answer
> Layer the evaluation: **task metrics** where ground truth exists (exact match, F1, pass@k for code, win rate), **reference-based text metrics** (BLEU/ROUGE only as smoke tests), **model-graded evaluation** (LLM-as-judge with rubrics), and **human evaluation** for the final word. Add safety, robustness, and regression suites. A single number hides the failures that matter.

Classic generation metrics are weak proxies: ROUGE overlaps n-grams with references but says nothing about factual correctness or usefulness. Where the task is verifiable, prefer verifiable metrics: code execution tests (pass@k), structured extraction accuracy against gold schemas, retrieval hit rates for RAG pipelines.

## The evaluation stack

1. **Automated task metrics** — exact match, accuracy on multiple choice, pass@k with unit tests, schema-validity for extraction.
2. **Model-as-judge** — a strong LLM scores outputs against a rubric (correctness, completeness, tone). Watch judge biases: position bias, verbosity preference, self-preference; calibrate against a human-labeled subset.
3. **Human evaluation** — pairwise comparisons with raters, the gold standard for open-ended quality; expensive, so reserve for releases and judge calibration.
4. **Safety and robustness** — refusal behavior, jailbreak resistance: [[What is prompt injection]], distribution-shift robustness, and regression testing of prompts and versions.
5. **Online metrics** — production acceptance rates, edit distance by users, task completion: the arbiter of offline-vs-online gaps.

```python
# judge pattern with a fixed rubric and structured output
rubric = ("Score 1-5 for factual correctness against the source; "
          "return JSON {score, reasons}.")
# for task metrics: pass@k = fraction of problems solved by k sampled attempts
```

**Listing 1.** Two anchors: a fixed rubric for the judge, and verifiable pass@k-style metrics wherever execution is possible — vibes-based scoring without a rubric is noise.

## The discipline

Evaluation sets must be **held out and versioned** like test sets: [[What is a train validation test split]] — tuning prompts against your eval set quietly converts it into a training set. Version pinning matters: models, prompts, and retrieval corpora all change under you — the drift discipline of [[What is data drift]] applied to software. Cost-quality trade-offs are explicit: more sampling, longer judges, human review — each buys reliability with latency and money. This whole stack is the LLMOps core: [[How does LLMOps differ from MLOps]].

> [!warning] Interview trap
> "We evaluate with ROUGE/BLEU." For open-ended generation these measure n-gram overlap, not correctness — a paraphrase scores low, a fluent hallucination scores high. Second trap: using the same powerful model as judge and contestant without human calibration — self-preference bias inflates scores; and letting the eval set leak into prompt iteration is the LLM-era version of test-set leakage: [[What is data leakage in machine learning]].

> [!tip] Interview answer
> I evaluate LLMs in layers: verifiable task metrics where execution or ground truth exists, model-as-judge with fixed rubrics calibrated against humans, human pairwise review for releases, plus safety and regression suites. I would stress versioned held-out eval sets, the known judge biases, and treating offline scores as provisional until online task-completion metrics confirm them.

