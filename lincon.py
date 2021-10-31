class Random:
    def __init__(self, seed):
        self.seed = seed 
    def random(self):
        x = self.seed
        self.seed = (106 * self.seed + 1283) % 6075
        return x / self.seed if x < self.seed else self.seed / x 

    def randint(self, start, end):
        self.seed = (106 * self.seed + 1283) % 6075 
        return self.seed % (end - start + 1) + start 
