#!/usr/bin/env python
import sys
import math

def convertToDecimal(genes):
    # Define your global variables here
    PARAM1_MAX = 120
    PARAM1_MIN = 20
    PARAM2_MAX = 1500
    PARAM2_MIN = 600
    GENE1_LENGTH_BINARY = 7
    GENE2_LENGTH_BINARY = 11

    # Split genes into two parts based on the lengths of the binary representations for each parameter
    genes1 = genes[:GENE1_LENGTH_BINARY]
    genes2 = genes[GENE1_LENGTH_BINARY:GENE1_LENGTH_BINARY+GENE2_LENGTH_BINARY]

    # Convert binary strings to integers
    decimal1 = int(genes1, 2)
    decimal2 = int(genes2, 2)

    # Scale integers to parameter ranges
    param1 = math.ceil(((decimal1 * 1.0) / (2**len(genes1) - 1)) * (PARAM1_MAX - PARAM1_MIN) + PARAM1_MIN) * 1.0
    param2 = math.ceil(((decimal2 * 1.0) / (2**len(genes2) - 1)) * (PARAM2_MAX - PARAM2_MIN) + PARAM2_MIN)

    return param1, param2

if __name__ == "__main__":
    # Get the genes from the command-line arguments
    genes = sys.argv[1]
    param1, param2 = convertToDecimal(genes)
    print("Parameter 1: ", param1)
    print("Parameter 2: ", param2)
