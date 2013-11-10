# -*- coding: utf-8 -*-
"""
Created on Sat Nov 09 19:35:46 2013

@author: Standard User
"""

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

import sys
import numpy
import csv

input_file = '../files/test.csv'
output_file = '../files/tfidf_test.csv'


input_data = csv.DictReader(open(input_file, 'rb'), delimiter=',', quotechar='"')
description = ""
description_list = []

count_vectorizer = CountVectorizer()
for row in input_data:
        description_list.append(row['description'])

freq_term_matrix = count_vectorizer.fit_transform(description_list)
tfidf = TfidfTransformer(norm="l2")
tfidf.fit(freq_term_matrix)
tf_idf_matrix = tfidf.transform(freq_term_matrix)

description_sum = []

header_fields = "tf-idf_norm"
i = 0
for row in tf_idf_matrix:
     value = str(row.sum()/row.shape[0]) 
     description_sum.append( value )

numpy.savetxt(output_file, numpy.asarray(description_sum), fmt="%s")
print "FIN"
