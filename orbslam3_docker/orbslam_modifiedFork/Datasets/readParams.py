#!/usr/bin/env python3

def Read_Required_Params(filename):
    # Initialize empty dictionary to store parameters
    parameters = {}

    # Open the file
    with open(filename, 'r') as f:
        # Read each line in the file
        for line in f:
            # Skip the line if it starts with '#'
            if line.startswith('#') or line.startswith(' ') or line.startswith('\n'):
                continue
            # Split the line into a parameter name and value
            parameter, value = line.strip().split(': ')
            # Store the parameter and its value in the dictionary
            parameters[parameter] = value
    return parameters
# Now you can access the parameters using their names

if __name__ == "__main__":
    parameters = Read_Required_Params('parameters.txt')
    root_dir = parameters['root_dir']
    test_results_path = parameters['test_results_path']
    test_parameter = parameters['test_parameter']
    results_evaluation_path = parameters['results_evaluation_path']

    print("root dir", parameters['root dir'])
    print('Test Path:', test_results_path)
    print('Test Parameter:', test_parameter)
    print('Results Path:', results_evaluation_path)