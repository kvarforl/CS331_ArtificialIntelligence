Implementation of a binomial Naive Bayes Classifier that classifies yelp reviews as positive (1) or negative (0).

To run:
```bash
python3 binomial_bayes.py
```

Data is read from trainSet.txt and testSet.txt. Resulting accuracies are printed to screen and stored in results.txt. Bagged train and test output is stored in `preprocessed_*.txt files.` Bagging was implemented by me, instead of using external packages. All code authored by me.

To run on engr servers, you need to install Pandas and Numpy, using the following:

```bash
pip3 --user install pandas
pip3 --user install numpy
```
