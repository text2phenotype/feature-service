from enum import Enum

from sklearn.naive_bayes import MultinomialNB
from sklearn.neural_network import MLPClassifier
from sklearn.svm import LinearSVC
from sklearn.linear_model import LogisticRegression


class AspectModelType(Enum):
    """
    Predictions (Model) Classifiers -- each have pros/cons.
    """
    nbc = MultinomialNB(alpha=1.0, fit_prior=True, class_prior=None)
    log = LogisticRegression(C=0.2)
    svm = LinearSVC(C=0.1)
    nn = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(300,), random_state=1)
