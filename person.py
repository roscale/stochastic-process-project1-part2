from typing import List

from util import random_percentage


class State:
    SUSCEPTIBLE = 'S'
    INFECTED = 'I'
    IMMUNE = 'R'


class Person:
    def __init__(self):
        self.state = State.SUSCEPTIBLE
        self.neighbours: List[Person] = []
        self.infected_duration = 0

    def add_neighbour(self, person):
        self.neighbours.append(person)

    def infect_neighbours(self, chance):
        infected = []
        for neighbour in self.neighbours:
            will_be_infected = random_percentage(chance)
            if neighbour.state == State.SUSCEPTIBLE and will_be_infected:
                neighbour.state = State.INFECTED
                infected.append(neighbour)

        return infected

    def is_infected(self):
        return self.state == State.INFECTED
