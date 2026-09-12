<!--
reps: 0
priority: 0
-->
#MachineLearning/DeepLearning #SRS

# How does a neural network learn

> [!abstract] Short answer
> A neural network learns by **iterating one loop**: forward pass produces predictions, a loss scores them against targets, backpropagation computes gradients of that loss for every weight, and an optimizer nudges weights a small step against the gradient — repeated over many mini-batches and epochs until validation performance stops improving.

Nothing in the loop "understands" — the network is a parameterized function whose weights are moved downhill on the loss surface. What makes it powerful is composition: layers of nonlinear transforms ([[Why do neural networks need nonlinear activations]]) create features progressively, and gradient descent in that huge parameter space reliably finds good solutions given the right conditions.

## The loop, concretely

1. **Batch forward:** a mini-batch flows through the network — [[What is the difference between batch SGD and mini-batch gradient descent]] explains why mini-batches.
2. **Loss:** cross-entropy or squared error — [[What is a loss function]], [[What is cross-entropy loss]].
3. **Backward:** gradients via backpropagation — [[What is backpropagation]].
4. **Update:** SGD with momentum or Adam — [[What is the difference between Adam and SGD]].
5. **Repeat,** with the learning rate scheduled, until validation stalls — [[What is early stopping]].

```python
for epoch in range(epochs):
    for xb, yb in train_loader:
        optimizer.zero_grad()
        loss = criterion(model(xb), yb)   # forward + loss
        loss.backward()                    # gradients for every weight
        optimizer.step()                   # one downhill step
    if val_metric_stalled():
        break                              # early stopping
```

**Listing 1.** The whole learning loop in eight lines; everything else — schedules, regularization, normalization — refines these four operations.

## What "learning" actually produced

The weights now encode a feature hierarchy: early layers detect primitives, deeper layers compositions — measurable via representations transferable across tasks: [[What is transfer learning]]. Whether the network learned the pattern or memorized the sample is decided by held-out data: [[What is overfitting]], [[What is a train validation test split]]. The optimization is non-convex — multiple minima, saddle points — yet in practice over-parameterized networks find solutions that generalize, a central empirical fact of deep learning.

> [!warning] Interview trap
> "The network learns by adjusting neurons that fired." Popular neuroscience-flavored fiction — no selective reinforcement of active neurons happens; **every** parameter receives a gradient every step, including weights of silent units. Second trap: "loss going down means learning" — training loss falling while validation rises is memorization, not learning: [[What is overfitting]].

> [!tip] Interview answer
> The network learns by gradient descent: predict on a mini-batch, score with a loss, backpropagate the gradients, update weights a learning-rate-sized step, repeat. The mechanism is plain calculus on a composition of nonlinear layers; the magic is that this finds generalizing solutions at scale. I would stress that generalization — not falling training loss — defines learning, and that validation discipline is what separates the two.

