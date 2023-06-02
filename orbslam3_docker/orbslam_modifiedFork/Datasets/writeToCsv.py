#!/usr/bin/env python
import pandas as pd

# global variables for the table size
num_rows = 4
num_cols = 0

# global variable for the data
data = {}
df = pd.DataFrame(data)

def write_to_csv(col_name, row_idx, value):
    global num_cols, data

    # check if column name exists
    if col_name in data:
        col_data = data[col_name]
    else:
        # create new column
        col_data = [None] * num_rows
        data[col_name] = col_data
        num_cols += 1

    # update value at the specified row index
    col_data[row_idx] = value

    # write to CSV file
    df = pd.DataFrame(data)
    df.to_csv("output.csv", index=False)
write_to_csv("Column 1", 0, 10)
write_to_csv("Column 1", 1, 500)
write_to_csv("Column 2", 1, 20)
write_to_csv("Column 3", 2, 30)
write_to_csv("Column 4", 3, 40)
write_to_csv("Column 5", 3, 40)
