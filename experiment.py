from random import randrange
from typing import List

from person import Person, State
from util import random_percentage


class Experiment:
    def __init__(self):
        self.iterations = 0
        self.total = 2000
        self.people: List[Person] = []

        self.infected_people: List[Person] = []
        self.immune_people: List[Person] = []

        for _ in range(self.total):
            self.people.append(Person())

        # Initially just one is infected
        self.susceptible_people_history = [self.total - 1]
        self.infected_people_history = [1]
        self.immune_people_history = [0]

        self.iterations_accum = []
        # Remember the number of infected people for each experiment for each time t
        self.susceptible_people_accum = []
        self.infected_people_accum = []
        self.immune_people_accum = []

        initially_infected = self.people[randrange(self.total)]
        initially_infected.state = State.INFECTED
        self.infected_people.append(initially_infected)

    def reset(self):
        self.iterations = 0
        self.total = 2000

        for person in self.people:
            person.state = State.SUSCEPTIBLE

        self.infected_people: List[Person] = []
        self.immune_people: List[Person] = []

        # Initial conditions
        self.susceptible_people_history = [self.total - 1]
        self.infected_people_history = [1]
        self.immune_people_history = [0]

        initially_infected = self.people[randrange(self.total)]
        initially_infected.state = State.INFECTED
        self.infected_people.append(initially_infected)

    def read_adjacency_matrix_from_file(self, filepath):
        adj_matrix = open(filepath, "r")

        for line in adj_matrix:
            indices = line.split(" ")
            i = int(indices[0]) - 1
            j = int(indices[1]) - 1

            self.people[i].add_neighbour(self.people[j])

    def read_adjacency_matrix(self, matrix):
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                self.people[i].add_neighbour(self.people[j])

    def step(self):
        self.iterations += 1

        for infected in self.infected_people.copy():
            infected_neighbours = infected.infect_neighbours(0.5)
            self.infected_people.extend(infected_neighbours)

        for person in self.people:
            will_recover = random_percentage(0.2)
            if person.is_infected() and will_recover:
                person.state = State.IMMUNE
                self.immune_people.append(person)
                self.infected_people.remove(person)

        self.infected_people_history.append(len(self.infected_people))
        self.immune_people_history.append(len(self.immune_people))
        self.susceptible_people_history.append(self.total - len(self.infected_people) - len(self.immune_people))

        # print(f"Temps {self.iterations} "
        #       f"I: {len(self.infected_people)} "
        #       f"R: {len(self.immune_people)} "
        #       f"S: {self.total - len(self.infected_people) - len(self.immune_people)}")

    def virus_is_gone(self):
        return len(self.infected_people) == 0

    def plot(self):
        import matplotlib.pyplot as plt
        import numpy as np
        import pandas as pd

        susceptible_people_means = [np.mean(accum) for accum in self.susceptible_people_accum]
        infected_people_means = [np.mean(accum) for accum in self.infected_people_accum]
        immune_people_means = [np.mean(accum) for accum in self.immune_people_accum]

        data = pd.DataFrame({
            'group_A': susceptible_people_means,
            'group_B': infected_people_means,
            'group_C': immune_people_means
        }, index=range(1, len(susceptible_people_means) + 1))

        # We need to transform the data from raw data to percentage (fraction)
        data_perc = data.divide(data.sum(axis=1), axis=0)

        # Make the plot
        plt.stackplot(range(1, len(susceptible_people_means) + 1), data_perc["group_A"], data_perc["group_B"],
                      data_perc["group_C"],
                      labels=['Susceptibles', 'Inféctés', 'Immunisés'],
                      colors=["yellow", "red", "green"])
        plt.legend(loc='upper right')
        plt.margins(0, 0)
        plt.title('Simulation')
        plt.show()

    def take_mean(self):
        self.iterations_accum.append(self.iterations)

        for i, n in enumerate(self.infected_people_history):
            # Grow the list
            if i >= len(self.infected_people_accum):
                self.infected_people_accum.append([])
            self.infected_people_accum[i].append(n)

        for i, n in enumerate(self.susceptible_people_history):
            # Grow the list
            if i >= len(self.susceptible_people_accum):
                self.susceptible_people_accum.append([])
            self.susceptible_people_accum[i].append(n)

        for i, n in enumerate(self.immune_people_history):
            # Grow the list
            if i >= len(self.immune_people_accum):
                self.immune_people_accum.append([])
            self.immune_people_accum[i].append(n)
