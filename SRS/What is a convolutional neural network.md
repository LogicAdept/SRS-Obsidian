<!--
reps: 0
priority: 0
-->
#MachineLearning/DeepLearning/CNN #SRS

# What is a convolutional neural network

> [!abstract] Short answer
> A CNN is a network built from **convolutional layers**: small learnable filters slide across the input and respond to local patterns, producing feature maps. Weight sharing plus locality give translation-tolerant pattern detection with drastically fewer parameters than dense layers — the architecture that made image recognition practical.

Each filter is a small grid of weights (e.g. 3×3×channels) applied at every position: the same detector everywhere in the image. Stacking layers builds a hierarchy — edges in layer one, motifs deeper, objects deeper still — with pooling or striding shrinking spatial size while channels grow.

## The three structural ideas

* **Local connectivity:** a neuron sees a small receptive field, not the whole image — matching the locality of visual structure.
* **Weight sharing:** one filter reused at all positions — parameters depend on filter size, not image size; a 3×3×64 conv over 224×224 images is under 200 weights per channel group instead of millions.
* **Pooling/striding:** downsample between stages, buying translation tolerance and enlarging the effective receptive field.

Output spatial size is `(W − K + 2P)/S + 1` for width `W`, kernel `K`, padding `P`, stride `S` — the arithmetic that interviews love and that padding exists to tame ("same" padding keeps size stable).

```python
import torch.nn as nn

cnn = nn.Sequential(
    nn.Conv2d(3, 32, kernel_size=3, padding=1),  # local + shared weights
    nn.BatchNorm2d(32), nn.ReLU(),
    nn.MaxPool2d(2),                              # downsample
    nn.Conv2d(32, 64, kernel_size=3, padding=1),
    nn.BatchNorm2d(64), nn.ReLU(),
    nn.AdaptiveAvgPool2d(1),                      # global pooling -> head
)
```

**Listing 1.** The conv–norm–ReLU–pool block repeated; today's variants (ResNet, EfficientNet) keep the pattern and add residuals: [[What is batch normalization]].

## Where convolutions win and lose

Win: images, video, audio spectrograms — data with strong local structure and stationarity. Lose: variable-length sequences with global dependencies (transformers took that: [[Why did transformers replace RNNs]]), and tabular data where no spatial structure exists. The receptive field grows with depth, so very long-range pixel dependencies need many layers or global operations — attention hybrids exist for exactly that.

> [!warning] Interview trap
> "CNNs are translation invariant." Strictly, convolution is **translation equivariant** (shift input, features shift), and only pooling plus global heads add partial invariance — the precise wording is a favorite probe. Second trap: "more filters always help" — capacity without depth or receptive-field planning wastes parameters; the receptive field arithmetic bounds what patterns a layer can even see.

> [!tip] Interview answer
> A CNN slides shared learnable filters over local windows, producing feature maps that stack into a hierarchy from edges to objects. The efficiency comes from locality and weight sharing; downsampling builds translation tolerance. I would give the output-size formula, note conv–norm–ReLU as the canonical block, and say CNNs dominate grid-structured data while transformers took sequential and global-context problems.

