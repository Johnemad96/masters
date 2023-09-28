#!/usr/bin/env python
import pandas as pd
results = pd.DataFrame(columns=['Generation', 'Solution', 'Fitness', 'Parameters'])

# Create empty lists for each column
generation_list = ["1","3","5","7"]
solution_list = ["5","6","7","8"]
fitness_list = ["1","3","5","7"]
parameters_list = ["5","6","7","8"]



new_results = pd.DataFrame({
    'Generation': generation_list,
    'Solution': solution_list,
    'Fitness': fitness_list,
    'Parameters': parameters_list
})

# Append the new DataFrame to the existing one
results = results.append(new_results, ignore_index=True, sort=False)

# Create empty lists for each column
generation_list = ["*",0,0,0,0]
solution_list = ["*",0,0,55,55]
fitness_list = ["*",1,0,0,0]
parameters_list = ["*",0,0,55,55]



newnew_results = pd.DataFrame({
    'Generation': generation_list,
    'Solution': solution_list,
    'Fitness': fitness_list,
    'Parameters': parameters_list
})

# Append the new DataFrame to the existing one
results = results.append(newnew_results, ignore_index=True, sort=False)
results.to_csv('results.csv', index=False)

print("zewwwwwwwwwww")
print("hobba")