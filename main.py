from experiment import Experiment, Proportion
from util import *

experiment = Experiment()
experiment.read_adjacency_matrix_from_file("Wbig_sparse.txt")
# experiment.reduce_interactions(0.35)
# experiment.read_adjacency_matrix(makeLin(6))

experiment.set_number_of_beds(140, 0.17)

for _ in range(20):
    experiment.soft_reset()
    experiment.set_probabilities(0.5, 0.2)
    experiment.set_initially_infected(Proportion.PERCENTAGE, 0.5)
    # experiment.give_meds_to_patients(2.0)

    # experiment.set_initially_infected(Proportion.VALUE, 1)
    # experiment.vaccinate_people(40.0)
    experiment.prepare_chain()

    print(f"TOTAL {experiment.total}")
    print(f"{experiment.iterations}) Infected {len(experiment.infected_people)}", end=' | ')
    print(f"Immune {len(experiment.immune_people)}")

    while not experiment.virus_is_gone():
        experiment.step()
        print(f"{experiment.iterations}) Infected {len(experiment.infected_people)}", end=' | ')
        print(f"Immune {len(experiment.immune_people)}")

    experiment.take_mean()

experiment.plot()
print(f"Maximum hospitalised: {experiment.maximum_occupied_beds}/{experiment.beds}")
