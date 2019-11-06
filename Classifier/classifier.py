import time

start = time.time()

import argparse
import cv2
import os
import pickle
import sys

from operator import itemgetter
import numpy as np
np.set_printoptions(precision=2)
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV
from sklearn import mixture
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn import preprocessing

def train(workDir,classifier,ldaDim=-1):
    print("[ClASSIFER]Loading embeddings.")
    fname = "{}/labels.csv".format(workDir)
    labels = pd.read_csv(fname, header=None).as_matrix()[:, 1]
    labels = map(itemgetter(1),map(os.path.split,map(os.path.dirname, labels)))
    
    labels=list(labels)
    fname = "{}/reps.csv".format(workDir)
    embeddings = pd.read_csv(fname, header=None).as_matrix()
    
    le = preprocessing.LabelEncoder().fit(labels)
    labelsNum = le.transform(labels)
    print("[ClASSIFER]labelsNum",labelsNum,type(labelsNum))

    nClasses = len(le.classes_)
    print("[ClASSIFER]Training for {} classes.".format(nClasses))

    if classifier == 'LinearSvm':
        clf = SVC(C=1, kernel='linear', probability=True)
    elif classifier == 'GridSearchSvm':
        param_grid = [
            {'C': [1, 10, 100, 1000],
             'kernel': ['linear']},
            {'C': [1, 10, 100, 1000],
             'gamma': [0.001, 0.0001],
             'kernel': ['rbf']}
        ]
        clf = GridSearchCV(SVC(C=1, probability=True), param_grid, cv=5)
    
    elif classifier == 'GMM':
        clf = mixture.GMM(n_components=nClasses)

    elif classifier == 'RadialSvm': 
        clf = SVC(C=1, kernel='rbf', probability=True, gamma=2)
    
    elif classifier == 'DecisionTree': 
        clf = DecisionTreeClassifier(max_depth=20)

    elif classifier == 'GaussianNB':
        clf = GaussianNB()

    elif classifier == 'DBN':
        from nolearn.dbn import DBN
        clf = DBN([embeddings.shape[1], 500, labelsNum[-1:][0] + 1], learn_rates=0.3,learn_rate_decays=0.9,epochs=300,verbose=1)

    if ldaDim > 0:
        clf_final = clf
        clf = Pipeline([('lda', LDA(n_components=ldaDim)),
                        ('clf', clf_final)])
    
    print("[CLASSIFER]labelsNum",labelsNum)
    clf.fit(embeddings, labelsNum)
    print(type(clf),type(le))
    fName = "{}/classifier.pkl".format(workDir)
    print("[CLASSIFER]Saving classifier to '{}'".format(fName))
    print(type(le),type(clf))
    with open(fName, 'wb+') as f:
        pickle.dump((le, clf), f)