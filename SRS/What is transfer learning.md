<!--
reps: 0
priority: 0
-->
#MachineLearning/DeepLearning #SRS

# What is transfer learning

> [!abstract] Short answer
> Transfer learning reuses a model **trained on one task as the starting point for another**: take pretrained weights, replace the task head, and fine-tune on your (usually small) dataset. The early layers' generic features — edges, textures, word and code patterns — transfer; only the task-specific tail needs your data. It is the default recipe whenever labeled data is scarce.

Why it works: deep networks learn a feature hierarchy where early layers are broadly useful and late layers are task-shaped — [[How does a neural network learn]]. Pretraining on a huge corpus (ImageNet for vision, web text for language) bakes the generic half in; your small dataset only has to teach the top.

## The three modes

* **Feature extraction:** freeze the backbone, train only the new head. Cheapest, safest with tiny data — the backbone is a fixed feature extractor.
* **Full fine-tuning:** unfreeze everything with a small learning rate (often lower for the backbone). Best quality when you have enough data; risk of catastrophic forgetting and overfitting: [[What is overfitting]].
* **Parameter-efficient fine-tuning:** freeze the backbone, train small adapters or low-rank updates — LoRA is the LLM standard: [[What is LoRA]].

```python
import torch.nn as nn
from torchvision import models

net = models.resnet50(weights="IMAGENET1K_V2")   # pretrained backbone
for p in net.parameters():                        # mode 1: freeze
    p.requires_grad = False
net.fc = nn.Linear(net.fc.in_features, 5)         # new head for 5 classes
# train net.fc first; optionally unfreeze later layers with a lower LR
```

**Listing 1.** The canonical vision recipe: pretrained ResNet, frozen body, new head; progressive unfreezing if data allows.

## When it does not pay

Huge domains gap (medical images to satellite tiles is usually fine; images to tabular is not a thing), very large in-domain datasets (pretraining yourself or training from scratch can win), and strict latency/size budgets where a compact model trained from scratch beats a giant fine-tuned one. The same logic scales up to LLMs: prompting and RAG are zero-training transfer, fine-tuning is the heavy end — [[When do you fine-tune versus use RAG versus prompting]].

> [!warning] Interview trap
> "Transfer learning always beats from scratch." With millions of in-domain labeled examples or a badly mismatched pretraining domain, from-scratch can win — and tiny-data fine-tuning of a huge backbone can still overfit through the head's confidence. Second trap: fine-tuning with the backbone learning rate — the pretrained body needs gentler updates than the random head; one LR for all is a classic quality leak.

> [!tip] Interview answer
> Transfer learning initializes a new task from pretrained weights, because generic early-layer features transfer while the task head does not. I would name the spectrum — frozen feature extraction, full fine-tuning with per-group learning rates, parameter-efficient adapters — and say it is the default whenever labeled data is limited, with domain gap and data volume as the deciding checks.

