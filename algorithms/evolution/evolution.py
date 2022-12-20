import numpy as np
from random import choice
from collections import deque


class Evolution:
    def __init__(self, max_iter=100, probability=0.5, alpha=1):
        self.max_iter = max_iter
        self.probabilities = [1 - probability, probability]
        self.alpha = alpha
        self.population = []
        self.ranks = []
        self.best = None

    def fit(self,
            loss_function=None,
            vector_size=None,
            population_size=10):
        old_generation = np.array([np.random.rand(vector_size) for _ in range(population_size)])
        losses = np.array([loss_function(vector) for vector in old_generation])
        new_generations = []
        generation_index = np.arange(0, population_size)
        for _ in range(self.max_iter):
            for i, old_vector in enumerate(old_generation):
                index = np.random.choice(generation_index, size=3, replace=False)
                v_1, v_2, v_3 = old_generation[index]
                v = v_1 + self.alpha * (v_2 - v_3)
                crossover_mask = np.random.choice([False, True], vector_size, p=self.probabilities)
                new_vector = v * crossover_mask + old_vector * (~crossover_mask)
                new_loss = loss_function(new_vector)
                if losses[i] > new_loss:
                    new_generations.append(new_vector)
                    losses[i] = new_loss
                else:
                    new_generations.append(old_vector)
            old_generation = np.array(new_generations)
            new_generations = []
        self.ranks = np.argsort([loss_function(vector) for vector in old_generation])
        self.population = old_generation[self.ranks]
        self.best = self.population[0]
        return self

    def get_best(self, loss_function):
        idx = np.argmin([loss_function(vector) for vector in self.population])
        return self.population[idx]
