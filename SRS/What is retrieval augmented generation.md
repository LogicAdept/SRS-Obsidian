<!--
reps: 0
priority: 0
-->
#MachineLearning/LLM #SRS

# What is retrieval augmented generation

> [!abstract] Short answer
> RAG **grounds generation in retrieved documents**: at query time, a retriever fetches relevant passages from an external corpus and stuffs them into the context window; the LLM answers using those passages as evidence instead of relying on memorized knowledge. It adds fresh, citable, controllable knowledge to a frozen model.

The pipeline has two halves. **Offline (indexing):** chunk documents, embed chunks with a text-embedding model — [[What is an embedding]] — and store vectors in a vector index for similarity search. **Online:** embed the query, retrieve top-k chunks (hybrid retrieval mixes vector search with keyword/BM25), optionally rerank, then generate with a prompt that frames chunks as sources.

## Why RAG beats memorization for knowledge

* **Freshness:** the index updates in minutes; the model's weights are frozen until retraining — the drift argument from [[What is data drift]] applied to knowledge.
* **Provenance:** answers can cite retrieved chunks, making verification and audit possible — the primary containment for [[What is an AI hallucination]].
* **Access control and scale:** per-user corpora, per-tenant indexes; knowledge beyond any context window, managed outside the model.
* **Cost:** no training cycle to update facts — the "no retrain" half of [[When do you fine-tune versus use RAG versus prompting]].

```d2
direction: right
q: "user question" { width: 140; height: 60 }
r: "retriever\n(embed + search)" { width: 160; height: 80 }
c: "top-k chunks" { width: 130; height: 60 }
g: "LLM\ngenerate with evidence" { width: 180; height: 80 }
a: "answer + citations" { width: 160; height: 60 }
idx: "vector index\n(chunk embeddings)" { width: 180; height: 80 }
q -> r -> c -> g -> a
idx -> r
```

**Fig. 1.** The online RAG loop: retrieve evidence into the context window, generate from it; index freshness lives outside the model.

## Where RAG quality actually breaks

Retrieval misses (wrong chunking, weak embeddings, vocabulary mismatch — hybrid search and rerankers fix most of it), context stuffing (too many chunks dilute attention in the window: [[What is an LLM and what is a context window]]), and generation ignoring or misreading the evidence. Evaluation must cover both halves: retrieval hit rate and faithfulness of the answer to the sources — [[How do you evaluate an LLM]]. Security note: retrieved content is untrusted input — the injection channel of [[What is prompt injection]].

> [!warning] Interview trap
> "RAG eliminates hallucination." It reduces unsupported claims and adds citations, but retrieval can miss, rerankers can mislead, and the generator can still override the evidence — measure faithfulness, do not assume it. Second trap: "RAG replaces fine-tuning" — they solve different problems: RAG injects knowledge, fine-tuning shapes behavior and format; mature systems often use both.

> [!tip] Interview answer
> RAG retrieves relevant chunks from an external index at query time and conditions the LLM's answer on them, giving fresh, citable, access-controlled knowledge without retraining. I would outline the offline indexing and online retrieve-generate halves, name the failure points — chunking, retrieval misses, context dilution, unfaithful generation — and stress measuring retrieval quality and faithfulness separately.

