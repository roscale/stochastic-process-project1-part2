from experiment import Experiment, Proportion

experiment = Experiment()
experiment.read_adjacency_matrix_from_file("Wbig_sparse.txt")
# experiment.read_adjacency_matrix(makeLin(6))

# experiment.reset()

for _ in range(10):
    experiment.soft_reset()
    experiment.set_probabilities(0.5, 0.2)
    experiment.set_initially_infected(Proportion.PERCENTAGE, 0.5)
    experiment.vaccinate_people(20.0)
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
