class Chromosome:
    def __init__(self, x1: float, x2: float, x3: float):
        self.x1 = x1
        self.x2 = x2
        self.x3 = x3

    def __str__(self):
        return "[x1: {0:.4f}, x2: {1:.4f}, x3: {2:.4f}]".format(self.x1, self.x2, self.x3)