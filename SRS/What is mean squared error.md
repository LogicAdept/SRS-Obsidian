<!--
reps: 0
priority: 0
-->
#MachineLearning/Metrics #SRS

# What is mean squared error

> [!abstract] Short answer
> Mean squared error is the **average of squared prediction errors**: `MSE = (1/n) Σ (yᵢ − ŷᵢ)²`. It is the default regression loss and a standard regression metric — smooth, differentiable, and brutally punitive toward large mistakes, because squaring makes a 10-unit miss cost as much as a hundred 1-unit misses.

Squaring does three things at once: it removes the sign, it makes the function differentiable everywhere, and it weights big errors disproportionately. The last property is a feature and a bug — a feature when large misses are genuinely more costly, a bug when outliers are data noise rather than signal.

## MSE, RMSE, MAE

RMSE is the square root of MSE, restoring the units of the target so the number is speakable ("off by 4.2 days on average"). MAE uses absolute differences instead: linear in error, so it is outlier-tolerant and targets the median rather than the mean. The trade-offs among the family members, plus R², are collected in [[What regression metrics do you use in machine learning]]; the loss-function perspective is in [[What is a loss function]].

```python
import numpy as np

def mse(y_true, y_pred):
    return float(np.mean((np.asarray(y_true) - np.asarray(y_pred)) ** 2))

# sklearn equivalent:
from sklearn.metrics import mean_squared_error
# mean_squared_error(y_te, pred)          # squared units
# mean_squared_error(y_te, pred, squared=False)  # RMSE
```

**Listing 1.** MSE in one line; the sklearn variant with `squared=False` gives RMSE in original units.

## Where it is the right tool and where it lies

MSE is the right headline when large deviations are disproportionately expensive (inventory planning, energy load) and the target is not heavy-tailed. It lies when outliers are typos or one-off shocks — a handful of extreme points dominates the number while the model may be excellent on the 99% that matters; then MAE or Huber tells the truer story. For model comparison across different scales, standardized errors or R² avoid unit confusion. Training dynamics differ too: squared-error gradients shrink as errors shrink, which makes optimization gentle but slow near the optimum — contrast with [[What is cross-entropy loss]] for classification.

> [!warning] Interview trap
> "MSE is always the regression metric." With heavy-tailed or count targets, MSE mostly measures your outliers; and comparing MSE across targets with different units is meaningless. Also note the asymmetry trap: minimizing MSE yields predictions near the conditional **mean**, which is wrong if your business needs a high quantile — for that you need quantile/pinball loss, not a differently-scaled MSE.

> [!tip] Interview answer
> MSE averages squared errors — differentiable and outlier-amplifying — and RMSE is its square root in original units. I would say it is the natural regression loss when big misses are genuinely worse, switch the story to MAE or Huber when outliers are noise, and mention that MSE-optimal predictions estimate the conditional mean, which matters if the business actually needs quantiles.

