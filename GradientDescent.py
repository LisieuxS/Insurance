import numpy as np #numpy is used to make some operations with arrays more easily
import pandas as pd #to manage the dataset :)
import matplotlib.pyplot as plt #for plotting 
from sklearn.model_selection import train_test_split #split of the training and test sets

#Lisieux Serrano
#A01207648
#Life Insurance

#Data Set Selection
df = pd.read_csv('insurance.csv') 
df = df[["age","sex","bmi","children","smoker","region", "charges"]]
###

#Preprocessing
thing1= pd.get_dummies(df['sex'])
thing2= pd.get_dummies(df['region'])
###

#sex hot encoding
df=pd.concat([df, thing1], axis=1).drop('sex', axis=1) 
#region hot encoding
df=pd.concat([df, thing2], axis=1).drop('region', axis=1)
df=df.reindex(columns=["age","male", "female", "bmi","children","smoker","northwest","northeast","southwest","southeast","charges"]) 
###

#More preprocessing
df["smoker"]=df["smoker"].map({"yes":1, "no":0}) #map to change yes to 1 and no to 0

X=df[["age","male", "female", "bmi","children","smoker","northwest","northeast","southwest","southeast"]]
y=df["charges"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.40, random_state=42)

__errors__= []

#tetas sumatory
def h(params, sample):
	acum = 0
	for i in range(len(params)):
		acum = acum + params[i]*sample[i]  
	return acum

def show_errors(params, samples,y):
	global __errors__
	error_acum =0
	for i in range(len(samples)):
		hyp = h(params,samples[i]) 
		error=hyp-y[i]
		error_acum=+error**2 
	mean_error_param=error_acum/len(samples)
	__errors__.append(mean_error_param)

def GD(params, samples, y, alfa):
	temp = list(params)
	general_error=0
	for j in range(len(params)):
		acum =0; error_acum=0
		for i in range(len(samples)):
			error = h(params,samples[i]) - y[i] 
			acum = acum + error*samples[i][j]  
		temp[j] = params[j] - alfa*(1/len(samples))*acum  
	return temp

def scaling(samples):
	acum =0
	samples = np.asarray(samples).T.tolist() 
	for i in range(1,len(samples)):	
		for j in range(len(samples[i])):
			acum=+ samples[i][j]
		avg = acum/(len(samples[i]))
		max_val = max(samples[i])
		for j in range(len(samples[i])):
			#print(samples[i][j])
			samples[i][j] = (samples[i][j] - avg)/max_val  
	return np.asarray(samples).T.tolist()

params = [0,0,0,0,0,0,0,0,0,0]
samples = X_train.values[1:].tolist()
y = y_train[1:].tolist()

alfa =.01  #learning rates, length of steps
for i in range(len(samples)):
	if isinstance(samples[i], list):
		samples[i]=  [1]+samples[i]
	else:
		samples[i]=  [1,samples[i]]

samples = scaling(samples)



epochs = 0

while True:  #  run gradient descent until local minima is reached
	oldparams = list(params) 
	params=GD(params, samples,y,alfa)	
	show_errors(params, samples, y)  #only used to show errors, it is not used in calculation
	epochs = epochs + 1
	if(oldparams == params or epochs == 2000):   #  local minima is found when there is no further improvement
		
		print ("final params:")
		print (params)
		break

#plt.plot(__errors__)
#plt.show()

#Predictions
test_samples = X_test.values.tolist()
for i in range(len(test_samples)):
	if isinstance(test_samples[i], list):
		test_samples[i]=  [1]+test_samples[i]
	else:
		test_samples[i]=  [1,test_samples[i]]
test_samples = scaling(test_samples) # scaling and obtaining test samples
y_pred = []
for i in range(len(test_samples)):
	y_pred.append(h(params,test_samples[i])) # h for making predictions with the test samples
###

y_test = y_test.tolist() # test results in a list
from sklearn.metrics import mean_squared_error, r2_score
print('Mean squared error: %.2f' 
      % mean_squared_error(y_test, y_pred))
print('Coefficient of determination: %.2f'
      % r2_score(y_test, y_pred))

userinput=[]    
userinput.append(int(input("age: "))) 
sex = input("sex [male/female]: ")
userinput += [1,0] if sex == "male" else [0,1]
weight=float(input("weight [kg]: "))
height = float(input("height [m]: "))
userinput.append(weight/height**2)
userinput.append(int(input("number of children: ")))
smoker=input("smoker [yes/no]: ")
userinput+= [1] if smoker == "yes" else [0]
region=input("region [northeast/northwest/southeast/southwest]: ")
if region=="northwest":
    addition=[1,0,0,0]
elif region=="northeast":
    addition=[0,1,0,0]
elif region =="southwest":
    addition=[0,0,1,0]
else:
    addition=[0,0,0,1]
userinput+= addition

test_samples = X_test.values.tolist()
test_samples.append(userinput) #addition of the new sample
for i in range(len(test_samples)):
	if isinstance(test_samples[i], list):
		test_samples[i]=  [1]+test_samples[i]
	else:
		test_samples[i]=  [1,test_samples[i]]
test_samples = scaling(test_samples)  
prediction = h(params, test_samples[-1]) #make prediction
print(prediction)


