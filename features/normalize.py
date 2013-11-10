import csv
import numpy
from sklearn import preprocessing
days_input_file = "../../see-click-predict/res/days_feature_test.csv"
tfidf_input_file = "../files/tfidf_test.data"
output_file = "../files/normalized_features_test.csv"

days_list= []
tfidf_list = []

days_input_data = csv.reader(open(days_input_file, 'rb'), delimiter=',', quotechar='"')
for row in days_input_data:
    days_list.append( float(row[1]) )

tfidf_input_data = csv.reader(open(tfidf_input_file, 'rb'), delimiter=',', quotechar='"')
for row in tfidf_input_data:
    tfidf_list.append( float(row[0]) )

print len(tfidf_list)
print len(days_list)
matrix = (tfidf_list, days_list)
matrix = numpy.array(matrix)
min_max_scaler = preprocessing.MinMaxScaler()
scaled = min_max_scaler.fit_transform(matrix)

output_writer = csv.writer(open(output_file, "wb"), delimiter = ",", quotechar = '"', quoting = csv.QUOTE_MINIMAL )

output_writer.writerow(["inverse_log_days", "tfidf"])
for row in matrix.transpose():
    output_writer.writerow(row)

