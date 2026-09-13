<!--
reps: 0
priority: 0
-->
#MachineLearning #SRS

# What is a model in machine learning

> [!abstract] Short answer
> A model is a **parameterized function plus the fitted parameter values**: the architecture says what the function computes in terms of parameters, training fixes the parameters, and inference just evaluates the frozen function on new inputs. A model is the artifact you serialize, version, deploy, and monitor.

Concretely: "logistic regression" is a family; "the 4 MB pickle of a logistic regression with coefficients θ̂ fitted on the March data" is a model. The distinction is not pedantic — version confusion between model family, fitted weights, and training data is a routine source of production incidents.

## Anatomy

* **Structure** `f(x; θ)` — linear combination, tree of splits, layered neural network. This is a human design decision.
* **Parameters** `θ` — numbers fitted from data by optimizing a loss; see [[What is a model parameter]].
* **Hyperparameters** — knobs you set before training (depth, learning rate, `k`); they shape the search, not the fitted values: [[What is a model hyperparameter]].
* **Training state** — optimizer state, preprocessing statistics, label encoders. A deployable model includes these; a bare weights file without the fitted `StandardScaler` is a broken deployment.

```d2
direction: right
data: "Training data" { width: 150; height: 70 }
family: "Model family\nf(x; theta)" { width: 160; height: 80 }
fit: "Training\noptimize theta" { width: 140; height: 70 }
model: "Fitted model\nf(x; theta-hat)" { width: 170; height: 80 }
serve: "Inference\nfrozen function" { width: 150; height: 70 }
data -> family -> fit -> model -> serve
```

**Fig. 1.** The family becomes a model only after fitting; serving uses the frozen result, never the learner.

## Same word, three meanings

Practitioners say "model" for the family ("tree models overfit"), the fitted artifact ("the model predicts 0.9"), and sometimes the whole serving unit. Interviews and code reviews benefit from being explicit: family, fitted weights, or serving package. In MLOps tooling the serving unit is what gets registered and versioned — that is the level [[What is MLOps]] operates on.

> [!warning] Interview trap
> "The model is the algorithm." Sloppy and wrong in practice: an algorithm (e.g. gradient boosting) is the procedure that produces the model; the model is the result you serve. Two teams can use the same algorithm and produce wildly different models because their data, hyperparameters, or preprocessing differ. When someone reports "the model is 95% accurate", always ask which artifact on which split.

> [!tip] Interview answer
> A model is a parameterized function with fitted parameters — architecture plus weights plus the preprocessing state needed to run it. I would stress the difference between the model family chosen by a human, the parameters fitted from data, and the hyperparameters set before training, and that in production the model is a versioned artifact that includes preprocessing, not just the weights.

