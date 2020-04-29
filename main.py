from experiment import Experiment, Proportion
from util import *

experiment = Experiment()
experiment.read_adjacency_matrix_from_file("Wbig_sparse.txt")
# experiment.read_adjacency_matrix(makeLin(6))

# experiment.reset()

print(f"{experiment.iterations}) Infected {len(experiment.infected_people)}", end=' | ')
print(f"Immune {len(experiment.immune_people)}")

for _ in range(1):
    experiment.soft_reset()
    experiment.set_probabilities(0.5, 0.2)
    experiment.set_initially_infected(Proportion.PERCENTAGE, 0.5)
    experiment.vaccinate_people(50.0)

    while not experiment.virus_is_gone():
        experiment.step()
        print(f"{experiment.iterations}) Infected {len(experiment.infected_people)}", end=' | ')
        print(f"Immune {len(experiment.immune_people)}")

    experiment.take_mean()

experiment.plot()
