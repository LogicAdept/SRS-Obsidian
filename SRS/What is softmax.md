<!--
reps: 0
priority: 0
-->
#MachineLearning/DeepLearning #SRS

# What is softmax

> [!abstract] Short answer
> Softmax converts a vector of raw scores (logits) into a **probability distribution**: exponentiate each score and normalize by the sum — `softmax(z)ᵢ = e^{zᵢ} / Σⱼ e^{zⱼ}`. Outputs are positive and sum to one, which is why it is the standard output head for multiclass classification and the weighting function inside attention.

Exponentiation is order-preserving and amplifies differences: the largest logit takes a disproportionate share of the probability mass. Temperature controls that sharpening — dividing logits by T > 1 flattens, T < 1 sharpens — the same knob reused at LLM generation time: [[What is temperature in an LLM]].

## Numerical stability — the interview detail

`e^{1000}` overflows. The standard trick subtracts the max before exponentiating: `softmax(z) = softmax(z − max(z))`, mathematically identical, numerically safe. Frameworks do it internally (`torch.softmax`, `scipy.special.softmax`); a from-scratch implementation missing the shift is a classic bug and a favorite interview probe. For binary cases softmax reduces to the sigmoid on the logit difference: [[What is the difference between linear regression and logistic regression]].

```python
import numpy as np

def softmax(z):
    z = z - z.max(axis=-1, keepdims=True)   # stability shift
    e = np.exp(z)
    return e / e.sum(axis=-1, keepdims=True)

logits = np.array([2.0, 1.0, 0.1])
print(softmax(logits))            # ~ [0.659, 0.242, 0.099]
```

**Listing 1.** Stable softmax in five lines: the max-subtraction changes nothing mathematically and prevents overflow.

## Where it appears

* **Output head:** multiclass classifiers output logits; the loss applies softmax internally (`CrossEntropyLoss` = log-softmax + NLL) — applying it twice is a real bug, see [[What is cross-entropy loss]].
* **Attention:** attention weights are softmax over compatibility scores — a distribution over "where to look": [[What is self-attention]]; multi-head variants re-use it per head: [[What is multi-head attention]].
* **Policy outputs** in reinforcement learning; **mixture weights** in mixture-of-experts.

```d2
direction: right
logits: "logits\n[2.0, 1.0, 0.1]" { width: 160; height: 70 }
exp: "exp(z)\n[7.39, 2.72, 1.11]" { width: 170; height: 70 }
norm: "normalize by sum\n[0.66, 0.24, 0.10]" { width: 200; height: 70 }
logits -> exp -> norm
```

**Fig. 1.** Exponentiate, then normalize: raw scores become a valid distribution whose mass concentrates on the top score.

> [!warning] Interview trap
> "Softmax outputs are true calibrated probabilities." They are normalized exponentials of scores — confident and often miscalibrated; treating 0.999 as a real 99.9% chance without calibration is a production mistake. Second trap: stacking an explicit softmax before a softmax-based loss — double application squashes gradients and silently degrades training.

> [!tip] Interview answer
> Softmax exponentiates logits and normalizes them into a probability distribution — the standard multiclass output and the weighting function in attention. The two details worth saying out loud are the max-subtraction for numerical stability and that softmax probabilities are not calibrated; training losses consume raw logits, and temperature tuning happens at generation time.

