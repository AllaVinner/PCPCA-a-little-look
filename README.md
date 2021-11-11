# Project to seperate
## - A short look at the PCPCA dimension reduction tool

PCA is a great tool for dimension reduction, but there are situations where it dosen't quit do the trick. 
<img style="float: right;" src="./media/scattered_data.jpeg">
Withouth opening the can of worms that are named *non-linear*, we have the scenario where we want to distinguise two set of groups wehre the variance between the groups are orthogonal to the variance in the overall population (we will see what that means in a secound). The paper [] introduces a linear method called PCPCA which deals with just this case, and this is what this repository will investigate.

## The data
The group mentioned above can be any formed by any cathegorical field e.g. man vs woman, sick vs healthy, or control group vs case group; below I will refere to the groups as *case* and *control*. Then with had the thing about difference in variance. Actually it is not the difference in variance, but difference in the **direction** of the variances. Look at the data below. The overall variation of the data is along an axis going (roughfly) from the bottom left corner to the top right one, however, the difference between the two groups seem to be better explained by the other axis (from top left to bottom right).


<p align="center">
  <img src="./media/scattered_data.jpeg" width="500">
</p>


Performing a simple 


<p align="center">
  <img src="./media/rotating_projection.gif" width="1000">
</p>




# [Probabilistic contrastive principal component analysis](https://arxiv.org/abs/2012.07977)
[![Build Status](https://travis-ci.com/andrewcharlesjones/pcpca.svg?branch=main)](https://travis-ci.com/github/andrewcharlesjones/pcpca)

This repo contains models and algorithms for probabilistic contrastive principal component analysis (PCPCA). Given a foreground dataset and a backround dataset, PCPCA is designed to find structure and variation that is enriched in the foreground relative to the background.

The accompanying paper can be found here: https://arxiv.org/abs/2012.07977.

## Installation

PCPCA can be installed with pip:
```
pip install pcpca
```

You should then be able to import the model as follows:
```python
from pcpca import PCPCA
```
## Example

Here's a simple example of fitting PCPCA with a toy dataset. In this data, the foreground contains two subgroups. The first half of the foreground samples belong to group 1, and the second half belong to group 2.

Load the toy dataset and plot it:
```python
import pandas as pd
import matplotlib.pyplot as plt

# Load
X = pd.read_csv("./data/toy/foreground.csv", header=None).values
Y = pd.read_csv("./data/toy/background.csv", header=None).values

# Should have same number of features
assert X.shape[0] == Y.shape[0]

p, n = X.shape
m = Y.shape[1]

# Plot
plt.scatter(X[0, :n//2], X[1, :n//2], alpha=0.5, label="Foreground group 1", s=80, color="green")
plt.scatter(X[0, n//2:], X[1, n//2:], alpha=0.5, label="Foreground group 2", s=80, color="orange")
plt.scatter(Y[0, :], Y[1, :], alpha=0.5, label="Background", s=80, color="gray")
plt.legend()
plt.xlim([-7, 7])
plt.ylim([-7, 7])
plt.show()
```

<p align="center">
  <img src="./example/toydata.png" width="500">
</p>

Now we'll instantiate and fit the model with maximum likelihood estimation.

```python
from pcpca import PCPCA
pcpca = PCPCA(gamma=0.7, n_components=1)
pcpca.fit(X, Y)
```

We can then visualize the line defined by W. (In general, this will be a hyperplane, but here we set n_components=1 for simplicity.)

```python
import numpy as np
def abline(slope, intercept):
    """Plot a line from slope and intercept"""
    axes = plt.gca()
    x_vals = np.array(axes.get_xlim())
    y_vals = intercept + slope * x_vals
    plt.plot(x_vals, y_vals, '--')

# Re-plot data
plt.scatter(X[0, :n//2], X[1, :n//2], alpha=0.5, label="Foreground group 1", s=80, color="green")
plt.scatter(X[0, n//2:], X[1, n//2:], alpha=0.5, label="Foreground group 2", s=80, color="orange")
plt.scatter(Y[0, :], Y[1, :], alpha=0.5, label="Background", s=80, color="gray")
plt.legend()
plt.xlim([-7, 7])
plt.ylim([-7, 7])

# Plot line defined by W
origin = np.array([[0], [0]])  # origin point
abline(slope=pcpca.W_mle[1, 0] / pcpca.W_mle[0, 0], intercept=0)
plt.show()
```

We can see that W finds the axis that splits the two foreground groups:

<p align="center">
  <img src="./example/toydata_W.png" width="500">
</p>

Once the model is fit, samples can be projected onto the components by calling `transform`:

```python
X_reduced, Y_reduced = pcpca.transform(X, Y)
```

Or both of these steps can be done with one call to `fit_transform`:

```python
X_reduced, Y_reduced = pcpca.fit_transform(X, Y)
```
