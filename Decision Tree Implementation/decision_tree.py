"""
Machine Learning Assignment 2
by Ross Quinn, Student No.: 14553707
and Stephen O'Reilly, Student No.: 16431206
"""
import pandas as pd
from statistics import mean
from statistics import mode
from math import log
import numpy
import random

## SOR
# small function to make writing the confusion matrix to the txt file easier
def matrix_to_string(mat):
    s = ""
    for row in mat:
        for e in row:
            s += "{} ".format(e)
        s += "\n"
    return s

## SOR
# returns its findings as a string in order to write to the results file
def confusion(mat):
    variety = ["Americana", "Avellana", "Cornuta"]
    s = "\nConfusion Matrix:\n"
    s += matrix_to_string(mat)

    # loops through each element of the confusion matrix and creates a string based on the information it gives
    for i in range(len(mat)):   
        s += "{} was correctly classified {} times.\n".format(variety[i], mat[i][i])
        for j in range(len(mat[i])):
            if i == j:
                continue    # a class can't be mistaken for itself
            else:
                s += "\t{} was mistaken for {} {} times.\n".format(variety[i], variety[j], mat[i][j])
    return s    # this string will end up being written to the results file

## SOR
# calculate the entropy of a dataset, no matter how many classes
def entropy(df):
    entropy = 0
    for i in numpy.unique(df[:,-1]):    # for each possible classification
        proportion = len(df[df[:,-1] == i]) / len(df)   # this is the "p-sub-i" part of the entropy equation
        entropy -= proportion*log(proportion, 2)
    return entropy

## SOR
# calculates the gain of an attribute, give dataframe -df and position of attribute -index
# returns the gain that that attribute when split at value x = myu
def gain(df, index):
    
    x = mean(df[:,index])
        
    less_than = df[df[:,index] < x]
    greater_than = df[df[:,index] >= x]

    if len(greater_than) in [0, 1, len(df)-1, len(df)]:
        return -1

    less_entropy = 0
    for i in numpy.unique(df[:,-1]):
        proportion = len(greater_than[greater_than[:,-1] == i])/len(greater_than)
        if proportion == 0:
        	pass
        else:
        	less_entropy -= proportion*log(proportion,2)

    greater_entropy = 0
    for i in numpy.unique(df[:,-1]):
        proportion = len(less_than[less_than[:,-1] == i])/len(less_than)
        if proportion == 0:
        	pass
        else:
        	greater_entropy -= proportion*log(proportion,2)

    gain = entropy(df) - (len(greater_than)/len(df))*less_entropy - (len(less_than)/len(df))*greater_entropy

    return gain

## SOR
# returns the index of the attribute which gives the most information gain
def best_attribute(df):
    best_gain = 0
    best_att = 1
    for i in range(1,11):   # iterate through each attribute, caluclate its gain
        if gain(df, i) > best_gain:
            best_gain = gain(df,i)
            best_att = i            # update when a new best gain has been found
    return best_att

# This function is used to find the most common variety in the groups created by the decision tree by finding the mode of 
# the variety attribute, denoted by 0, 1, and 2. If the mode can not be calculated, such as when two varieties are equally
# common, a random variety is chosen from the dataset
## RQ
def findmode(data):
	try:
		return mode(data)
	except:
		return random.choice(data)

## SOR  # based on previous code by RQ
# splits the df into two smaller ones based on the attribute of greatest gain
def split(x, y):

    # The variable that produces the highest information gain is saved and used to split the dataset         
	best_split[x] = best_attribute(y)

	# The datasets are then split based on this attribute of maximum gain, firstly the two global variabkes are defined
	global greater_than
	global less_than

	# Here, the dataset is split using the mean of the highest information gain attribute, and the resulting entropies are calculated
	greater_than = y[y[:,best_split[x]] >= mean(y[:,best_split[x]])]
	less_than = y[y[:,best_split[x]] < mean(y[:,best_split[x]])]

## SOR # this is defined as its own function for the sake of keeping things neat
def results_to_file(s):
	f = open("results.txt", "w")
	f.write(s)
	f.close()


# This function then allows the user to try to predict the variety of a hazelnut using the decision tree created above
# The function simply takes the row of the desired hazelnuts
## RQ
def predict(x):
    
    # The 'test' dataframe is used here as this allows the original 'train' dataframe to be sliced. This allows for the spliiting
    # of test and training data
    testrow = test[x,:]
    
    # The data is split using the splits created from the training set
    split(0, train)
    if testrow[best_split[0]] > mean(train[:,best_split[0]]):
    	if testrow[best_split[1]] > mean(greater_than[:,best_split[1]]):

    		# Here, the split dataset is first checked to see if all hazelnuts in this dataset were the same variety. If this is the 
    		# case, the function returns that value and stops going forther down the tree
    		if B1 == True:
    			return findmode(highergroup1)
    		else:
	    		split(1, greater_than)
	    		if testrow[best_split[3]] > mean(greater_than[:,best_split[3]]):

	    			# Here, the returned predicted value is given as the most common variety in the created datasets from 
	    			# the training data
	    			return findmode(group2)
	    		else:
	    			return findmode(group1)

    	else:
    		if B2 == True:
    			return findmode(highergroup2)
    		else:

	    		split(1, greater_than)
	    		if testrow[best_split[4]] > mean(less_than[:,best_split[4]]):
	    			return findmode(group4)

	    		else:
	    			return findmode(group3)
		


    else:
    	if testrow[best_split[2]] > mean(less_than[:,best_split[1]]):
    		if B3 == True:
    			return findmode(highergroup3)
    		else:
	    		split(2, less_than)
	    		if testrow[best_split[5]] > mean(greater_than[:,best_split[5]]):
	    			return findmode(group6)
	    		else:
	    			return findmode(group5)

    	else:
    		if B4 == True:
    			return findmode(highergroup4)
    		else:
	    		split(2, less_than)
	    		if testrow[best_split[6]] > mean(less_than[:,best_split[6]]):
	    			return findmode(group8)
	    		else:
	    			return findmode(group7)



print("_____Importing necessary modules...") # keep the user informed as the code runs

# This array will be used to house the attributes that can be best used to split the data at each node
best_split =  [0,0,0,0,0,0,0]

# The Hazelnuts data is read in and a copy is made to be used for test data 
print("____Reading CSV file...")
train = pd.read_csv('hazel.csv')

# Here, an array of unique random numbers are created to be used for splitting the dataset into 1/3rd test and 2/3rds training data
randrows = random.sample(range(0, len(train)), round(len(train)/3))

# These lines use the random numbers above to remove the rows corresponding to those numbers from the training dataset while also
# using these rows for the training dataset 
test = train.values[randrows,:]
train = train.drop(randrows)
train = train.values

# This is the model for a decision tree with a depth of three, and so we get up to 8 groups that our test data could end up in.
# Each split is run through in order and arrays are made to house these groups 
## RQ
split(0,train)
split(1,greater_than)

# Here, groups are created to house the secind splits. A logical variable is then created to check if all varietys in that group are
# the same. If this is the case, later on the decision tree will stop at this part of the branch

print("___Constructing decision tree...")

highergroup1 = greater_than[:,11]
highergroup2 = less_than[:,11]
B1 = (mean(highergroup1) == mode(highergroup1))
B2 = (mean(highergroup2) == mode(highergroup2))
split(3,greater_than)
group2 = greater_than[:,11]
group1 = less_than[:,11]
split(0,train)
split(1,greater_than)
split(4,less_than)
group4 = greater_than[:,11]
group3 = less_than[:,11]
split(0,train)
split(2,less_than)
highergroup3 = greater_than[:,11]
highergroup4 = less_than[:,11]
B3 = (mean(highergroup3) == mode(highergroup3))
B4 = (mean(highergroup4) == mode(highergroup4))
split(5,greater_than)
group6 = greater_than[:,11]
group5 = less_than[:,11]
split(0, train)
split(2,less_than)
split(6,less_than)
group8 = greater_than[:,11]
group7 = less_than[:,11]

# The variables that are chosen each time are saved and displayed here for the user
#print(best_split)

print("__Testing...")
# Here, the predict function is used on all entries in the test dataset.
counter = 0
variety = ('Americana', 'Avellana','Cornuta')

outfile_string = ""

## SOR based on previous code by RQ
confusion_matrix = [[0 for i in range(len(variety))] for i in range(len(variety))]
for i in range(0, len(test)):
   if predict(i) == test[i,11]:
       counter = counter + 1
   actual = variety[int(test[i,11])]
   predicted = variety[int(predict(i))]
   confusion_matrix[int(test[i,11])][int(predict(i))] += 1
   outfile_string += "Actual: {:<10}".format(actual)
   outfile_string += "\tPredicted: {:<10}".format(predicted)
   if actual == predicted:
       outfile_string += "\t\tCorrect\n"
   else:
   	   outfile_string += "\t\tIncorrect\n"

## SOR
outfile_string += "\nC4.5 Decision Tree\nDepth: 3\tTraining data size: {} \tTest data size: {}\n".format(len(train), len(test))
outfile_string += confusion(confusion_matrix)
outfile_string += "\n{} out of {} correct classifications. {:.2f}% accuracy.\n"\
    .format(counter, len(test), (counter/(len(test)))*100)

print("_Writing results to ./results.txt...")
results_to_file(outfile_string)
print("---Program executed---\nAccuracy: {:.2f}%\nYou may find more detailed results at ./results.txt"\
    .format(counter/(len(test)) * 100))

# This can be used to sheck if the tree created a leaf node further up the tree than depth 3 
# print(B1)
# print(B2)
# print(B3)
# print(B4)

# This can show the different datasets
# print(group1)
# print(group2)
# print(group3)
# print(group4)
# print(group5)
# print(group6)
# print(group7)
# print(group8)
