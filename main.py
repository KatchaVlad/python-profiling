import numpy as np
from profilers.gini import gini
from profilers.profiler import profileit, line_profileit
import pandas as pd

""" Profiling through decorators
@profileit
def python-profiling(arr):
    ret = gaussian_fit(arr, n_gauss=3, return_plot=False)
    return ret
"""

x = np.concatenate((np.random.normal(10, 5, 100), np.random.normal(50, 20, 100)))
x -= np.min(x)
x /= np.max(x)

ret = profileit(gini,n_run=1000)(x)
ret = line_profileit(gini)(x)

# Analyse
df = pd.read_csv("profiling_files/gini_line_profile.csv", sep=';', index_col='Line #')

df = pd.read_csv("profiling_files/gini_profile.csv", sep=';')
df.sort_values(by='tottime', inplace=True, ascending=False)

