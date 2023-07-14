#!/usr/bin/env python3
import random
import pandas as pd
import sys
import math
# Parameters
# The number of individuals in the population.
POPULATION_SIZE = 70

# The length of the binary string that represents the parameters being optimized.
# This should be twice the number of bits needed to represent the maximum parameter value in binary,
# because the binary string is split into two parts to represent two parameters.

#       The range of param1 is 110 (130 - 20) and 
#       the range of param2 is 900 (1500 - 600), 
#       so you need at least ceil(log2(110)) = 7 bits for param1 and
#       ceil(log2(900)) = 10 bits for param2. 
#       Therefore, the total GENOME_LENGTH should be at least 17 (7 + 10).
GENOME_LENGTH = 18

# The probability that a bit in a chromosome will be flipped 
# (changed from 0 to 1 or from 1 to 0) during mutation.
MUTATION_RATE = 0.1
# The probability that two parents will be selected for crossover to create a child.
# This is not used in the provided code, but you could use it in the reproduction method
# to decide whether to perform crossover.
CROSSOVER_RATE = 0.8

# The number of generations to run the genetic algorithm.
# A generation is one cycle of the genetic algorithm, including selection, crossover, mutation, 
# and fitness evaluation.
MAX_GENERATIONS = 50

# The number of individuals selected for the tournament in tournament selection.
# The individual with the highest fitness in the tournament is selected as a parent.
TOURNAMENT_SIZE = 4

# The number of the fittest individuals that are automatically passed to the next generation.
# This is a form of elitism, which ensures that the best solutions found so far are not lost.
ELITISM_SIZE = 5

# Whether to use mutation in the genetic algorithm.
# If this is set to False, the bitFlipMutation method will not be called, so no bits will be flipped in the chromosomes.
USE_MUTATION = True

# The method used to select parents for crossover.
# If this is set to 'tournament', tournament selection is used.
# If this is set to 'roulette', roulette wheel selection is used.
SELECTION_METHOD = 'tournament'  # 'tournament' or 'roulette'

# to detect stall generation
USE_STALL_GEN = False
STALL_LIMIT = 20

# Initialize stall counter
stall_counter = 0
prev_best_fitness = None

#Param1 = baseline
PARAM1_MIN = 20  # minimum value for parameter 1
PARAM1_MAX = 120  # maximum value for parameter 1
GENE1_LENGTH_BINARY = 7 #(UP TO 128)

#Param2 = n of orb features
PARAM2_MIN = 600  # minimum value for parameter 2
PARAM2_MAX = 1500 # maximum value for parameter 2
GENE2_LENGTH_BINARY = 11 #(UP TO 2048)

results = pd.DataFrame(columns=['Generation', 'Solution', 'Fitness', 'Parameters'])
# PATH_TO_CSV = 

class Chromosome :
    def __init__(self , length, function):
        self.genes = ""
        self.function = function
        # for i in range(length):
        #     self.genes += str(random.randint(0, 1)) 
        self.genes = self.generate_genes(GENE1_LENGTH_BINARY) + self.generate_genes(GENE2_LENGTH_BINARY)
        self.calculateTheFitness()    
    
    def generate_genes(self, length):
        genes = ""
        for i in range(length):
            genes += str(random.randint(0, 1))
        return genes.zfill(length)

    def calculateTheFitness(self):
        param1, param2 = self.convertToDecimal()
        fitnessValue = self.function(param1, param2)
        self.fitness = fitnessValue
        
    def convertToDecimal(self):
        # Split genes into two parts
        # genes1 = self.genes[:len(self.genes)//2]
        # genes2 = self.genes[len(self.genes)//2:]
        
        # Split genes into two parts based on the lengths of the binary representations for each parameter
        genes1 = self.genes[:GENE1_LENGTH_BINARY]
        genes2 = self.genes[GENE1_LENGTH_BINARY:GENE1_LENGTH_BINARY+GENE2_LENGTH_BINARY]
    
        # Convert binary strings to integers
        decimal1 = int(genes1, 2)
        decimal2 = int(genes2, 2)
        
        # Scale integers to parameter ranges
        param1 = math.ceil((decimal1 / (2**len(genes1) - 1)) * (PARAM1_MAX - PARAM1_MIN) + PARAM1_MIN) * 1.0
        param2 = math.ceil((decimal2 / (2**len(genes2) - 1)) * (PARAM2_MAX - PARAM2_MIN) + PARAM2_MIN)

        return param1, param2

class Population :
    def __init__(self , populationSize , chromosomeSize , function , init):
        self.chromosomes = []
        if init :
            self.chromosomes = [Chromosome(chromosomeSize , function) for i in range(populationSize)]
            self.chromosomes.sort(key = lambda x:x.fitness)
            self.fittest = self.chromosomes[0]
    
    def getNFittestChromosomes(self, n):
        self.chromosomes.sort(key = lambda x:x.fitness)
        return self.chromosomes[:n]
    
    def findTheFittest(self):
        self.chromosomes.sort(key = lambda x:x.fitness)
        self.fittest = self.chromosomes[0]
    
    def calculateTheFitnessForAll(self):
        for chromosome in self.chromosomes:
            chromosome.calculateTheFitness()

class GeneticAlgorithm : 
    def __init__(self , populationSize , chromosomeSize , tournamentSize , elitismSize , mutationRate , function):
        self.populationSize = populationSize
        self.chromosomeSize = chromosomeSize
        self.tournamentSize = tournamentSize
        self.elitismSize    = elitismSize
        self.mutationRate   = mutationRate
        self.function       = function
    
    def reproduction(self , population):
        temp = []
        temp[:self.elitismSize] = population.getNFittestChromosomes(self.elitismSize)
        for i in range(self.elitismSize , self.populationSize):
            if SELECTION_METHOD == 'tournament':
                parent1 = self.tournamentSelection(population)
                parent2 = self.tournamentSelection(population)
            elif SELECTION_METHOD == 'roulette':
                parent1 = self.rouletteWheelSelection(population)
                parent2 = self.rouletteWheelSelection(population)
            
            child = self.onePointCrossOver(parent1, parent2)
            
            if USE_MUTATION:
                self.bitFlipMutation(child)
            
            temp.append(child)
            
        newPopulation = Population(self.populationSize, self.chromosomeSize, self.function, False)
        newPopulation.chromosomes = temp
        newPopulation.findTheFittest()
        # newPopulation.calculateTheFitnessForAll()
        return newPopulation
        
    def bitFlipMutation(self , child):
        if random.random() < self.mutationRate :
            mutationPoint = random.randint(0, len(child.genes) -1)
            geneslist = list(child.genes)
            geneslist[mutationPoint] = "0" if geneslist[mutationPoint] == "1" else "1"
            child.genes = ''.join(geneslist)
            child.calculateTheFitness()

    def tournamentSelection(self , population):
        tournamentPool = []
        for i in range(self.tournamentSize):
            index = random.randint(0, len(population.chromosomes) -1)
            tournamentPool.append(population.chromosomes[index])
        tournamentPool.sort(key = lambda x:x.fitness)
        return tournamentPool[0]

    def rouletteWheelSelection(self, population):
        total_fitness = sum(chromosome.fitness for chromosome in population.chromosomes)
        pick = random.uniform(0, total_fitness)
        current = 0
        for chromosome in population.chromosomes:
            current += chromosome.fitness
            if current > pick:
                return chromosome
    
    def onePointCrossOver(self , parent1 , parent2):
        temp = []
        crossOverPoint = random.randint(0, len(parent1.genes) -1)            
        temp[:crossOverPoint] = parent1.genes[:crossOverPoint]
        temp[crossOverPoint:] = parent2.genes[crossOverPoint:]
        child = Chromosome(self.chromosomeSize, self.function)
        child.genes = ''.join(temp)
        child.calculateTheFitness()
        return child
    
# Function to be optimized
def f(param1, param2):
    print("#$%*** PARAMERTERS = ",param1,param2)
    # sys.exit()
    # Here, replace with your SLAM system function
    # Run your SLAM system with param1 and param2, get the trajectory and calculate the RMSE

    # return the negative RMSE as the fitness
    # return -RMSE
    pass

# Generate the initial population
initialPopulation = Population(populationSize = POPULATION_SIZE, chromosomeSize = GENOME_LENGTH, function = f, init = True)

# Create an instance of Genetic Algorithm
GeneticAlgo = GeneticAlgorithm(populationSize = POPULATION_SIZE, chromosomeSize = GENOME_LENGTH, tournamentSize = TOURNAMENT_SIZE, elitismSize = ELITISM_SIZE, mutationRate = MUTATION_RATE, function = f)

population = initialPopulation

# Repeat the process for the number of generations
for i in range(MAX_GENERATIONS):    
    population = GeneticAlgo.reproduction(population)
    param1, param2 = population.fittest.convertToDecimal()
    print("# Generation: ", i)
    print("\t solution: ", population.fittest.genes)
    print("\t fitness: ", population.fittest.fitness)
    print("\t parameters: ", param1, param2)
    results = results.append({
    'Generation': i,
    'Solution': population.fittest.genes,
    'Fitness': population.fittest.fitness,
    'Parameters': (param1, param2)
    }, ignore_index=True)
    # Check if fitness has improved
    if USE_STALL_GEN != True:
        continue
    # law el error bada2 yezid tany ba3d makan olayel ma3naha eni kont f makan kowayes aw fi rakam kwoayes
    # the idea is en el rakam mesh hayzid 20 mara wara ba3d msln
    if prev_best_fitness is not None and population.fittest.fitness >= prev_best_fitness:
        stall_counter += 1
    else:
        stall_counter = 0
        # Update previous best fitness
        prev_best_fitness = population.fittest.fitness
    
    
    # Check if stall limit has been reached
    if stall_counter >= STALL_LIMIT:
        print("Terminating due to stall in fitness improvement.")
        break

# Print the best solution
print("Best solution: ", population.fittest.genes)
print("Best fitness: ", population.fittest.fitness)
best_param1, best_param2 = population.fittest.convertToDecimal()
print("Best parameters: ", best_param1, best_param2)
results.to_csv('results.csv', index=False)
