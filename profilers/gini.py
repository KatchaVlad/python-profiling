import numpy as np


def get_area(lst):
    heights = np.cumsum(lst)
    areas = np.cumsum(heights - lst / 2.)
    return areas[-1], heights[-1]


def gini(list_of_values):
    """
    Compute Gini index, an indicator usually used for measurement of economic inequality
    see : https://en.wikipedia.org/wiki/Gini_coefficient
    """

    sorted_list = np.sort(list_of_values)
    area, height = get_area(sorted_list)
    fair_area = height * len(list_of_values) / 2.
    return (fair_area - area) / fair_area

