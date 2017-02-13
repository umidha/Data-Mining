import math
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import openpyxl
import glob
import string
from nltk.corpus import stopwords
from wordcloud import WordCloud

path = '/usr/local/share/nltk_data/corpora/movie_reviews/neg/'

files = glob.glob(path + '*')
corpus = []
No_of_Documents = 100

for fileNumber in range(0, No_of_Documents):
	with open(files[fileNumber], 'r') as myfile:
		D1 = myfile.read().replace('\n', ' ').lower()
		corpus.append(D1)	

terms = []
for doc in corpus:
	terms = terms + doc.translate(None, string.punctuation).split()
terms = list(set(terms))
terms = [w for w in terms if not w in stopwords.words('english') and len(w) > 2 and not w[0] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']] 

TF = []

n = [0 for i in range(len(terms))]

for doc in corpus:
	tf_doc= [0 for i in range(len(terms))]
	
	for term in doc.translate(None, string.punctuation).split():
		if not term in stopwords.words('english') and len(term) > 2 and not term[0] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
			term_i = terms.index(term)
			tf_doc[term_i] = tf_doc[term_i] + 1
		
	for item in range(len(terms)):
		if tf_doc[item] > 0:
			n[item] = n[item] + 1
	TF.append(tf_doc)

TFN = []

for TFj in TF:
    #for each term TFij
    TFj = [TFij / float(max(TFj)) for TFij in TFj]
    TFN.append(TFj)

N = len(corpus)

IDF = []
for termi in range(len(terms)):
	IDF.append(math.log(No_of_Documents/float(n[termi]), 2))

TFNIDF = []
for TFNj in TFN:
	TFNjIDF = []
	for termIDX in range(len(terms)):
		TFNjIDF.append(TFNj[termIDX]*IDF[termIDX])
	TFNIDF.append(TFNjIDF)



TFNIDF_Matrix = np.matrix(TFNIDF)

# Column Max

C_Max = [TFNIDF_Matrix.max(axis = 0).item(i) for i in range(0, len(terms))]
#Column Min
C_Min = [TFNIDF_Matrix.min(axis = 0).item(i) for i in range(0, len(terms))]
#Column Mean
C_Mean = [TFNIDF_Matrix.mean(axis = 0).item(i) for i in range(0, len(terms))]

Column_Stats = [C_Max, C_Min, C_Mean]
Column_Stats = pd.DataFrame(Column_Stats)

#Row Maximum
R_Max = [TFNIDF_Matrix.max(axis = 1).item(i) for i in range(0, No_of_Documents)]
#Column Min
R_Min = [TFNIDF_Matrix.min(axis = 1).item(i) for i in range(0, No_of_Documents)]
#Column Mean
R_Mean = [TFNIDF_Matrix.mean(axis = 1).item(i) for i in range(0, No_of_Documents)]

Row_Stats = [R_Max, R_Min, R_Mean]
Row_Stats = pd.DataFrame(Row_Stats)

TFIDX = pd.DataFrame(TFNIDF)
TFIDX.columns = terms

#TFIDX.to_csv('result.csv', sep='\t', encoding='utf-8')

writer = pd.ExcelWriter('result_cloud.xlsx', engine='xlsxwriter')

# Convert the dataframe to an XlsxWriter Excel object.
TFIDX.to_excel(writer, sheet_name='Sheet1')
Row_Stats.to_excel(writer, sheet_name = 'Sheet2')
Column_Stats.to_excel(writer, sheet_name = 'Sheet3')

# Close the Pandas Excel writer and output the Excel file.
writer.save()	

#Plotting

word_frequency_list = []
document_no = 0

for i in range(0,5):
	max_temp = max(TFNIDF[document_no])
	max_index = TFNIDF[document_no].index(max_temp)
	word_frequency = (terms[max_index], max_temp)
	word_frequency_list.append(word_frequency)
	TFNIDF[document_no][max_index] = 0

wordcloud = WordCloud().generate_from_frequencies(word_frequency_list)
plt.imshow(wordcloud)
plt.show()
