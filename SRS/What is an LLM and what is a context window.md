<!--
reps: 0
priority: 0
-->
#MachineLearning/LLM #SRS

# What is an LLM and what is a context window

> [!abstract] Short answer
> A large language model is a **transformer trained to predict the next token** over massive text corpora — the objective is trivial, the scale is not: with billions of parameters and trillions of tokens, next-token prediction yields grammar, world knowledge, and in-context task performance. The **context window** is the model's working memory: the maximum number of tokens it can attend to in one request.

The architecture is the standard decoder-only transformer: tokenized input, [[What is self-attention]] over positions with [[What is causal masking in a transformer]], stacked blocks. Scale laws drove the "large": GPT-3 put 175 billion parameters into an autoregressive LM and demonstrated few-shot learning purely from prompts — no gradient updates at inference: [[What is transfer learning]] in its prompt-shaped form.

## The context window as a resource

Everything the model can use about your request must fit in the window: system prompt, conversation history, retrieved documents, the question, and the generated output share it. The window is finite (4k → 8k → 128k+ tokens over model generations) because attention is quadratic in it: [[Why does self-attention scale poorly with sequence length]]. Attention quality also degrades across the window — "lost in the middle" effects mean a huge window is not uniformly reliable memory.

```text
[ system prompt | retrieved docs | conversation history | user question | answer ]
<--------------------------- context window (tokens) ---------------------->
```

**Listing 1.** The window is a shared budget; RAG and prompt design are, at bottom, window-allocation policies: [[What is retrieval augmented generation]].

## How an LLM is used

Inference: tokenize, run the forward pass, sample the next token from the output distribution (temperature and top-p shape that sampling: [[What is temperature in an LLM]]), append, repeat — the KV cache makes the loop affordable: [[What is the KV cache in LLM inference]]. Adaptation options form a spectrum from zero-cost prompting to fine-tuning: [[When do you fine-tune versus use RAG versus prompting]], with LoRA making the heavy end cheap: [[What is LoRA]]. Operational reliability is its own discipline: [[What is an AI hallucination]], [[What is prompt injection]].

> [!warning] Interview trap
> "The LLM has a database of facts inside." It has a compressed statistical memory of training data — fluent, lossy, and dated; provenance and recency come from retrieval, not memorization. Second trap: "context window = memory" — it is attention span over the current request only; nothing persists between requests unless you engineer state externally.

> [!tip] Interview answer
> An LLM is a decoder-only transformer trained on next-token prediction at massive scale, which produces general language competence and few-shot in-context learning. The context window is the finite token budget the request, history, and retrieved material all share — bounded by quadratic attention. I would stress that it is a statistical memory, not a database, and that window allocation is the core design act in LLM applications.

