import numpy as np
import csv
import math
import time
from sklearn.tree import DecisionTreeRegressor
from sklearn import preprocessing
from sklearn.feature_extraction import DictVectorizer
from sklearn.ensemble import AdaBoostRegressor
from sklearn import cross_validation
from sklearn.metrics import make_scorer


file_name = "../files/test.csv"
output_file = "./Xencoded_test.csv"

''' Load data '''
# load training data into dict
data = []

reader = csv.DictReader(open(file_name, 'rb'), delimiter=',', quotechar='"')
for row in reader:
    data.append(row)
rng = np.random.RandomState(1)
# convert appropriate keys from string to appropriate type
for sub in data:
    for key in sub:
        if key == 'id' or key == 'num_votes' or key == 'num_comments' or key == 'num_views':
            sub[key] = int(sub[key])
        elif key == 'latitude' or key =='longitude':
            sub[key] = float(sub[key])
        elif key == 'created_time':
            sub[key] = time.mktime(time.strptime(sub[key], "%Y-%m-%d %H:%M:%S"))    # make time into datetime (float)
        elif key == 'summary':
            sub[key] = len(sub[key])
        elif key == 'description':
            sub[key] = len(sub[key])
print "Training data loaded successfully!"

''' Pre-process training data '''
# select which variables to fit the model on
X_vars = ['source', 'tag_type']
X = []

for d in data:
    subdict_X = dict([(i, d[i]) for i in X_vars if i in d])
    subdict_X["loc"] = "%s%s" % ( str( math.ceil(abs( float(d['latitude'])) ) ), str( math.ceil(abs(float(d['longitude']))) ) ) 
    X.append(subdict_X)

# encode categorical variables in X
vec_X = DictVectorizer()

X_transformed = vec_X.fit_transform(X)
X_encoded = X_transformed.toarray()

print "Length of the X file: ", len(X_encoded)

output_csv = csv.writer( open(output_file,"wb"), X_encoded, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

output_csv.writerow(vec_X.get_feature_names())
for row in X_encoded:
    output_csv.writerow(row)

print 'xxxxx X encoded to ' , output_file, '  xxxxx'

