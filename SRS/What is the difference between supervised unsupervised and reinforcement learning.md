<!--
reps: 0
priority: 0
-->
#MachineLearning/Supervised #MachineLearning/Unsupervised #MachineLearning/Reinforcement #SRS

# What is the difference between supervised unsupervised and reinforcement learning

> [!abstract] Short answer
> The three paradigms differ in **what feedback the algorithm gets**. Supervised: the right answer `y` for every input. Unsupervised: no answers, only inputs — find structure. Reinforcement: no answers per step, only a **delayed reward** signal for a sequence of actions taken by an agent. The feedback type determines the loss, the algorithms, and the evaluation.

Everything else — neural networks, trees, regularization — is shared machinery; the paradigm is about the learning signal. That is why the first question about any ML problem is "what feedback do we actually have?"

## Side by side

```text
supervised     : (x, y) pairs          -> learn f: x -> y     loss vs label
unsupervised   : x only               -> find structure       intrinsic objective
reinforcement  : state, action, reward -> learn policy        maximize return
```

**Listing 1.** The learning signal is the dividing line: labels, nothing, or delayed reward.

* **Supervised** needs labeled data and gives the most direct optimization — classification and regression: [[What is supervised learning]].
* **Unsupervised** trades labels for exploratory objectives — clustering, dimensionality reduction: [[What is unsupervised learning]]; also the engine of self-supervised pretraining.
* **Reinforcement** handles sequential decision-making where credit for a win must be assigned back to earlier moves. An agent balances exploration against exploitation, and the reward is often delayed and noisy. Q-learning and policy-gradient methods are the classics; AlphaGo and game-playing agents are the canonical demos. The gap to supervised is the absence of a teacher: the environment only scores, it does not show the best action.

```d2
direction: right
s: "Signal?" { width: 130; height: 70 }
sup: "Labels (x, y)\n-> supervised\nloss vs y" { width: 210; height: 90 }
uns: "No labels\n-> unsupervised\nfind structure" { width: 200; height: 90 }
rl: "Delayed reward\n-> reinforcement\nlearn policy" { width: 210; height: 90 }
s -> sup: "per-example answer" { }
s -> uns: "nothing" { }
s -> rl: "scores after actions" { }
```

**Fig. 1.** One question — what feedback exists — routes the problem into the right paradigm.

> [!warning] Interview trap
> "RL is better because it is more human-like." For a static prediction problem with labels, supervised learning is strictly more sample-efficient — do not reach for RL where a loss would do. The reverse trap: calling self-supervised pretraining "unsupervised, so no data labeling is needed" — labels are manufactured from the data itself, and the objective is still supervised-style prediction.

> [!tip] Interview answer
> The paradigms differ by feedback: labeled answers for supervised, none for unsupervised, delayed reward for reinforcement. I would say supervised covers prediction problems with labels, unsupervised covers structure discovery, and reinforcement covers sequential decision-making where actions change the environment and credit is delayed. In practice most business ML is supervised, and the paradigms combine — self-supervised pretraining plus supervised fine-tuning being the dominant modern recipe.

