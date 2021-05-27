import numpy as np #numpy is used to make some operations with arrays more easily
import pandas as pd #to manage the dataset :)
import matplotlib.pyplot as plt #for plotting 
from mpl_toolkits.mplot3d import Axes3D #for cooler plotting
from sklearn import linear_model #linear model needed for lasso implementation
from sklearn.model_selection import train_test_split #split of the training and test sets
from sklearn.metrics import mean_squared_error, r2_score

#Lisieux Serrano
#A01207648
#Life Insurance

#data set selection
df = pd.read_csv('insurance.csv') 
df = df[["age","sex","bmi","children","smoker","region", "charges"]]
###

#preprocessing
thing1= pd.get_dummies(df['sex'])
thing2= pd.get_dummies(df['region'])
###

#sex hot encoding
df=pd.concat([df, thing1], axis=1).drop('sex', axis=1) 
#region hot encoding
df=pd.concat([df, thing2], axis=1).drop('region', axis=1)
df=df.reindex(columns=["age","male", "female", "bmi","children","smoker","northwest","northeast","southwest","southeast","charges"]) 
###

#more preprossesing
df["smoker"]=df["smoker"].map({"yes":1, "no":0}) #map to change yes to 1 and no to 0
###

#determining X set and y
X=df[["age","male", "female", "bmi","children","smoker","northwest","northeast","southwest","southeast"]]
y=df["charges"]
###

#split of data set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)
###

# lasso
regr = linear_model.Lasso() 
# train - linear fit
regr.fit(X_train, y_train)
# predict 
y_pred = regr.predict(X_test) 
###

#print of coefficient, MSE and coefficient of determination
print('Coefficients: \n', regr.coef_)
print('Mean squared error: %.2f' 
      % mean_squared_error(y_test, y_pred))
print('Coefficient of determination: %.2f'
      % r2_score(y_test, y_pred))

#sample_of_list=["age", "sex", "bmi", "children", "smoker","northwest","northeast","southwest","southeast"]

#user interaction and asignation of values to a list
userinput=[]    
userinput.append(int(input("age: "))) 
sex = input("sex [male/female]: ")
userinput += [1,0] if sex == "male" else [0,1] #operador ternario
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
###

#print(userinput)
userinput = np.array(userinput).reshape(1, -1) # single user, one at a time
prediction = regr.predict(userinput)
print(prediction) 


#graphs
#some examples used
#2d
# import matplotlib.pyplot as plt
# plt.scatter(X_test['children'], y_test, color='blue')
# plt.xlabel('children')
# plt.ylabel('insurance price')
# plt.show()

#3d
# x = df['northwest']
# y = df['age']
# z = df['charges']

# fig = plt.figure(figsize=(6, 6))
# ax = fig.add_subplot(111, projection='3d')
# ax.scatter(x, y, z,
#            linewidths=1, alpha=.7,
#            edgecolor='k',
#            s = 200,
#            c=z)
# plt.show()

# plt.scatter(X_test['smoker'], y_test, color='blue')
# plt.xlabel('smoker')
# plt.ylabel('insurance price')
# plt.show()



# x = df['age']
# y = df['smoker']
# z = df['charges']

# fig = plt.figure(figsize=(6, 6))
# ax = fig.add_subplot(111, projection='3d')
# ax.scatter(x, y, z,
#            linewidths=1, alpha=.7,
#            edgecolor='k',
#            s = 200,
#            c=z)
# plt.show()