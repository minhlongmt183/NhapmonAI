import numpy as np

def generateChromosome():
    global nQueens
    init_distribution = np.arange(nQueens)
    np.randome.shuffle(init_distribution)
    return init_distribution

def generatePopulation(population_size = 100):
    global POPULATION

    POPULATION = population_size

    population = [BoardPosition() for i in range(population_size)]
    for i in range(population_size):
        population[i].setSequence(generateChromosome())
        population[i].setFitness(fitness(population[i].sequence))

    return population
