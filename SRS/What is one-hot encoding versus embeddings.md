<!--
reps: 0
priority: 0
-->
#MachineLearning/Embeddings #MachineLearning/Supervised #SRS

# What is one-hot encoding versus embeddings

> [!abstract] Short answer
> One-hot encoding represents a category as a **sparse binary vector with one 1** — dimensionality equals the number of categories, and all categories are equally distant. An embedding is a **learned dense vector** of fixed smaller size where geometry encodes similarity. One-hot is simple and exact; embeddings compress and generalize — but they must be learned, and they import their training assumptions.

The practical split: low-cardinality categorical features and models that handle sparsity well (linear models, trees via native categorical support) do fine with one-hot; high-cardinality data (words, users, products) needs embeddings or it blows up the feature space — [[What is an embedding]]. The encoding choice is one of the standard decisions of [[What is feature engineering]].

## Mechanics

```text
categories: {RU, DE, US}
one-hot RU = [1, 0, 0]        dist(RU, DE) == dist(RU, US)  # no similarity
embedding RU = [0.9, -0.2, 0.4]   (learned, dim << n_categories)
```

**Listing 1.** One-hot is a fixed binary code; the embedding is a trained vector whose dot products and distances carry meaning.

```python
from sklearn.preprocessing import OneHotEncoder
import torch, torch.nn as nn

ohe = OneHotEncoder(handle_unknown="ignore")
X_cat = ohe.fit_transform(df[["country"]])          # sparse (n, n_categories)
emb = nn.Embedding(num_embeddings=n_countries, embedding_dim=32)
# embeddings train jointly with the task; vectors are parameters
```

**Listing 2.** One-hot via scikit-learn for a handful of categories; an embedding table when the cardinality or the similarity structure demands it.

## Decision factors

* **Cardinality:** 10 countries — one-hot; 2 million products — embeddings, no contest.
* **Model class:** trees handle one-hot poorly with high cardinality (splits become hay needle searches) and often prefer native categorical handling or target encodings; linear models treat one-hot cleanly; neural networks require embeddings for id inputs.
* **Similarity signal:** if "RU behaves like KZ" is real signal, only embeddings can express it; one-hot makes every pair equidistant.
* **Cost:** embeddings need training data and care (dimension, initialization, collision of rare items); one-hot needs nothing but memory.

> [!warning] Interview trap
> "One-hot is always safe." With 50k categories it destroys tree models and inflates linear models, and `handle_unknown` decisions silently misbehave at serving time. The reverse trap: using pretrained embeddings for entity ids without checking that your entities were in the embedding's training world — out-of-world items get meaningless vectors; also one-hot embeddings trained on tiny data simply memorize noise.

> [!tip] Interview answer
> One-hot is an exact, sparse, similarity-blind encoding whose width equals cardinality; embeddings are dense learned vectors that encode similarity geometrically. I would choose one-hot for low-cardinality categories in linear models, embeddings for high-cardinality ids and neural networks, and mention the middle ground: target and frequency encodings with strict leakage control for tree models.

