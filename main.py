from experiment import Experiment
from util import makeLin

experiment = Experiment()
experiment.read_adjacency_matrix_from_file("Wbig_sparse.txt")
# experiment.read_adjacency_matrix(makeLin(6))

# experiment.reset()

print(f"{experiment.iterations}) Infected {len(experiment.infected_people)}", end=' | ')
print(f"Immune {len(experiment.immune_people)}")

for _ in range(20):
    experiment.reset()

    while not experiment.virus_is_gone():
        experiment.step()
        print(f"{experiment.iterations}) Infected {len(experiment.infected_people)}", end=' | ')
        print(f"Immune {len(experiment.immune_people)}")

    experiment.take_mean()

experiment.plot()
