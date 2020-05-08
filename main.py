from experiment import Experiment, Proportion
from util import *

# experiment = Experiment("Simulation: Réduction de la probabilité de transmission")
# experiment = Experiment("Simulation: Réduction des interactions entre les individus")
# experiment = Experiment("Simulation: Vaccination d'un pourcentage fixe d'individus")
# experiment = Experiment("Simulation: Traitement avec médicaments pour les patients hospitalisés")
experiment = Experiment("Wbig")
experiment.read_adjacency_matrix_from_file("Wbig_sparse.txt")
# experiment.read_adjacency_matrix(makeFull(6))
# experiment.reduce_interactions(0.33)

# experiment.set_number_of_beds(140, 0.17)

for _ in range(50):
    experiment.soft_reset()
    experiment.set_probabilities(0.5, 0.2)
    # experiment.set_probabilities(0.25, 0.2)
    experiment.set_initially_infected(Proportion.PERCENTAGE, 0.5)
    # experiment.set_initially_infected(Proportion.VALUE, 1)
    # experiment.vaccinate_people(22.0)
    # experiment.give_meds_to_patients(2.5)

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
