import pandas as pd
import numpy as np
import os



count = 0

labels = pd.read_csv("/data/mschatz1/bbock4/bracken_reports/SAMEA2448331.bracken", sep="\t")


compiled_df = pd.DataFrame(columns=labels['name'].values)
compiled_df["sample"] = " "

data_changed = False


if data_changed == True:

	for file in os.listdir("./bracken_reports"):
		
		curr_file = pd.read_csv("./bracken_reports/" + file, sep="\t")

		compiled_df.loc[len(compiled_df)] = 0.0
		for index, row in curr_file.iterrows():
			# compiled_df[]
			abundance = row.iloc[6]
			name = row.iloc[0]
			sample = file.split(".")[0]

			if name not in compiled_df.columns:
				compiled_df[name] = 0.0
			
			compiled_df.at[count, name] = abundance
			compiled_df.at[count, "sample"] = sample
		compiled_df = compiled_df.copy()
		count += 1
else:
	compiled_df = pd.read_csv("/data/mschatz1/bbock4/compiled_data.csv")


# print(len(compiled_df.columns.values.tolist()))



compiled_df = compiled_df.sort_values(by="sample")
	

	

print("outputting")
compiled_df.to_csv('compiled_data_sorted.csv')

	# print(compiled_df)



