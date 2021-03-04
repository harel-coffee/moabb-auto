"""
===============================================
Motor Imagery CSP + LDA Classification (Part 2)
===============================================
We extend the previous example to a case where we want to analyze the score of
a classifier with three different MI datasets instead of just one. As before,
we begin by importing all relevant libraries.
"""
# Authors: Pedro L. C. Rodrigues, Sylvain Chevallier
#
# https://github.com/plcrodrigues/Workshop-MOABB-BCI-Graz-2019

import os
import warnings

import matplotlib.pyplot as plt
import mne
import pandas as pd
import seaborn as sns
from mne.decoding import CSP
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.pipeline import make_pipeline

import moabb
from moabb.datasets import BNCI2014001, Weibo2014, Zhou2016
from moabb.evaluations import WithinSessionEvaluation
from moabb.paradigms import LeftRightImagery


moabb.set_log_level('info')
mne.set_log_level('CRITICAL')
warnings.filterwarnings('ignore')


##############################################################################
# Initializing Datasets
# ---------------------
#
# We instantiate the three different datasets that follow the MI paradigm
# (with left-hand/right-hand classes) but were recorded with different number
# of electrodes, different number of trials, etc.

datasets = [Zhou2016(), Weibo2014(), BNCI2014001()]

# The following lines go exactly as in the previous example, where we end up
# obtaining a pandas dataframe containing the results of the evaluation. We
# set `overwrite` to False to cache the results, avoiding to restart all the
# evaluation from scratch if a problem occurs.
paradigm = LeftRightImagery()
evaluation = WithinSessionEvaluation(paradigm=paradigm, datasets=datasets,
                                     overwrite=False)
pipeline = make_pipeline(CSP(n_components=8), LDA())
results = evaluation.process({"csp+lda": pipeline})

# To export the results in CSV within a directory:
if not os.path.exists("./results"):
    os.mkdir("./results")
results.to_csv("./results/results_part2-2.csv")

# To load previously obtained results saved in CSV
results = pd.read_csv("./results/results_part2-2.csv")

##############################################################################
# Plotting Results
# ----------------
#
# We plot the results using the seaborn library. Note how easy it
# is to plot the results from the three datasets with just one line.

results["subj"] = [str(resi).zfill(2) for resi in results["subject"]]
g = sns.catplot(kind='bar', x="score", y="subj", col="dataset",
                data=results, orient='h', palette='viridis')
plt.show()
