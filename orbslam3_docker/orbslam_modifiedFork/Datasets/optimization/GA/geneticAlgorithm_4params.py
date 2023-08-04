#!/usr/bin/env python
import random
import pandas as pd
# import sys
import math

# ROS IMPORTS
import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
# parent_dir = os.path.dirname(current_dir)
parent_dir = os.sep.join(current_dir.split(os.sep)[:-2])
print(parent_dir)
sys.path.insert(1, parent_dir)

import rospy

from changeYamlFileValues import Change_Yaml_Parameters
from readParams import Read_Required_Params
from createIcrementedDatasetTestFolder import create_incremented_folder
from parseResults import ParseResults_SubSubfolder, Update_Global_Variables
from automateORBSLAM import list_bag_files, Run_ORBSlam_and_Dataset
from parseResults_Generic import find_files
from std_msgs.msg import String, Float32
import time
# END OF ROS IMPORTS

# Parameters
# The number of individuals in the population.
POPULATION_SIZE = 30

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
MAX_GENERATIONS = 30

# The number of individuals selected for the tournament in tournament selection.
# The individual with the highest fitness in the tournament is selected as a parent.
TOURNAMENT_SIZE = 5

# The number of the fittest individuals that are automatically passed to the next generation.
# This is a form of elitism, which ensures that the best solutions found so far are not lost.
ELITISM_SIZE = 3

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

#Param3 = iniThFAST
PARAM3_MIN = 18  # minimum value for parameter 1
PARAM3_MAX = 50  # maximum value for parameter 1
GENE3_LENGTH_BINARY = 6 #(UP TO 64)

# #Param4 = n of orb features
# PARAM4_MIN = 600  # minimum value for parameter 2
# PARAM4_MAX = 1500 # maximum value for parameter 2
# GENE4_LENGTH_BINARY = 11 #(UP TO 2048)

# The length of the binary string that represents the parameters being optimized.
# This should be twice the number of bits needed to represent the maximum parameter value in binary,
# because the binary string is split into two parts to represent two parameters.

#       The range of param1 is 110 (130 - 20) and 
#       the range of param2 is 900 (1500 - 600), 
#       so you need at least ceil(log2(110)) = 7 bits for param1 and
#       ceil(log2(900)) = 11 bits for param2. 
#       Therefore, the total GENOME_LENGTH should be at least 17 (7 + 10).
GENOME_LENGTH = GENE1_LENGTH_BINARY + GENE2_LENGTH_BINARY + GENE3_LENGTH_BINARY #24 #18

# Track Generation Number
Current_Generation = 0

results = pd.DataFrame(columns=['Generation', 'Solution', 'Fitness', 'Parameters','Fittest'])
# PATH_TO_CSV = 

# ROS CLASSES
received_rmse = 0
last_received_rmse = 0
parameters = Read_Required_Params('optimizationParameters_4.txt')
dataset_dir = parameters['dataset_dir']
root_dir = parameters['root_dir']
test_results_path = parameters['test_results_path']
test_parameter = parameters['test_parameter']

bag_files, filtered_files = list_bag_files(dataset_dir, ["20230331_1", "normal"])
pathToSaveTestResults_testParameter = create_incremented_folder(test_results_path, folder_name_suffix=test_parameter)

# ROS GLOBAL VARIABLES

# ROS CLASSES
def is_float_num(n):
    return isinstance(n, (int, float)), isinstance(n, float)

class Receiver:
    def __init__(self,rospy):
        self.received_rmse=0
        self.received_expected_data = False
        # rospy.init_node('receiver')
        rospy.Subscriber('rmse_to_GA', Float32, self.callback)

    def callback(self, msg):
        # global received_rmse
        rospy.loginfo('Received: %s', msg.data)
        is_digit, is_float = is_float_num(msg.data)
        if is_digit == True:
            self.received_expected_data = True
            self.received_rmse = msg.data

    def spin(self):
        rate = rospy.Rate(1)  # 1 Hz
        while not rospy.is_shutdown() and not self.received_expected_data:
            rate.sleep()
        self.received_expected_data = False  

class Sender:
    def __init__(self,rospy):
        # rospy.init_node('sender')
        self.publisher = rospy.Publisher('cmd_from_GA', String, queue_size=10)
    def send(self, data):
        msg = String()
        msg.data = data
        # print(msg.data)
        self.publisher.publish(msg)

# ROS NODE INIT, SENDER/RECEIVER INIT
rospy.init_node('GA_Node')
sender = Sender(rospy)
time.sleep(1)
receiver = Receiver(rospy)
time.sleep(1)
# END OF ROS CLASSES

class Chromosome :
    def __init__(self , length, function):
        self.genes = ""
        self.function = function
        self.param1_decimal=0
        self.param2_decimal=0
        self.param3_decimal=0
        self.param4_decimal=0
        self.fitness=0
        # for i in range(length):
        #     self.genes += str(random.randint(0, 1)) 
        self.gene1 = self.generate_genes(GENE1_LENGTH_BINARY) 
        self.gene2 = self.generate_genes(GENE2_LENGTH_BINARY)
        self.gene3 = self.generate_genes(GENE3_LENGTH_BINARY)

        # self.genes = self.generate_genes(GENE1_LENGTH_BINARY) + self.generate_genes(GENE2_LENGTH_BINARY) + self.generate_genes(GENE3_LENGTH_BINARY)
        self.combine_chromosome_from_gene()
        # print(self.genes)
        self.calculateTheFitness()    
    
    def generate_genes(self, length):
        genes = ""
        for i in range(length):
            genes += str(random.randint(0, 1))
        return genes.zfill(length)

    def combine_chromosome_from_gene(self):
        self.genes = self.gene1 + self.gene2 + self.gene3

    def calculateTheFitness(self,chromosome_in_population=False,is_fittest=""):
        global results
        _,_ = self.convertToDecimal()
        fitnessValue = self.function(self.param1_decimal, self.param2_decimal,param3=self.param3_decimal, param4=self.param4_decimal)
        self.fitness = fitnessValue
        if chromosome_in_population == True:
            results = results.append({
            'Generation': Current_Generation,
            'Solution': "\""+  self.genes + "\"",
            'Fitness': self.fitness,
            'Parameters': (self.param1_decimal, self.param2_decimal,self.param3_decimal, self.param4_decimal),
            'Fittest' : ("Fittest" if (is_fittest.lower() == "fittest") else ("Elite" if (is_fittest.lower() == "elite") else "Population"))
            }, ignore_index=True)
        
        
    def convertToDecimal(self):
        global PARAM1_MAX, PARAM1_MIN, PARAM2_MAX, PARAM2_MIN
        # Split genes into two parts
        # genes1 = self.genes[:len(self.genes)//2]
        # genes2 = self.genes[len(self.genes)//2:]
        
        # Split genes into two parts based on the lengths of the binary representations for each parameter
        genes1 = self.genes[:GENE1_LENGTH_BINARY]
        genes2 = self.genes[GENE1_LENGTH_BINARY:GENE1_LENGTH_BINARY+GENE2_LENGTH_BINARY]
        genes3 = self.genes[GENE1_LENGTH_BINARY + GENE2_LENGTH_BINARY:GENE1_LENGTH_BINARY+GENE2_LENGTH_BINARY+GENE3_LENGTH_BINARY]
        # print(genes1, genes2)
        # Convert binary strings to integers
        decimal1 = int(genes1, 2)
        decimal2 = int(genes2, 2)
        decimal3 = int(genes3, 2)
        # print(decimal1, decimal2)
        # Scale integers to parameter ranges
        param1 = math.ceil(((decimal1 * 1.0) / (2**len(genes1) - 1)) * (PARAM1_MAX - PARAM1_MIN) + PARAM1_MIN) * 1.0
        param2 = math.ceil(((decimal2 * 1.0) / (2**len(genes2) - 1)) * (PARAM2_MAX - PARAM2_MIN) + PARAM2_MIN)
        param3 = math.ceil(((decimal3 * 1.0) / (2**len(genes3) - 1)) * (PARAM3_MAX - PARAM3_MIN) + PARAM3_MIN)
        # param4 = math.ceil(((decimal2 * 1.0) / (2**len(genes2) - 1)) * (PARAM2_MAX - PARAM2_MIN) + PARAM2_MIN)
        self.param1_decimal = param1
        self.param2_decimal = param2
        self.param3_decimal = param3
        self.param4_decimal = math.floor(param3 * 0.35)
        # print ((decimal1 / (2**len(genes1) - 1)) , "*", (PARAM1_MAX - PARAM1_MIN) , "+", PARAM1_MIN) 
        # print(param1,param2)
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
            chromosome.calculateTheFitness(chromosome_in_population=True)

class GeneticAlgorithm : 
    def __init__(self , populationSize , chromosomeSize , tournamentSize , elitismSize , mutationRate , function):
        self.populationSize = populationSize
        self.chromosomeSize = chromosomeSize
        self.tournamentSize = tournamentSize
        self.elitismSize    = elitismSize
        self.mutationRate   = mutationRate
        self.function       = function
    
    def reproduction(self , population):
        global results, Current_Generation
        temp = []
        temp[:self.elitismSize] = population.getNFittestChromosomes(self.elitismSize)
        print("Starting Gen ", Current_Generation)
        for i in range(self.elitismSize):
            print("\t ", i  ," ",temp[i].genes,"  rmse: ", temp[i].fitness , "Fittest" if i == 0 else "Elite")
            results = results.append({
                'Generation': Current_Generation,
                'Solution': "\""+  temp[i].genes + "\"",
                'Fitness': temp[i].fitness,
                'Parameters': (temp[i].param1_decimal, temp[i].param2_decimal,temp[i].param3_decimal, temp[i].param4_decimal),
                'Fittest' : "Fittest" if i == 0 else "Elite"
                }, ignore_index=True)
        i = self.elitismSize
        while i < self.populationSize:
            if SELECTION_METHOD == 'tournament':
                parent1 = self.tournamentSelection(population)
                parent2 = self.tournamentSelection(population,exclude = parent1)
            elif SELECTION_METHOD == 'roulette':
                parent1 = self.rouletteWheelSelection(population)
                parent2 = self.rouletteWheelSelection(population)
            
            # child = self.onePointCrossOver(parent1, parent2)
            child1,child2 = self.multiPointCrossOver(parent1, parent2,num_crossover_points=3)

            if USE_MUTATION:
                child1 = self.bitFlipMutation(child1)
                child2 = self.bitFlipMutation(child2)
            # found = any(temp_chromosome.genes == child.genes for temp_chromosome in temp)
            # found = False
            # for temp_chromosome in temp:
            #     if temp_chromosome.genes == child.genes:
            #         found = True
            #         break
            # if found:
            #     print("**!!!!**DUPLICATE CHROMOSOME IN GEN ", Current_Generation,
            #         "\n\t\t Index inside this gen (pop): ",i ,
            #         "\n\t\t Chromosome is ", child.genes
            #         )
            #     continue
            child1.calculateTheFitness(chromosome_in_population=True)
            child2.calculateTheFitness(chromosome_in_population=True)
            temp.append(child1)
            temp.append(child2)
            print("\t ", i  ," ",temp[i].genes,"  rmse: ", temp[i].fitness, "Population")
            i += 1
            temp.append(child2)
            print("\t ", i  ," ",temp[i].genes,"  rmse: ", temp[i].fitness, "Population")
            i += 1
        # for i in range(self.elitismSize , self.populationSize):
        #     if SELECTION_METHOD == 'tournament':
        #         parent1 = self.tournamentSelection(population)
        #         parent2 = self.tournamentSelection(population)
        #     elif SELECTION_METHOD == 'roulette':
        #         parent1 = self.rouletteWheelSelection(population)
        #         parent2 = self.rouletteWheelSelection(population)
            
        #     child = self.onePointCrossOver(parent1, parent2)

        #     # if random.random() < CROSSOVER_RATE:
        #     #     child = self.onePointCrossOver(parent1, parent2)
        #     # elif (child.genes == population.fittest.genes) :
        #     #     # if (population.fittest.genes == parent1.genes):
        #     #     #     child = parent2
        #     #     # elif (population.fittest.genes == parent2.genes):
        #     #     #     child = parent1
        #     #     child = parent2 if (population.fittest.genes == parent1.genes) else parent1

        #     # else:
        #     #     child = parent1 if random.random() < 0.5 else parent2
            
        #     if USE_MUTATION:
        #         child = self.bitFlipMutation(child)
        #         child.calculateTheFitness(chromosome_in_population=True)
        #     found = any(temp_chromosome.genes == child.genes for temp_chromosome in temp)
        #     if found:
        #         i = i -1
        #         continue
        #     temp.append(child)
            
        newPopulation = Population(self.populationSize, self.chromosomeSize, self.function, False)
        newPopulation.chromosomes = temp
        # newPopulation.calculateTheFitnessForAll()
        newPopulation.findTheFittest()
        return newPopulation
        
    def bitFlipMutation(self , child, mutation_per_chromosome = False):
        if mutation_per_chromosome == False:
            # Perform mutation for each gene
            genes = []
            for gene in [child.gene1, child.gene2, child.gene3]:
                if random.random() < self.mutationRate :
                    mutationPoint = random.randint(0, len(gene) -1)
                    genelist = list(gene)
                    genelist[mutationPoint] = "0" if genelist[mutationPoint] == "1" else "1"
                    gene = ''.join(genelist)
                genes.append(gene)
            child.genes = ''.join(genes)
            # return child
        else:
            if random.random() < self.mutationRate :
                mutationPoint = random.randint(0, len(child.genes) -1)
                geneslist = list(child.genes)
                geneslist[mutationPoint] = "0" if geneslist[mutationPoint] == "1" else "1"
                child.genes = ''.join(geneslist)
                # child.calculateTheFitness()
        return child

    def tournamentSelection(self , population, exclude=None):
        tournamentPool = []
        # for i in range(self.tournamentSize):
        while len(tournamentPool) < self.tournamentSize:
            # start from 1 to exclude the fittest
            index = random.randint(0, len(population.chromosomes) -1)
            # tournamentPool.append(population.chromosomes[index])
            chromosome = population.chromosomes[index]
            if chromosome.genes != exclude.genes:
                tournamentPool.append(chromosome)
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
        child = Chromosome(self.chromosomeSize, self.function)
        if random.random() < CROSSOVER_RATE:
            # child = self.onePointCrossOver(parent1, parent2)
            temp = []
            crossOverPoint = random.randint(0, len(parent1.genes) -1)            
            temp[:crossOverPoint] = parent1.genes[:crossOverPoint]
            temp[crossOverPoint:] = parent2.genes[crossOverPoint:]
            child.genes = ''.join(temp)
        # elif (population.fittest.genes == parent1.genes) or (population.fittest.genes == parent2.genes) :
        #     # if (population.fittest.genes == parent1.genes):
        #     #     child = parent2
        #     # elif (population.fittest.genes == parent2.genes):
        #     #     child = parent1
        #     child = parent2 if (population.fittest.genes == parent1.genes) else parent1

        else:
            child = parent1 if random.random() < 0.5 else parent2
        # if not USE_MUTATION:
            # child.calculateTheFitness()
        # child.calculateTheFitness()
        return child
    
    def multiPointCrossOver(self, parent1, parent2, num_crossover_points):
        # Generate crossover points
        crossover_points = sorted(random.sample(range(1, len(parent1.genes) - 1), num_crossover_points))
        
        # Initialize children genes
        child1_genes = []
        child2_genes = []
        
        if random.random() < self.mutationRate :
            # Iterate through crossover points and alternate genes between parents
            for i in range(num_crossover_points + 1):
                start = crossover_points[i - 1] if i != 0 else 0
                end = crossover_points[i] if i < num_crossover_points else len(parent1.genes)
                
                # If i is even, take genes from parent1 for child1 and parent2 for child2
                if i % 2 == 0:
                    child1_genes += parent1.genes[start:end]
                    child2_genes += parent2.genes[start:end]
                # If i is odd, take genes from parent2 for child1 and parent1 for child2
                else:
                    child1_genes += parent2.genes[start:end]
                    child2_genes += parent1.genes[start:end]
        else:
            child1_genes = parent1.genes
            child2_genes = parent2.genes
        # Create child chromosomes
        child1 = Chromosome(self.chromosomeSize, self.function)
        child2 = Chromosome(self.chromosomeSize, self.function)
        child1.genes = ''.join(child1_genes)
        child2.genes = ''.join(child2_genes)
        # child1.calculateTheFitness()
        # child2.calculateTheFitness()
        return child1, child2
    
# Function to be optimized
def f(param1, param2, param3=None, param4=None):
    print("#$%*** PARAMERTERS = ",param1,param2)
    # sys.exit()
    global receiver, sender
    global parameters, dataset_dir, root_dir, test_results_path, test_parameter, bag_files, filtered_files, pathToSaveTestResults_testParameter
    # Here, replace with your SLAM system function

    new_ThDepth = param1
    new_ORBextractor_nFeatures = int(param2)
    new_ORBextractor_iniThFAST = int(param3)
    new_ORBextractor_minThFAST = int(param4)

    new_ThDepth = new_ThDepth*1.0
    Change_Yaml_Parameters( new_ThDepth=new_ThDepth,
                            new_ORBextractor_nFeatures = new_ORBextractor_nFeatures,
                            ORBextractor_iniThFAST=new_ORBextractor_iniThFAST, 
                            ORBextractor_minThFAST=new_ORBextractor_minThFAST)
    # pathToSaveTestResults = os.path.join(pathToSaveTestResults_testParameter,((str(int(new_ThDepth)).zfill(4)) +"_"+ (str(new_ORBextractor_nFeatures).zfill(4))).replace('.', '_'))

    pathToSaveTestResults = create_incremented_folder(pathToSaveTestResults_testParameter, 
                                                      folder_name_suffix=((str(int(new_ThDepth)).zfill(4)) +
                                                        "_"+ (str(new_ORBextractor_nFeatures).zfill(4)) + 
                                                        "_"+ (str(new_ORBextractor_iniThFAST).zfill(3)) +
                                                        "_"+ (str(new_ORBextractor_minThFAST).zfill(3))
                                                        ).replace('.', '_'))

    # os.makedirs(pathToSaveTestResults, exist_ok=True)
    print("running orb slam")
    Run_ORBSlam_and_Dataset(filtered_files[0], pathToSaveTestResults)
    # time.sleep(3)

    # full_path, relative_path = find_files(parameters['ROOT_DIR'], "FrameTrajectory_TUM_Format.txt", parameters['STEREO_FOLDER_NAME'],parameters['test_parameter'])
    evaluationParameters =Update_Global_Variables("parseResultsParameters.txt")
    _ , resultInstance_Index = os.path.split(pathToSaveTestResults_testParameter)
    subfolder_path, subfolder = os.path.split(pathToSaveTestResults)
    subfolder_path = (os.path.join(subfolder_path, subfolder))
    print(resultInstance_Index,"\n", subfolder,"\n" ,subfolder_path,"\n", os.getcwd())
    if "FrameTrajectory_TUM_Format.txt" in sorted(os.listdir(pathToSaveTestResults)):
        eval_command = ParseResults_SubSubfolder(subfolder, sorted(os.listdir(subfolder_path)),
                                subfolder_path, 
                                dataset_ground_truth_folder=evaluationParameters['dataset_ground_truth_folder'], 
                                Stereo_Folder_Name=resultInstance_Index, 
                                external_server_evaluation=True)
        sender.send(eval_command)
        receiver.spin()
        receiver.received_rmse
        return receiver.received_rmse
    # Run your SLAM system with param1 and param2, get the trajectory and calculate the RMSE

    # return the negative RMSE as the fitness
    # return -RMSE

    # pass
    else:
        return 999.0


def filter_group_by_min(dfg, col):
    '''Get the rows with the minimum value of a column in a Pandas group

    Args:
        dfg (pandas.core.groupby): Pandas group
        col (str): Column name in the DF for which you wish to calculate the minimum
    '''
    return dfg[dfg[col] == dfg[col].min()]


def get_min_in_each_group(df, group_col, min_col):
    '''Get the rows with the minimum value of a column in a Pandas group

    Args:
        df (pandas.dataframe): Pandas DataFrame
        group_col (str): Column in the DF to group by
        min_col (str): Column in the DF to calculate the minimum of
    
    Returns:
        output (pandas.dataframe): Pandas DataFrame filtered by the minimum of each group
    '''

    output = df.groupby(group_col, group_keys=False)\
        .apply(lambda x: filter_group_by_min(x, min_col))
    return output

if __name__ == "__main__":


    # Generate the initial population
    initialPopulation = Population(populationSize = POPULATION_SIZE, chromosomeSize = GENOME_LENGTH, function = f, init = True)

    # Create an instance of Genetic Algorithm
    GeneticAlgo = GeneticAlgorithm(populationSize = POPULATION_SIZE, chromosomeSize = GENOME_LENGTH, tournamentSize = TOURNAMENT_SIZE, elitismSize = ELITISM_SIZE, mutationRate = MUTATION_RATE, function = f)

    population = initialPopulation

    # Create empty lists for each column
    generation_list = ["*"]
    solution_list = ["*"]
    fitness_list = ["*"]
    parameters_list = ["*"]
    fittest_list = ["*"]
    best_param1, best_param2 = None, None
    # with open(os.path.join(pathToSaveTestResults_testParameter,'output.txt'), 'a') as f:
        # Repeat the process for the number of generations
    for i in range(MAX_GENERATIONS):
        Current_Generation = i    
        population = GeneticAlgo.reproduction(population)
        # best_param1, best_param2 = population.fittest.convertToDecimal()
        best_param1, best_param2 = population.fittest.param1_decimal , population.fittest.param2_decimal

        # print >>f, "# Generation: ", i 
        # print >>f, "\t solution: ", population.fittest.genes
        # print >>f, "\t fitness: ", population.fittest.fitness
        # with open(os.path.join(pathToSaveTestResults_testParameter,'output_zew.txt'), 'a') as fff:
        #     print >>fff, "\t parameters: ", best_param1, best_param2

        # results = results.append({
        # 'Generation': i,
        # 'Solution': population.fittest.genes,
        # 'Fitness': population.fittest.fitness,
        # 'Parameters': (best_param1, best_param2)
        # }, ignore_index=True)
        print("### Gen", Current_Generation,
            "\n\tBest solution: ", population.fittest.genes, 
            "\n\tBest fitness: ", population.fittest.fitness,
            "\n\tBest parameters: ",population.fittest.param1_decimal , population.fittest.param2_decimal ,population.fittest.param3_decimal, population.fittest.param4_decimal )
        generation_list.append(i)
        solution_list.append("\""+ population.fittest.genes + "\"")
        fitness_list.append(population.fittest.fitness)
        # parameters_list.append((best_param1, best_param2))
        parameters_list.append((population.fittest.param1_decimal , population.fittest.param2_decimal,population.fittest.param3_decimal, population.fittest.param4_decimal))
        fittest_list.append("Fittest")
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
    new_results = pd.DataFrame({
    'Generation': generation_list,
    'Solution': solution_list,
    'Fitness': fitness_list,
    'Parameters': parameters_list,
    'Fittest': fittest_list
    })


    # Print the best solution
    print("Best solution: ", "\""+ population.fittest.genes +"\"")
    print("Best fitness: ", population.fittest.fitness)
    # best_param1, best_param2 = population.fittest.convertToDecimal()
    print("Best parameters: ",population.fittest.param1_decimal , population.fittest.param2_decimal,population.fittest.param3_decimal, population.fittest.param4_decimal )
    # print("Best parameters: ", best_param1, best_param2)
    # fittest_for_each_gen = results.groupby('Generation')['Fitness'].min()
    # Calculate the minimum value in the Fitness column and group the DF by the Generation column

    best_params_in_each_gen = get_min_in_each_group(results, 'Generation', 'Fitness')
    
    # Append the new DataFrame to the existing one
    results = results.append(new_results, ignore_index=True, sort=False)
    # Save the best parameters in a new file
    best_params_in_each_gen.to_csv(os.path.join(pathToSaveTestResults_testParameter,'best_params_in_each_gen.csv'))
    results.to_csv(os.path.join(pathToSaveTestResults_testParameter,'results.csv'), index=False)
    for i in range (len(fitness_list)-1):
        print(generation_list[i], solution_list[i], fitness_list[i], parameters_list[i])
