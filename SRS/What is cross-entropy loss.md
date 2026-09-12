<!--
reps: 0
priority: 0
-->
#MachineLearning/Optimization #SRS

# What is cross-entropy loss

> [!abstract] Short answer
> Cross-entropy measures the **distance between the predicted distribution and the true label**: for binary, `−[y·log p + (1−y)·log(1−p)]`; for multiclass, `−log p_true` after softmax. It punishes confident wrong answers asymptotically hard (log of ~0 → ∞) while barely penalizing confident correct ones — which is exactly the gradient signal classification training wants.

It is the maximum-likelihood objective in disguise: minimizing cross-entropy maximizes the log-likelihood of the true labels under the model's predicted distribution. That statistical grounding — not convention — is why it is the classification default: the loss corresponds to a probabilistic model of the data: [[What is a loss function]].

## Mechanics and the softmax partnership

```python
import torch, torch.nn as nn

head = nn.Linear(256, 10)                 # raw logits
loss_fn = nn.CrossEntropyLoss()           # = log_softmax + NLL, fused
logits = head(features)
loss = loss_fn(logits, targets)           # targets: class indices, no softmax
```

**Listing 1.** The fused contract: pass **logits**, never softmaxed outputs — the loss applies log-softmax internally; double softmax is the classic bug: [[What is softmax]].

```text
p=0.99, y=1 -> loss 0.01      confident and right: almost free
p=0.51, y=1 -> loss 0.67      right but unsure: noticeable cost
p=0.01, y=1 -> loss 4.6       confident and wrong: heavy cost
```

**Listing 2.** The asymmetric punishment profile — log-scale cost explodes as confident-wrong approaches certainty.

## Properties worth knowing

* **Calibration pressure:** cross-entropy pushes toward calibrated probabilities (it is a proper scoring rule), though real networks still miscalibrate under shift — temperature scaling at eval time is the usual patch: [[What is softmax]].
* **Imbalance handling:** plain CE under-weights the minority; weighted CE (per-class weights), focal loss (down-weight easy examples), and label smoothing (soft targets against overconfidence) are the standard variants: [[How do you handle class imbalance]].
* **MSE is wrong for classification:** with sigmoid/softmax outputs, squared error saturates gradients exactly when the model is confidently wrong — CE's log-derivative keeps gradients alive: [[What is the difference between linear regression and logistic regression]].
* **In LLMs:** next-token training is cross-entropy over the vocabulary at every position — the loss behind [[What is an LLM and what is a context window]].

> [!warning] Interview trap
> "Cross-entropy and log loss are different things." They are the same objective — binary cross-entropy on two classes, categorical over many; naming differs, math does not. Second trap: passing softmaxed probabilities into `CrossEntropyLoss` — it applies log-softmax again, squashing gradients and silently degrading training; frameworks expect raw logits.

> [!tip] Interview answer
> Cross-entropy is the negative log-likelihood of the true class under the predicted distribution — binary as log loss, multiclass as minus log of the softmaxed true-class probability. It punishes confident errors explosively and confident correctness almost not at all, which yields healthy gradients; it expects raw logits in modern frameworks, has weighted, focal, and label-smoothed variants for imbalance and overconfidence, and it is literally the training objective of next-token LLMs.

