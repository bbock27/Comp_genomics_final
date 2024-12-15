import pandas as pd
import numpy as np



def compile_data():
	diag = open("./diagnosies.txt", "r")

	samples = open("./sample_accessions.csv", "r")

	output = open("./diagnosis_sample.csv", "w")

	output.write("sample\tdiagnosis\n")

	for diagnosis, sample in zip(diag, samples):
		line = sample.strip() + "\t" + diagnosis.strip() + "\n"
		output.write(line)

# compile_data()
df = pd.read_csv("/data/mschatz1/bbock4/diagnosis_sample.tsv", sep="\t")


print(df.head())

df = df.sort_values(by="sample")

print(df.head())


data = pd.read_csv("./compiled_data_sorted.csv")
print("--------------------------------------------")
print(data["sample"].head())


df.to_csv("diagnosis_sample_sorted.csv")

# print(df[df["sample"] == "SAMEA2448333"])





