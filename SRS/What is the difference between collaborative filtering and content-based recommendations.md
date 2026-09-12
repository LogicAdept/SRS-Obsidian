<!--
reps: 0
priority: 0
-->
#MachineLearning/Supervised #SRS

# What is the difference between collaborative filtering and content-based recommendations

> [!abstract] Short answer
> Collaborative filtering recommends from **behavior patterns of many users** ("users like you liked this") without needing to know what items are. Content-based recommends from **item features and a user's own history** ("you liked sci-fi, here is more sci-fi"). They fail differently: collaborative needs data density and suffers cold start for new users/items; content-based generalizes to new items but locks users into their past.

## How each works

* **Collaborative filtering** builds the user–item interaction matrix and factorizes it: learn a vector for each user and each item so that dot products reconstruct observed interactions — the matrix-factorization lineage, and the ancestor of learned embeddings: [[What is an embedding]]. Neighborhood variants (user-user, item-item) approximate the same idea with similarity counts.
* **Content-based** represents items by their attributes (genre, text embeddings, price tier), builds a user profile from items they liked, and scores new items by profile–item similarity. No other users' data is needed.

```text
CF:            ratings matrix R (users x items)  ->  U @ V^T ~ R
content-based: item features F + user's liked items -> similarity(F, profile)
```

**Listing 1.** CF is matrix completion on behavior; content-based is similarity search in a feature space.

```d2
direction: right
cf: "Collaborative filtering\nbehavior of many users\nlearns item+user vectors" {
  width: 260; height: 100
}
cb: "Content-based\nitem attributes\nuser's own history" {
  width: 250; height: 100
}
hy: "Hybrid\nboth signals\ncold-start covered" { width: 200; height: 90 }
cf -> hy; cb -> hy
```

**Fig. 1.** Production systems are hybrids: CF gives discovery and serendipity, content side covers cold start; blending is the standard architecture.

## Failure modes decide the choice

* **Cold start:** a brand-new item has no interactions — CF is blind until someone reacts; content-based handles it immediately if attributes exist. A brand-new user has no history — content side needs a profile bootstrap, CF can only lean on population priors.
* **Popularity bias and filter bubbles:** CF over-recommends what is already popular and can narrow the user's world; content-based over-narrows by construction. Discovery ("serendipity") is CF's strength.
* **Data demands:** CF needs dense overlap across users and items; sparse long-tail domains degrade it. Content quality depends on feature quality — garbage attributes, garbage recommendations, which makes the content side a [[What is feature engineering]] problem as much as a modeling one.

> [!warning] Interview trap
> "Collaborative filtering understands item content." It does not — a shoe and a hammer are similar if similar users interact with both. The reverse trap: "content-based personalizes" — not until the user has history; with a cold user it produces the same popular-content recommendations for everyone.

> [!tip] Interview answer
> Collaborative filtering learns from the interaction patterns of many users, typically via matrix factorization into user and item embeddings; content-based matches item attributes to one user's own history. I would contrast their cold-start behavior — content wins for new items, both struggle with new users — mention popularity bias and filter bubbles on the CF side, and say real systems blend both with a candidate-generation plus ranking structure.

