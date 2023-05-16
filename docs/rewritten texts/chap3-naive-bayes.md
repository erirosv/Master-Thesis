NOTE: HAve not placed the sources at the correct position...

---

Naïve Bayes is a probabilistic classification algorithm that is often used for text classification, spam filtering, and sentiment analysis [42], [43]. The algorithm is based on Bayes’ theorem, which provides a way to calculate the probability of a hypothesis given some evidence.

The basic idea behind Naïve Bayes is to calculate the probability of a given data point belonging to a particular class, based on the probabilities of the features of the data point [42], [43]. Naïve Bayes assumes that the features are independent of each other, which makes the calculations much simpler.

To calculate the probability of a class label given a new data point xnew, Naïve Bayes uses Bayes’ theorem [42], [43]. According to Bayes’ theorem, the probability of a class label y given a data point x is calculated based on the probability of observing the data point x given that it belongs to class y (P(x|y)), the prior probability of class y (P(y)), and the probability of observing the data point x (P(x)).

**BAYES THEOREM**

To calculate P(x|y), Naïve Bayes assumes that the features are independent of each other [42], [43]. This means that it calculates the probability of observing the new data point xnew given that it belongs to class yi as the product of the probabilities of observing each feature given that it belongs to class yi.

**SECOND FORMULA**

Naïve Bayes uses a probability distribution to model each feature, depending on its type. For example, it can use a Gaussian distribution for continuous features and a categorical distribution for discrete features [42], [43].

To calculate the prior probability of class y (P(y)), Naïve Bayes simply counts the number of data points in each class and divides by the total number of data points [42], [43].

To calculate the probability of observing the data point x (P(x)), Naïve Bayes uses the law of total probability [42], [43]. It calculates the sum of the products of the probability of observing the new data point xnew given that it belongs to each class yi and the prior probability of class yi.

**LAST FORMULA?**

Once Naïve Bayes has calculated the probabilities for each class label, it chooses the one with the highest probability as the predicted class label for the new data point xnew [42], [43].

**COMPLETE ALGORITHM**
