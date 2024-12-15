


import pandas as pd
import numpy as np
def reduce_data(full_data):

	columns = full_data.columns.values
	bad_cols = []
	for col in columns:
		non_zero = np.count_nonzero(full_data[col].values)
		max = np.max(full_data[col].values)
		if(max < .0001 or non_zero < 10):
			# print(col)
			bad_cols.append(col)

	reduced_data = full_data.drop(labels=bad_cols, axis=1)
	print(reduced_data.head())

	return reduced_data

full_data = pd.read_csv("./compiled_data_sorted.csv")
full_data = full_data.drop(labels=["sample","Unnamed: 0.1", "Unnamed: 0"], axis=1)
reduce_data(full_data)
