<!--
reps: 0
priority: 0
-->
#MachineLearning/Optimization #SRS

# What is gradient descent

> [!abstract] Short answer
> Gradient descent minimizes a loss by **iterating `θ ← θ − η·∇L(θ)`**: compute the gradient of the loss with respect to the parameters, step a small learning rate η against it, repeat. It is the engine under almost all ML training — the variants (SGD, momentum, Adam) differ only in how the step is shaped.

Intuition: the gradient points uphill; stepping against it descends. Convergence depends on η: too large overshoots and oscillates or diverges; too small crawls; learning-rate schedules (decay, warmup, cosine) manage the trajectory over time. For convex problems it converges to the global minimum; neural-network losses are non-convex — practice shows the found minima usually generalize anyway: [[How does a neural network learn]].

## The three evaluation regimes

* **Batch (full) gradient descent:** one step per pass over the whole dataset — accurate gradient, glacial progress, memory-heavy.
* **Stochastic (per-sample):** one step per row — noisy but fast; the noise itself has a regularizing effect.
* **Mini-batch:** the modern compromise — steps on chunks of 32–10k rows, GPU-friendly: [[What is the difference between batch SGD and mini-batch gradient descent]].

```python
for epoch in range(epochs):
    for xb, yb in loader:                 # mini-batches
        optimizer.zero_grad()
        loss = criterion(model(xb), yb)
        loss.backward()                   # gradient of this batch
        optimizer.step()                  # theta -= eta * grad
```

**Listing 1.** The loop is gradient descent regardless of the optimizer inside; momentum and Adam reshape the step, the skeleton stays.

## What makes it work in deep learning

The chain rule supplies gradients via backpropagation: [[What is backpropagation]]. Plain descent is rarely enough: **momentum** accumulates velocity through ravines; **Adam** adapts per-parameter step sizes from gradient moments — [[What is the difference between Adam and SGD]]; schedules and warmup manage η over training; initialization and normalization keep gradients usable in the first place: [[How does weight initialization affect training]], [[What is batch normalization]]. The step size story is the practical core: everything else in this stack exists to let η stay large enough to make progress.

> [!warning] Interview trap
> "Gradient descent finds the global minimum." Only in convex landscapes; in neural nets it finds a basin — and the bias-variance reality is that which basin and how it generalizes depend on init, batch noise, and regularization: [[What is overfitting]]. Second trap: "bigger batches are strictly better" — large batches reduce gradient noise and often generalization with it; the LR must scale accordingly, and the optimum is empirical.

> [!tip] Interview answer
> Gradient descent repeats: compute the loss gradient, step against it with learning rate η. Mini-batch versions trade gradient accuracy for GPU throughput, momentum and Adam reshape the step, and schedules manage η over time. I would note convergence is global only in convex settings, that in deep nets the found basins usually generalize, and that learning-rate management is the single most impactful knob in practice.

