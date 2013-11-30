import numpy as np
import csv
import math
import time
from sklearn.tree import DecisionTreeRegressor
from sklearn import svm
from sklearn import preprocessing
from sklearn.feature_extraction import DictVectorizer
from sklearn.ensemble import AdaBoostRegressor
from sklearn import cross_validation
from sklearn.metrics import make_scorer


train_x_encode_file = "./Xencoded.csv"
test_x_encode_file = "./Xencoded_test.csv"
input_training_set = "../files/train.csv"
input_test_set = "../files/test.csv"
submission_file = "../files/num_comments.csv"
output_csv_file = "output_"

''' Functions and classes '''
def loss(p_num_comments, a_num_comments):
    # check if shape is the same
    n = p_num_comments.size
    log_p_num_comments = np.log(p_num_comments + 1)
    log_a_num_comments = np.log(a_num_comments + 1)
    sum_num_comments = np.sum(np.square(log_p_num_comments - log_a_num_comments))
    rmsle = np.sqrt((sum_num_comments) / n)
    return rmsle

def scorer_loss(y_predicted, y):
    rmsle = loss(y_predicted, y)
    return rmsle

##def scorer_rmsle(clf, X, y):
    ##clf.fit(X, y)
    ##y_predicted = clf.predict(X)
    ##rmsle = loss(y_predicted[:, 0], y_predicted[:, 1], y_predicted[:, 2], y[:, 0], y[:, 1], y[:, 2])
    ##return rmsle
    

''' Pre-process training data '''
# select which variables to fit the model on

Y_vars = ['num_comments']

Y = []

data = []

reader = csv.DictReader(open(input_training_set, 'rb'), delimiter=',', quotechar='"')
for row in reader:
    data.append(row)

for d in data:
    subdict_Y = dict([(i, float(d[i])) for i in Y_vars if i in d])
    Y.append(subdict_Y)


# encode categorical variables in X
vec_Y = DictVectorizer()
vec_X = DictVectorizer()

x_reader = csv.reader( open(train_x_encode_file), delimiter=',', quotechar='"')

x_reader.next()

new_x_encoded = []

#test data 
for row in x_reader:
    each_row = []
    for element in row:
        each_row.append(float(element))
    new_x_encoded.append(each_row)

# convert y into proper numpy array
#Y_transformed = vec_Y.fit_transform(Y)
Y_encoded = vec_Y.fit_transform(Y).toarray()

# separate training/testing data

X_train, X_test, Y_train, Y_test = cross_validation.train_test_split(new_x_encoded, Y_encoded, test_size=0.7)
# remove unneeded dimension
Y_train = np.squeeze(Y_train)
Y_test = np.squeeze(Y_test)


#''' Begin building the model on training data'''

clf = svm.SVR(kernel='rbf', C=1, epsilon=0.02, gamma=10 )
print X_train.flags, " ", X_train.dtype
print Y_train.flags, " ", Y_train.dtype

clf.fit( X_train,Y_train )

print "before ytrain predicted"
Y_train_predicted = clf.predict(X_train)
Y_test_predicted = clf.predict(X_test)
print "after ytrain predicted: ", Y_train_predicted

train_loss = loss(Y_train_predicted,  Y_train)
test_loss = loss(Y_test_predicted, Y_test)

print "Train loss =", train_loss
print "Test loss =", test_loss


#testing test data and saving results to file
x_reader_test = csv.reader( open(test_x_encode_file), delimiter=',', quotechar='"')
x_reader_test.next()
x_encoded_testdata = []
for row in x_reader_test:
    each_row = []
    for element in row:
        each_row.append(float(element))
    x_encoded_testdata.append(each_row)

print len(x_encoded_testdata)
y_encoded_testdata = clf.predict(x_encoded_testdata)

np.savetxt(submission_file, np.rint(y_encoded_testdata), delimiter=",",  fmt="%f")
print "Saved to file ", submission_file





# custom_scorer = make_scorer(scorer_loss, greater_is_better=False)
# scores = cross_validation.cross_val_score(clf, new_x_encoded, Y_encoded, scoring=custom_scorer)

# #raw_input("/New cv method")
# ######
# #
# #''' Load test data '''
# ## load test data into dict
# data = []
# file_name = input_test_set
# reader = csv.reader(open(file_name, 'rb'), delimiter=',', quotechar='"')
# reader.next()
# for row in reader:
#     each_row = []
#     for element in row:
#         each_row.append(float(element))
#     data.append(each_row)

# #''' Fit model to test data '''
# y_predicted = clf.predict(data)
# #print "Testing model fit!"
# #
# #''' Write submission file for test data '''

# raw_input("Press enter to write submission file")
# id_list = [d['id'] for d in data]
# id_list = np.array(id_list)[:, np.newaxis]
# header_text = "id,num_comments"
# output_array = np.hstack((id_list, y_predicted))
# np.savetxt(submission_file, output_array, delimiter=",", header=header_text, fmt="%f")
