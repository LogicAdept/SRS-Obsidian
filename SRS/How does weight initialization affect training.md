<!--
reps: 0
priority: 0
-->
#MachineLearning/DeepLearning #SRS

# How does weight initialization affect training

> [!abstract] Short answer
> Initialization sets the **variance of activations and gradients at step zero**: too small and the signal dies before reaching the output (vanishing), too large and it saturates or explodes. Variance-preserving schemes — Xavier/Glorot for sigmoid/tanh, Kaiming/He for ReLU — keep activation and gradient variance roughly constant across layers, which decides whether deep nets train at all.

Zero initialization is the instructive failure: all neurons in a layer compute identically and receive identical gradients — symmetry is never broken and the layer stays degenerate. Small random values fix symmetry but shrink the signal multiplicatively through layers; large values saturate activations and blow up gradients — the step-zero version of [[What are vanishing and exploding gradients]].

## The variance math in one breath

For a layer with `n_in` inputs and weights of variance `Var(w)`, output variance scales by `n_in · Var(w)`. Xavier sets `Var(w) = 2/(n_in + n_out)` keeping variance stable for linear/tanh nets; Kaiming sets `Var(w) = 2/n_in` accounting for ReLU zeroing half the pre-activations. Frameworks default to these: PyTorch `nn.Linear` uses Kaiming-uniform with a=√5; you rarely override for standard layers, but custom layers and huge models need explicit care.

```python
import torch.nn as nn

def init_weights(m):
    if isinstance(m, nn.Linear):
        nn.init.kaiming_normal_(m.weight, nonlinearity="relu")
        nn.init.zeros_(m.bias)          # zero bias: symmetry broken by weights

model.apply(init_weights)
```

**Listing 1.** Explicit Kaiming initialization for a ReLU network; biases at zero are fine because random weights already break symmetry.

## Beyond the first step

Initialization interacts with everything downstream: normalization layers re-standardize activations and relax the constraints — [[What is batch normalization]]; residual architectures scale the last layer of each block (zero-init on the residual branch is a known stabilizer); very deep nets may use orthogonal or scaled schemes. A poor init can still be survived with lower learning rates — at the cost of slower, worse optimization — and the learning-rate story lives in [[What is the difference between Adam and SGD]] and [[What is gradient descent]]. Transfer learning is the extreme case of good initialization: pretrained weights: [[What is transfer learning]].

> [!warning] Interview trap
> "Initialization does not matter much — Adam fixes everything." The optimizer cannot resurrect a network whose forward signal saturated at layer two; early training dynamics are set by init. Second trap: initializing biases with large values "to be safe" — biases do not break symmetry, weights do; large biases just move activations into saturation.

> [!tip] Interview answer
> Initialization controls activation and gradient variance at the start of training: zero or tiny weights freeze the network via symmetry or vanishing signal, large ones saturate and explode it. Xavier keeps variance stable for tanh-type nets, Kaiming for ReLU by compensating the zeroed half. I would add that normalization and residuals relax but do not remove the issue, and that pretrained weights are initialization taken to its best case.

