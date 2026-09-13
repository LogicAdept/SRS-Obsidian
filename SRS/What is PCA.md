<!--
reps: 0
priority: 0
-->
#MachineLearning/Unsupervised #SRS

# What is PCA

> [!abstract] Short answer
> Principal component analysis finds **orthogonal directions of maximum variance** in the data and projects onto the top ones: the first principal component is the direction where the data varies most, the second the direction orthogonal to it with the next-most variance, and so on. It is the linear workhorse of dimensionality reduction, decorrelation, compression, and visualization.

Mechanically, PCA eigendecomposes the covariance matrix (or the SVD of the centered data matrix): eigenvectors are the components, eigenvalues the variance along them. "Explained variance ratio" tells how much of the total variance each component carries — the standard way to choose how many to keep.

## How it is used

* **Compression/denoising:** keep the top `k` components; reconstruct or work in the reduced space — variance-heavy directions dominate, small-noise directions drop.
* **Decorrelation:** PCA components are uncorrelated by construction — useful before models that assume or prefer non-collinear inputs; collinear raw features become clean axes — [[What is the difference between L1 and L2 regularization]] motivation.
* **Visualization:** project to 2–3 components for structure inspection.
* **Speed/stability:** reduce `p` before expensive downstream fitting.

```python
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

Xs = StandardScaler().fit_transform(X)     # PCA is variance-based: scale first
pca = PCA(n_components=0.95, svd_solver="full")  # keep 95% of variance
Z = pca.fit_transform(Xs)
print(pca.explained_variance_ratio_)       # variance per component
```

**Listing 1.** The standard recipe: center and scale, fit PCA to a variance budget, transform. Without scaling, wide-range features own the first components regardless of meaning.

## Limits and honest alternatives

PCA is linear — curved manifolds (swiss rolls) get flattened wrongly; kernel PCA, t-SNE, or UMAP handle non-linear structure, at higher cost and with less interpretability. Components mix original features, so interpretability suffers compared to the raw axes; loadings inspection partially recovers it. PCA is **unsupervised**: max-variance directions are not guaranteed predictive — a low-variance direction can carry all the target signal, so PCA-before-supervised-learning must be validated, not assumed: [[What is overfitting]] discipline and [[What is cross-validation]] pipelines apply. It also cannot be fit on train and test independently — the fitted projection must be frozen and replayed, see [[What is a train validation test split]].

> [!warning] Interview trap
> "PCA removes the least important features." It removes nothing — it **rotates** all features into variance-ranked combinations; dropping the last components is a separate decision, and "low variance equals unimportant" is false for prediction. Second trap: fitting PCA (or its scaler) on the full dataset before splitting — classic leakage that inflates downstream scores.

> [!tip] Interview answer
> PCA is an unsupervised linear projection onto orthogonal maximum-variance directions, computed via SVD of the centered — ideally scaled — data. I use it for compression, decorrelation, and visualization, choose the component count by explained-variance budget, and validate any supervised use downstream. Its limits: linearity, lost interpretability, and the fact that variance is not relevance.

