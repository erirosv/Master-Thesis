### OLD
Support Vector Machines (SVM) is a powerful machine learning algorithm used for classification, regression, and outlier detection. It finds the best possible boundary that can separate the two classes in the input data by finding a hyperplane in the input space that maximally separates the two classes. This hyperplane is chosen such that the distance between the hyperplane and the nearest data points from each class is maximized. These nearest data points are called support vectors. The hyperplane that separates the two classes is defined as wT ∗ x + b = 0, where w is the weight vector, x is the input vector, and b is the bias term [42], [43].

The SVM algorithm optimizes a cost function that penalizes misclassifications and encourages a large margin between the hyperplane and the nearest data points. The cost function is typically a convex optimization problem that can be solved using optimization algorithms like gradient descent [42], [43].

---

## NEW
Support Vector Machines (SVM) is a powerful machine learning algorithm that finds the best possible boundary to separate two classes in input data. It does so by finding a hyperplane in the input space that maximally separates the two classes, with the hyperplane chosen so that the distance between the hyperplane and the nearest data points from each class is maximized. These nearest data points are called support vectors, and the hyperplane that separates the two classes is defined as wT ∗ x + b = 0, where w is the weight vector, x is the input vector, and b is the bias term [42], [43].

To achieve this, the SVM algorithm optimizes a cost function that penalizes misclassifications and encourages a large margin between the hyperplane and the nearest data points. The cost function is typically a convex optimization problem that can be solved using optimization algorithms like gradient descent [42], [43].

The cost function for SVM is the hinge loss function, given by:

**SVM MATH FORMULA**

Here, n is the number of training instances, xi is the i-th input vector, yi is the corresponding target output, and alpha is a regularization hyperparameter that controls the tradeoff between maximizing the margin and minimizing the misclassifications. The first term in the cost function is the classification loss, which penalizes misclassifications, and the second term is the regularization term, which encourages a small weight vector [42], [43].

To optimize this cost function, one can use optimization algorithms such as stochastic gradient descent or quadratic programming. The optimal solution for the SVM algorithm is found when the weight vector w and the bias term b are determined such that they minimize the cost function while satisfying the constraints that ensure the hyperplane separates the two classes with the maximum margin. Therefore, SVM is a linear model for binary classification that tries to find the best possible boundary that can separate the two classes in the input data by maximizing the margin between the hyperplane and the nearest data points while minimizing misclassifications using the hinge loss function [42], [43].

**PSEUDO CODE**

**ALGORITHM**
