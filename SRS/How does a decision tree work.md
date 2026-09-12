<!--
reps: 0
priority: 0
-->
#MachineLearning/Supervised #SRS

# How does a decision tree work

> [!abstract] Short answer
> A decision tree recursively **splits the data on feature thresholds to reduce impurity**: at each node it searches over features and cut points for the split that best separates classes (or reduces variance), then repeats per branch until a stopping rule fires. Prediction walks the tree from root to leaf and returns that leaf's majority class or average target.

Training is greedy — the best split now, not a globally optimal tree (finding the optimum is NP-hard). The greediness plus depth control is why trees overfit fast when grown fully: a fully grown tree can memorize the training set one leaf per row.

## The split criterion

For classification, impurity is Gini or entropy; the split maximizes impurity reduction (information gain). For regression, it is variance reduction — squared-error improvement per split: [[What is a loss function]] vocabulary applies directly. Scikit-learn's `DecisionTreeClassifier` defaults to Gini and grows until leaves are pure or `min_samples_split` is hit.

```python
from sklearn.tree import DecisionTreeClassifier, export_text

clf = DecisionTreeClassifier(criterion="gini", max_depth=4,
                             min_samples_leaf=20, random_state=0)
clf.fit(X_tr, y_tr)
print(export_text(clf, feature_names=feature_names))  # the learned rules
```

**Listing 1.** A depth-4 tree with a minimum leaf size — the two knobs that keep the greedy memorizer honest; the printed rules are directly readable by humans.

## Why trees anchor ensembles

Trees capture non-linearities and interactions natively, need no scaling, handle mixed feature types, and are cheap to fit — which makes them ideal base learners. But a single deep tree has high variance: change a few rows and the structure changes. Bagging fixes that: [[What is a random forest]] averages many bootstrap trees; boosting builds trees sequentially on residuals: [[What is gradient boosting]] — and the two philosophies are compared in [[What is the difference between bagging and boosting]].

```d2
direction: down
root: "income > 50k?\n(gini drop best)" { width: 200; height: 80 }
l: "age > 30?" { width: 140; height: 70 }
r: "loan > 10k?" { width: 150; height: 70 }
ll: "class: A\n(43 rows)" { width: 140; height: 70 }
lr: "class: B" { width: 110; height: 60 }
rl: "class: B" { width: 110; height: 60 }
rr: "class: A\nhigh purity" { width: 130; height: 70 }
root -> l: "no"; root -> r: "yes"
l -> ll: "no"; l -> lr: "yes"
r -> rl: "no"; r -> rr: "yes"
```

**Fig. 1.** Axis-aligned splits chosen greedily for maximum impurity reduction; each leaf holds the prediction.

> [!warning] Interview trap
> "Trees find the globally optimal tree." They do not — the greedy split search is local, and two nearly identical datasets can yield different trees, which is exactly the variance that bagging exploits. Another classic: "trees don't need scaling" is true, but they also **cannot extrapolate** — outside the training range they output the nearest leaf's constant, unlike linear models which extend the plane.

> [!tip] Interview answer
> A decision tree greedily picks the feature and threshold that reduce impurity most, recurses, and predicts from the leaf — Gini or entropy for classification, variance for regression. I would note the greedy, high-variance nature and the controls (depth, min leaf size), its strengths — interpretability, no scaling, native interactions — and that its real-world dominance comes through ensembles like random forests and gradient boosting.

