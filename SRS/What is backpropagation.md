<!--
reps: 0
priority: 0
-->
#MachineLearning/DeepLearning #SRS

# What is backpropagation

> [!abstract] Short answer
> Backpropagation is the **algorithm that computes the gradient of the loss with respect to every parameter**: it runs the network forward to get the loss, then applies the chain rule backward through the computation graph, reusing intermediate results so the whole gradient costs roughly the same as one forward pass. It is not a learning method — it is the gradient factory that optimizers consume.

Two passes per step: forward stores each operation's inputs and outputs; backward walks the graph in reverse, multiplying local derivatives (Jacobian-vector products) and passing the result to predecessors. The dynamic-programming trick — reusing already-computed upstream gradients instead of recomputing them per parameter — is what makes the cost linear in network size rather than exponential in depth.

## Where it sits in a training step

```text
1. forward pass:   x -> layers -> loss
2. backward pass:  loss -> dLoss/d(param) for every parameter   [backprop]
3. optimizer step: param -= lr * grad   (SGD/Adam choose the update rule)
```

**Listing 1.** Backprop is step 2 only; the update rule is the optimizer's business: [[What is gradient descent]], [[What is the difference between Adam and SGD]].

```python
import torch

loss = criterion(model(x), y)   # forward: builds the computation graph
loss.backward()                 # backprop: fills p.grad for every parameter
optimizer.step()                # optimizer consumes the gradients
optimizer.zero_grad()           # grads accumulate: must be zeroed explicitly
```

**Listing 2.** The autograd contract: `backward()` accumulates into `.grad` — forgetting `zero_grad()` is the classic silent training bug.

## What it costs and where it hurts

Backprop trades memory for speed: every intermediate needed by the backward pass is stored — training memory dwarfs inference, and activation checkpointing exists to recompute instead of store. The gradient it produces is exact for the given batch, but a **product across layers**: depth multiplies local derivatives, which is the root of vanishing/exploding gradients — [[What are vanishing and exploding gradients]] — and of the fixes: residuals, gating, normalization: [[What is batch normalization]]. In recurrent nets it unrolls through time (BPTT); in transformers it traverses attention: [[What is self-attention]].

> [!warning] Interview trap
> "Backpropagation is how the network learns." It only computes gradients — the learning rule is the optimizer plus loss plus data; calling SGD "backpropagation" conflates the factory with the factory's customer. Second trap: "backprop computes gradients in one pass per parameter" — no, one shared backward sweep serves all parameters simultaneously; that reuse is the entire point of the algorithm.

> [!tip] Interview answer
> Backpropagation computes loss gradients for all parameters by applying the chain rule backward over the computation graph, reusing intermediate results so the cost is comparable to a forward pass. I would separate it from the optimizer step, mention the memory cost of storing intermediates, and connect the multiplicative structure of the backward pass to vanishing gradients and the architectural fixes that made deep networks trainable.

