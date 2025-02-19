import entropy_estimators as ee


def information_gain(f1, f2):
    """
    This function calculates the information gain, where ig(f1, f2) = H(f1) - H(f1\f2)

    :param f1: {numpy array}, shape (n_samples,)
    :param f2: {numpy array}, shape (n_samples,)
    :return: ig: {float}
    """

    ig = ee.entropyd(f1) - conditional_entropy(f1, f2)
    return ig


def conditional_entropy(f1, f2):
    """
    This function calculates the conditional entropy, where ce = H(f1) - I(f1;f2)
    :param f1: {numpy array}, shape (n_samples,)
    :param f2: {numpy array}, shape (n_samples,)
    :return: ce {float} conditional entropy of f1 and f2
    """

    ce = ee.entropyd(f1) - ee.midd(f1, f2)
    return ce


def su_calculation(f1, f2):
    """
    This function calculates the symmetrical uncertainty, where su(f1,f2) = 2*IG(f1,f2)/(H(f1)+H(f2))
    :param f1: {numpy array}, shape (n_samples,)
    :param f2: {numpy array}, shape (n_samples,)
    :return: su {float} su is the symmetrical uncertainty of f1 and f2
    """
    # calculate information gain of f1 and f2, t1 = ig(f1, f2)
    t1 = information_gain(f1, f2)
    # calculate entropy of f1
    t2 = ee.entropyd(f1)
    # calculate entropy of f2
    t3 = ee.entropyd(f2)
    if t2 + t3 == 0:
        su = 0  #Avoid division by zeor
    else:
        su = 2.0 * t1 / (t2 + t3)

    return su
