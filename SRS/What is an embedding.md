<!--
reps: 0
priority: 0
-->
#MachineLearning/Embeddings #SRS

# What is an embedding

> [!abstract] Short answer
> An embedding is a **learned dense vector representation of a discrete object** — a word, user, product, image, or token — where geometric position encodes meaning: similar objects land near each other. Embeddings turn untyped IDs into fixed-length real vectors that models and similarity searches can actually work with.

The alternative to an embedding for categorical data is one-hot encoding: a vector as long as the vocabulary, almost all zeros, with no notion of similarity (any two distinct items are equally far apart). Embeddings compress that to a chosen dimensionality and learn similarity from data — the comparison is its own card: [[What is one-hot encoding versus embeddings]].

## How they are learned

An embedding is a lookup table: one trainable vector per item. Training makes the vectors useful as a side effect of some objective — predicting a word from context (word2vec), predicting masked tokens, or serving as the input layer of any neural net trained on IDs. In PyTorch, `nn.Embedding(vocab_size, dim)` is literally a matrix of shape `(vocab_size, dim)` whose rows are the vectors. LLMs tokenize text and embed every token; the same mechanism underlies [[What is an LLM and what is a context window]].

```python
import torch, torch.nn as nn

emb = nn.Embedding(num_embeddings=50_000, embedding_dim=128)  # 50k rows x 128
ids = torch.tensor([[17, 942, 305]])   # a sequence of item/token ids
vectors = emb(ids)                     # shape (1, 3, 128): dense vectors
```

**Listing 1.** An embedding layer maps integer ids to dense rows; the rows are parameters learned by backpropagation like any other weights.

## Why geometry is the point

Once objects are vectors, "similar" becomes computable: dot product, cosine similarity, or Euclidean distance. That is what makes semantic search, recommendations, duplicate detection, and RAG retrieval possible — the retrieval half is covered in [[What is retrieval augmented generation]]. Dimensionality reduction methods like [[What is PCA]] can also produce embeddings of features rather than items, and recommendation systems live on learned user/item vectors: [[What is the difference between collaborative filtering and content-based recommendations]].

> [!warning] Interview trap
> "Embeddings understand meaning." They encode statistical co-occurrence of the training data — including its biases and its gaps. An embedding space is valid only for the distribution it was trained on; mixing embeddings from different models, or applying an e-commerce text embedder to medical notes, produces plausible-looking garbage. Also, cosine similarity on raw embeddings is a baseline, not a guarantee — domain-specific fine-tuning or re-ranking is usually required.

> [!tip] Interview answer
> An embedding is a learned dense vector for a discrete item, positioned so that proximity reflects similarity, learned as a lookup table by some training objective. I would contrast it with one-hot vectors, name word2vec and transformer token embeddings as canonical examples, and explain that the payoff is making semantic similarity a geometric computation that powers search, recommendations, and RAG.

