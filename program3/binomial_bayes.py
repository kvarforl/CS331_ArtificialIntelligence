#!/usr/bin/env python3
import numpy as np
import pandas as pd
from string import punctuation

#function takes in a space delimited string and returns a cleaned list of words
def clean_text(review):
    translator = str.maketrans('','',punctuation)
    return str(review).translate(translator).lower().split()

def load_data():
    train = np.array(pd.read_csv("trainingSet.txt",sep="\t"))
    test = np.array(pd.read_csv("testSet.txt",sep="\t"))
    trainX, trainy = train.T
    vocab = np.unique(np.array(clean_text(trainX)))
    trainX = np.array([clean_text(x) for x in trainX])
    testX = np.array([clean_text(x) for x in test])
    #trainX and testX are now a jagged array of cleaned examples
    return (trainX, trainy), testX, vocab
    
  
train, test, vocabulary = load_data()
trainX, trainY = train
print()