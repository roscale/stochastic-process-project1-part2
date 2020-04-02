from experiment import Experiment

experiment = Experiment()
experiment.read_adjacent_matrix_from_file("Wbig_sparse.txt")

for _ in range(10):
    experiment.reset()

    while not experiment.virus_is_gone():
        experiment.step()
        print(f"{experiment.iterations}) Infected {len(experiment.infected_people)}", end=' | ')
        print(f"Immune {len(experiment.immune_people)}")

experiment.plot()
