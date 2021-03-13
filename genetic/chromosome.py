import numpy as np


class Chromosome:
    def __init__(self, portfolio: np.ndarray):
        self.portfolio = portfolio/np.sum(portfolio)

    def is_valid(self):
        return np.sum(self.portfolio) == 1

    def __str__(self):
        return self.portfolio.__str__()
