<!--
reps: 0
priority: 0
-->
#MachineLearning/DeepLearning #SRS

# What are vanishing and exploding gradients

> [!abstract] Short answer
> In backpropagation, gradients pass through **a product of many layer Jacobians**. If those factors are consistently smaller than one, the product collapses toward zero — vanishing gradients: early layers train at a standstill. If factors exceed one, the product blows up — exploding gradients: updates oscillate or produce NaNs. Deep or recurrent networks are exposed by construction.

## Vanishing: where it comes from

Saturating activations are the classic source: sigmoid's derivative peaks at 0.25, so ten sigmoid layers multiply derivatives ≤ 0.25¹⁰ — the earliest layers receive almost no signal. ReLU-family activations, careful initialization that keeps variance stable across layers: [[How does weight initialization affect training]], and normalization layers that re-center activations: [[What is batch normalization]] are the standard defenses. Architectural shortcuts are the strongest fix — residual connections give gradients a highway that skips the multiplicative chain: [[What is backpropagation]] dynamics; gated recurrence fixes the RNN version: [[What is an LSTM]].

## Exploding: where it comes from and how it is tamed

Large weights, long unrolled RNNs, and ill-conditioned loss surfaces produce factor products exceeding one. The pragmatic fixes: **gradient clipping** (cap the global norm — standard in RNN and LLM training), lower learning rates, weight decay, and normalization. Clipping does not solve the underlying ill-conditioning; it makes training survivable.

```python
import torch

loss.backward()
torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
optimizer.step(); optimizer.zero_grad()
```

**Listing 1.** Global-norm gradient clipping — the one-line insurance policy in recurrent and large-model training.

```d2
direction: down
l1: "layer 1" { width: 130; height: 60 }
l2: "layer 2" { width: 130; height: 60 }
l3: "layer 3  ...  layer N" { width: 210; height: 60 }
grad: "gradient = product of\nlayer Jacobians" { width: 240; height: 80 }
small: "factors < 1 -> vanishing\near layers frozen" { width: 260; height: 80 }
big: "factors > 1 -> exploding\nNaN updates" { width: 200; height: 80 }
l1 -> l2 -> l3 -> grad
grad -> small; grad -> big
```

**Fig. 1.** Backward signal is a Jacobian product: each factor under unity shrinks it, each above unity amplifies it.

> [!warning] Interview trap
> "Vanishing gradients mean the model cannot learn at all." Usually it means the **early layers** learn while the network effectively behaves as a shallow, partially random feature extractor — training loss still improves, hiding the pathology. Also, exploding gradients are not only an RNN issue: large-batch LLM training hits loss spikes handled with clipping and careful LR schedules.

> [!tip] Interview answer
> Both pathologies come from multiplying many layer Jacobians in backprop: factors below one shrink the signal until early layers stall, factors above one blow it up. The fixes map one-to-one: non-saturating activations, variance-preserving initialization, normalization, and residual or gated architectures for vanishing; gradient clipping and LR control for exploding. I would mention that residuals are what made very deep nets trainable at all.

