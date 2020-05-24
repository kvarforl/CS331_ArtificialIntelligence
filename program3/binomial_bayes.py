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
    testX, testy = test.T
    vocab = np.unique(clean_text(trainX))
    t = [clean_text(x) for x in trainX]
    trainX = np.array(t)
    t = [clean_text(x) for x in testX]
    testX = np.array(t)
    #trainX and testX are now a jagged array of cleaned examples
    return (trainX, trainy), (testX, testy), vocab

#really just for assignment specifications; outputs comma delimited text file of preprocess results
def output_info(bow, labels, vocab, filename):
    with open(filename,"w") as fp:
        print(*vocab, "classlabel", sep=",", file=fp)
        n_examples = bow.shape[0]
        for ind in range(n_examples):
            if(labels != []):
                print(*bow[ind], labels[ind], sep=",", file=fp)
            else:
                print(*bow[ind], sep=",", file=fp)

#expects 1D np arrays of equal dimensions
def accuracy_score(preds, labels):
    correct = np.count_nonzero(preds==labels)
    return correct / labels.shape[0]

class BinomialBayesClassifier():

    def fit(self, trainX, trainY, vocab):
        self.vocab = vocab
        self.train_bow = self._bag_words(trainX)#only saved for access for assignment output
        self.pos_wordprobs, self.neg_wordprobs = self._p_words_given_class(self.train_bow, trainY)

    #takes in jagged np array of strings of examples
    def predict(self, X):
        self.test_bow = self._bag_words(X) #only saved for access for assignment output
        preds = [self._predict(x) for x in self.test_bow]
        return np.array(preds)

    #predict a single example
    def _predict(self, x):
        if self._p_class_given_x(x, "pos") > self._p_class_given_x(x,"neg"):
            return 1
        else:
            return 0

    #takes in a jagged np array of strings of examples and a vocabulary
    #returns a binomal bag of words (num examples rows, num words in vocab cols)    
    def _bag_words(self, data):
        num_examples = data.shape[0]
        num_features = self.vocab.shape[0]
        #make zero matrix with numex rows and numft columns
        matrix = np.zeros((num_examples, num_features), dtype="int8")
        for row_ind in range(num_examples): #for each review
            for row_word in data[row_ind]:
                #match vocab indexes for each word in review, and set to 1
                matrix[row_ind][np.where(row_word==self.vocab)]=1
        return matrix
        
    #function for training
    #takes training features BOW (X), training labels (Y), and optional uniform dirichlet prior value (default 1)
    #also sets self.ppos and self.pneg
    #returns 2 row vectors of probabilities - [p(w0|y=0), p(w1|y=0)...], [p(w0|y=1), p(w1|y=1)...]    
    def _p_words_given_class(self, X, y, alpha=1):
        class1_examples = X[y==1] #positive reviews
        class0_examples = X[y==0] #negative reviews
        num_c1, _ = class1_examples.shape
        num_c0, _ = class0_examples.shape
        self.ppos = num_c1 / (num_c1 + num_c0)
        self.pneg = 1 - self.ppos
        c1_numerator = np.sum(class1_examples, axis=0) + alpha #vector of word occurances in class 1 + alpha
        c0_numerator = np.sum(class0_examples, axis=0) + alpha # '' in class 0 
        return (c1_numerator/num_c1), (c0_numerator/num_c0)

    #helper function for _predict; calculates probability of example X being in class cl ("pos" or "neg")
    def _p_class_given_x(self, x, cl):
        if cl == "pos":
            return np.sum(x*np.log(self.pos_wordprobs)) + np.log(self.ppos)
        else:
            return np.sum(x*np.log(self.neg_wordprobs)) + np.log(self.pneg)

train, test, vocabulary = load_data()
trainX, trainY = train
testX, testY = test

classifier = BinomialBayesClassifier()

classifier.fit(trainX, trainY, vocabulary)

train_predictions = classifier.predict(trainX)
test_predictions = classifier.predict(testX)

train_accuracy = accuracy_score(train_predictions,trainY)
test_accuracy = accuracy_score(test_predictions, testY)

output_info(classifier.train_bow, trainY, vocabulary, "preprocessed_train.txt")
output_info(classifier.test_bow, testY, vocabulary, "preprocessed_test.txt")

with open("results.txt","w") as fp:
    print("Results from ./trainingSet.txt and ./testSet.txt:",file=fp)
    print("\tTrain Accuracy:", train_accuracy, file=fp)
    print("\tTest Accuracy:", test_accuracy, file=fp)

print("Results from ./trainingSet.txt and ./testSet.txt:")
print("\tTrain Accuracy:", train_accuracy)
print("\tTest Accuracy:", test_accuracy)





