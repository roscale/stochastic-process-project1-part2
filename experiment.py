import itertools
import random
from typing import List

from person import Person, State
from util import random_percentage


class Proportion:
    VALUE = 0
    PERCENTAGE = 1


class Experiment:
    def __init__(self, title):
        self.title = title
        self.iterations = 0
        self.iterations_accum = []

        self.beta = None
        self.mu = None
        self.immunization_speedup = 1.0

        self.total = None
        self.people: List[Person] = []

        self.hospitalized_people = []
        self.infected_people: List[Person] = []
        self.immune_people: List[Person] = []

        # The number of infected people for each experiment for each time t
        self.susceptible_people_accum = []
        self.infected_people_accum = []
        self.immune_people_accum = []

        self.susceptible_people_history = []
        self.infected_people_history = []
        self.immune_people_history = []

        # The mean of infected duration for each experiment
        self.infected_duration_mean_accum = []

        self.beds = 0
        self.maximum_occupied_beds = 0  # Could be greater than the total number of beds
        self.hospitalised_ratio = 0.0

    def soft_reset(self):
        self.iterations = 0
        self.hospitalized_people = []

        # Make all the people susceptible again
        for person in self.people:
            person.state = State.SUSCEPTIBLE
            person.infected_duration = 0

        self.infected_people_history.clear()
        self.immune_people_history.clear()
        self.susceptible_people_history.clear()

        self.infected_people: List[Person] = []
        self.immune_people: List[Person] = []

    def read_adjacency_matrix_from_file(self, filepath):
        # Just count the number of people
        n_people = -1
        adj_matrix = open(filepath, "r")
        for line in adj_matrix:
            indices = [int(x) for x in line.split(" ")]
            if indices[0] > n_people:
                n_people = indices[0]
            if indices[1] > n_people:
                n_people = indices[1]
        adj_matrix.close()

        # Prepare the storage for all the people
        self.people.clear()
        self.total = n_people
        for _ in range(self.total):
            self.people.append(Person())

        # Create all the edges of the graph
        adj_matrix = open(filepath, "r")
        for line in adj_matrix:
            indices = line.split(" ")
            i = int(indices[0]) - 1
            j = int(indices[1]) - 1

            self.people[i].add_neighbour(self.people[j])

    def read_adjacency_matrix(self, matrix):
        # Prepare the storage for all the people
        self.people.clear()
        self.total = len(matrix)
        for _ in range(self.total):
            self.people.append(Person())

        # Create all the edges of the graph
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                self.people[i].add_neighbour(self.people[j])

    # To be called after reading the adjacency matrix or after a soft reset
    def set_initially_infected(self, proportion, amount):
        def infect_n_people(n):
            for i in range(n):
                infected_person = random.choice(self.people)
                if infected_person not in self.infected_people:
                    self.infected_people.append(infected_person)
                    infected_person.state = State.INFECTED

        if proportion == Proportion.VALUE:
            infect_n_people(amount)
        elif proportion == Proportion.PERCENTAGE:
            infect_n_people(int(amount / 100 * self.total))

    def set_probabilities(self, beta, mu):
        self.beta = beta
        self.mu = mu

    # Sets the initial data before running the simulation
    def prepare_chain(self):
        n_infected = len([p for p in self.people if p.state == State.INFECTED])
        n_immune = len([p for p in self.people if p.state == State.IMMUNE])

        self.infected_people_history.append(n_infected)
        self.immune_people_history.append(n_immune)
        self.susceptible_people_history.append(self.total - n_infected - n_immune)

    # Advances the simulation
    def step(self):
        self.iterations += 1

        # Infect others
        infected_people_now = []
        for infected in [p for p in self.infected_people if p not in self.hospitalized_people]:
            infected_neighbours = infected.infect_neighbours(self.beta)
            infected_people_now.extend(infected_neighbours)

        # Hospitalise a fixed percentage of new infected people
        hospitalised_people_now = []
        n_hospitalised_people_now = int(self.hospitalised_ratio * len(infected_people_now))
        while len(hospitalised_people_now) != n_hospitalised_people_now:
            to_be_hospitalised = random.choice(infected_people_now)
            if to_be_hospitalised not in hospitalised_people_now:
                hospitalised_people_now.append(to_be_hospitalised)

        # Immunise people
        for person in self.people:
            if person in self.hospitalized_people and person not in hospitalised_people_now:
                will_recover = random_percentage(self.mu * self.immunization_speedup)
                if will_recover:
                    person.state = State.IMMUNE
                    self.immune_people.append(person)
                    self.infected_people.remove(person)
                    self.hospitalized_people.remove(person)

            elif person.is_infected() and person not in infected_people_now:
                will_recover = random_percentage(self.mu)
                if will_recover:
                    person.state = State.IMMUNE
                    self.immune_people.append(person)
                    self.infected_people.remove(person)

        self.infected_people.extend(infected_people_now)
        self.hospitalized_people.extend(hospitalised_people_now)

        # Increment infected duration
        for person in self.infected_people:
            person.infected_duration += 1

        self.infected_people_history.append(len(self.infected_people))
        self.immune_people_history.append(len(self.immune_people))
        self.susceptible_people_history.append(self.total - len(self.infected_people) - len(self.immune_people))

        n_hospitalised_people = len(self.hospitalized_people)
        if n_hospitalised_people > self.maximum_occupied_beds:
            self.maximum_occupied_beds = n_hospitalised_people

    def virus_is_gone(self):
        return len(self.infected_people) == 0

    def plot(self):
        import matplotlib.pyplot as plt
        import numpy as np
        import pandas as pd

        print(f"The average duration of infected people is {np.mean(self.infected_duration_mean_accum)}")

        susceptible_people_means = [np.mean(accum) for accum in self.susceptible_people_accum]
        infected_people_means = [np.mean(accum) for accum in self.infected_people_accum]
        immune_people_means = [np.mean(accum) for accum in self.immune_people_accum]

        infected_people_means = list(itertools.takewhile(lambda x: x >= 0.4/100 * self.total, infected_people_means))
        susceptible_people_means = susceptible_people_means[:len(infected_people_means)]
        immune_people_means = immune_people_means[:len(infected_people_means)]

        # n_average_iterations = int(np.mean(self.iterations_accum))
        # susceptible_people_means = susceptible_people_means[:n_average_iterations]
        # infected_people_means = infected_people_means[:n_average_iterations]
        # immune_people_means = immune_people_means[:n_average_iterations]

        data = pd.DataFrame({
            'group_A': susceptible_people_means,
            'group_B': infected_people_means,
            'group_C': immune_people_means
        }, index=range(1, len(susceptible_people_means) + 1))

        # We need to transform the data from raw data to percentage (fraction)
        data_perc = data.divide(data.sum(axis=1), axis=0)

        # Make the plot
        plt.stackplot(
            range(1, len(susceptible_people_means) + 1), data_perc["group_A"], data_perc["group_B"],
            data_perc["group_C"],
            labels=['Susceptible', 'Infecté', 'Rétablis'])
        plt.legend(loc='upper right')
        plt.margins(0, 0)
        plt.title(self.title)
        plt.xlabel('temps')
        plt.ylabel('taux de personnes')

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

        # Take mean of infected duration
        durations = []
        for person in self.people:
            if person.infected_duration > 0:
                durations.append(person.infected_duration)

        import numpy as np
        if len(durations) != 0:
            duration_mean = np.mean(durations)
            self.infected_duration_mean_accum.append(duration_mean)

    # Various protection methods
    def set_number_of_beds(self, beds, hospitalised_ratio):
        self.beds = beds
        self.hospitalised_ratio = hospitalised_ratio

    def vaccinate_people(self, amount):
        people_to_vaccinate = []
        n = int(amount / 100 * self.total)

        while len(people_to_vaccinate) != n:
            person = random.choice(self.people)
            if person.state != State.INFECTED:
                person.state = State.IMMUNE
                people_to_vaccinate.append(person)
                self.immune_people.append(person)

    def reduce_interactions(self, amount):
        for person in self.people:
            n_neighbours_to_remove = int(amount * len(person.neighbours))
            for _ in range(n_neighbours_to_remove):
                neighbour_to_remove = random.choice(person.neighbours)

                neighbour_to_remove.neighbours.remove(person)
                person.neighbours.remove(neighbour_to_remove)

    def give_meds_to_patients(self, immunization_speedup):
        self.immunization_speedup = immunization_speedup
