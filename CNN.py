from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.decomposition import PCA
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
import reduce_data
from random import randint

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.nn.functional as F
import seaborn as sns

import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset


def pCA(df, labels):
	pca = PCA(n_components=2)
	data = df.copy()
	# data.drop(labels="sample")
	print(data["sample"])
	data = data.drop(labels=["sample"], axis=1)

	pca.fit(data)
	x=pca.transform(data)
	plt.figure(figsize=(15,15))

	df_2 = pd.DataFrame()
	df_2["pca-one"] = x[:, 0]
	df_2["pca-two"] = x[:, 1]
	df_2["diagnosis"] = labels["diagnosis"]



	sns.scatterplot(x="pca-one", y="pca-two", 
		data=df_2, hue="diagnosis", 
		palette=sns.color_palette("hls", 13))
	plt.xlabel('pc 1')
	plt.ylabel('pc 2')
	plt.legend()
	plt.show()


data = pd.read_csv('./compiled_data_sorted.csv')
data = data.drop(labels=["sample", "Unnamed: 0.1", "Unnamed: 0"], axis=1)
data = reduce_data.reduce_data(data)
y_train_df = pd.read_csv("./diagnosis_sample_sorted.csv")



def custom_aggregation(series):
	# For example, return the range (max - min) of the column
	c_count = 0
	ad_count = 0
	norm_count = 0
	for string in series.values:
		if(string == "Cancer"): c_count += 1
		elif(string == "Large adenoma" or string == "Small adenoma"): ad_count += 1
		elif(string == "Normal"): norm_count += 1

	maximum = np.max([c_count, ad_count, norm_count])
	if(maximum == c_count): return "Cancer"
	elif maximum == ad_count: return "adenoma"
	else: return "Normal"

	if("Cancer" in series.values ): return "Cancer"
	elif("Large adenoma" in series.values): return "adenoma"
	elif("Small adenoma" in series.values): return "adenoma"
	elif ("Normal" in series.values): return "Normal"
	else: return "Normal"

# Use the custom function in groupby aggregation
y_train_df = y_train_df.groupby("sample").agg({
    "sample": lambda x: ", ".join(x.unique()),  # Combine unique names
    "diagnosis": custom_aggregation              # Apply the custom aggregation
})

# pCA(data, y_train_df)



label_encoder = LabelEncoder()



device = "cuda" if torch.cuda.is_available() else "cpu"


X_train, X_test, y_train, y_test = train_test_split(
    data.values, label_encoder.fit_transform(y_train_df["diagnosis"].values), test_size=0.33, random_state=42)


y_train_tensor = torch.tensor(y_train)

X_train_tensor = torch.tensor(X_train, dtype=torch.float32)

print(X_train_tensor.shape)
print(y_train_tensor.shape)
dataset = TensorDataset(X_train_tensor, y_train_tensor)
dataloader = DataLoader(dataset, batch_size=16, shuffle=True, drop_last=True)

# Load testing data
y_test_tensor = torch.tensor(y_test)

x_test_tensor = torch.tensor(X_test , dtype=torch.float32)

test_dataset = TensorDataset(x_test_tensor, y_test_tensor)
test_dataloader = DataLoader(dataset, batch_size=16, shuffle=True, drop_last=True)

class MLP(nn.Module):
	def __init__(self):
		# Define layers
		super(MLP, self).__init__()
		self.fc1 = nn.Linear(3120, 64)
		self.bn1 = nn.BatchNorm1d(64)
		self.fc2 = nn.Linear(64, 32)
		self.fc3 = nn.Linear(32, 3)    
		
		self.dropout = nn.Dropout(0.2)

	# Model for forward propagation
	def forward(self, x):
		x = torch.relu(self.bn1(self.fc1(x)))
		x = self.dropout(x)  
		x = torch.relu(self.fc2(x))
		x = self.fc3(x)      
		return x

class convNN(nn.Module):
	def __init__(self):
		super(convNN, self).__init__()
		self.conv1 = nn.Conv1d(16, 32, kernel_size=4)
		self.conv2 = nn.Conv1d(32, 32, kernel_size=7)
		self.max_pool1 = nn.MaxPool1d(kernel_size=2)
		self.conv3 = nn.Conv1d(32, 16, kernel_size=4)
		self.max_pool2 = nn.MaxPool1d(kernel_size=3)
		self.fc1 = nn.Linear(517, 16)
		self.fc2 = nn.Linear(16, 3)

	def forward(self, x):

		# print("pre: " + str(x.shape))      
		x = F.relu(self.conv1(x))  
		# print("post covn1: " + str(x.shape))      

		x = F.relu(self.conv2(x))  
		# print("post conv2: " + str(x.shape))    

		x = self.max_pool1(x)
		# print("post pool 1: " + str(x.shape))      

		x = F.relu(self.conv3(x))  
		# print("post conv 3: " + str(x.shape))      

		x = self.max_pool2(x)  
		# print("post pool2: " + str(x.shape))      
		x = F.relu(self.fc1(x)) 
		# print("post fc1: " + str(x.shape))      

		x = self.fc2(x)       
		# print("post fc2: " + str(x.shape))      
		return x
		



model = convNN()

# Define the loss function
criterion = nn.CrossEntropyLoss()  
# Define the optimizer
optimizer = optim.Adam(model.parameters(), lr=0.001)


num_epochs = 100

# Holds average training loss per epoch
training_loss_per_epoch = []
testing_loss_per_epoch = []

for epoch in range(num_epochs):
	# Set the model into training mode
	model.train()  
	running_loss = 0.0
	num_batches = 0
	num_test_batches = 0
	test_running_loss = 0
	# Stochastic gradient descent on each batch 
	for batch_X, batch_y in dataloader:
		# Zero gradients
		optimizer.zero_grad()
		# Forward pass 
		output = model(batch_X)
		# print(output.shape)
		# print(batch_X.shape)
		# print(batch_y.shape)
		# Compute loss for current batch
		loss = criterion(output, batch_y)
		# Backpropagation
		loss.backward()
		# Update model parameters 
		optimizer.step()

		# Keep track of loss for each batch
		running_loss += loss.item()
		num_batches += 1


	with torch.no_grad():      
		for test_batch_X, test_batch_y in test_dataloader:
			# Forward pass on the entire test set
			output_test = model(test_batch_X)
			# Compute loss on the entire test set
			avg_test_loss = criterion(output_test, test_batch_y).item()
			test_running_loss += avg_test_loss
			num_test_batches += 1

	# Calculate average loss per epoch
	avg_loss = running_loss / num_batches
	training_loss_per_epoch.append(avg_loss)
	testing_loss_per_epoch.append(test_running_loss/num_test_batches)


	# Print epoch and training loss
	print(f'Epoch {epoch+1}/{num_epochs}, Train Loss: {loss:.6f}')
	# print(f'Epoch {epoch+1}/{num_epochs}, test Loss: {loss:.6f}')

print(training_loss_per_epoch)
print(testing_loss_per_epoch)

plt.scatter((range(1,len(training_loss_per_epoch)+1)), training_loss_per_epoch)
plt.xlabel("Number of Epochs")
plt.ylabel("Train Loss")
plt.title("Train Loss Against Number of Epochs")
plt.show()


# # ## TODO evaluation



predicted_labels = []
true_labels = []

with torch.no_grad():
	for batch_X, batch_y in test_dataloader:
		model.eval()
		output = model(batch_X)

		_, tmp_predicted_labels = torch.max(output, 1)  
		predicted_labels.append(tmp_predicted_labels)
		true_labels.append(batch_y)
	
	# true_labels = y_test



report = classification_report(torch.cat(true_labels), torch.cat(predicted_labels), target_names=label_encoder.classes_)
print(report)