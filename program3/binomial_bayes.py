#!/usr/bin/env python3
import numpy as np
import pandas as pd
from string import punctuation

#function takes in a space delimited string and returns a cleaned list of words
#presently does not omit numbers (but it easily could)
def clean_text(review):
    translator = str.maketrans('','',punctuation)
    return np.array(str(review).translate(translator).lower().split())

def load_data():
    train = np.array(pd.read_csv("trainingSet.txt",sep="\t"))
    test = np.array(pd.read_csv("testSet.txt",sep="\t"))
    trainX, trainy = train.T
    vocab = np.unique(clean_text(trainX))
    t = [clean_text(x) for x in trainX]
    trainX = np.array(t)
    t = [clean_text(x) for x in test]
    testX = np.array(t)
    #trainX and testX are now a jagged array of cleaned examples
    return (trainX, trainy), testX, vocab
    
def bag_words(data, vocab):
    num_examples = data.shape[0]
    num_features = vocab.shape[0]
    #make zero matrix with numex rows and numft columns
    matrix = np.zeros((num_examples, num_features))
    for row_ind in range(num_examples): #for each review
        for row_word in data[row_ind]:
            #match vocab indexes for each word in review, and set to 1
            matrix[row_ind][np.where(row_word==vocab)]=1
    return matrix
  
train, test, vocabulary = load_data()
trainX, trainY = train
train_bow = bag_words(trainX, vocabulary)
test_bow = bag_words(test, vocabulary)


print()
