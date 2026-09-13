<!--
reps: 0
priority: 0
-->
#MachineLearning/Supervised #SRS

# What is supervised learning

> [!abstract] Short answer
> Supervised learning trains a function on **labeled examples** `(x, y)` so that it predicts `y` for new `x`. The label gives you a target to be wrong about, which is why every supervised method is built around a loss comparing predictions to true labels.

The name comes from the training signal acting like a supervisor: for every input the learner is told the right answer. Classification predicts a discrete class (spam or not), regression predicts a continuous number (price in dollars). Both use the same skeleton — model class, loss, optimizer — differing in loss and output shape.

## How training actually works

1. Split data into training and held-out evaluation sets; the split discipline is the whole game, see [[What is a train validation test split]].
2. Choose a model family `f(x; θ)` with parameters `θ`: linear model, tree, k-NN, neural network.
3. Choose a loss `L(f(x), y)`: cross-entropy for classification, squared error for regression — see [[What is a loss function]].
4. Optimize `θ` to minimize average loss, usually by gradient descent variants: [[What is gradient descent]].
5. Evaluate honestly on held-out data and watch for [[What is overfitting]].

```python
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

X_tr, X_te, y_tr, y_te = train_test_split(X, y, stratify=y, random_state=0)
clf = LogisticRegression(C=1.0, max_iter=1000)
clf.fit(X_tr, y_tr)                    # labels y_tr supervise the fit
pred = clf.predict(X_te)
print(accuracy_score(y_te, pred))      # honest score on unseen rows
```

**Listing 1.** The supervised skeleton in scikit-learn: fit on labeled training rows, score on rows the estimator never saw.

## What makes a supervised problem hard

Label quality dominates: mislabeled or leaked labels teach the model exactly the wrong lesson. Label cost matters too — supervised learning needs someone to produce `y`, which is why semi-supervised and self-supervised pretraining exist for the cases where labels are expensive. When labels are rare and actions have delayed payoffs, that is the reinforcement setting instead; the boundary is drawn in [[What is the difference between supervised unsupervised and reinforcement learning]].

> [!warning] Interview trap
> "Supervised means the human is in the loop during inference." No — supervision is a **training-time** property of the dataset. At inference a supervised classifier runs exactly like any other function. Also, having labels for training does not save you from evaluation mistakes: labels leaking into features is the classic disaster, see [[What is data leakage in machine learning]].

> [!tip] Interview answer
> Supervised learning is fitting a mapping from inputs to known labels with an explicit loss, then trusting it only if it generalizes to held-out data. I would name classification versus regression as the two flavors, mention that label cost is the practical bottleneck, and stress that the honest train/test discipline is what separates real supervised modeling from curve fitting on the whole dataset.

