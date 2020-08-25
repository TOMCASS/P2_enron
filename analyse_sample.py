import pandas as pd
import os
import numpy
from collections import Counter 

SAMPLE_DATA_PATH = os.path.join(os.getcwd() , "sample_dataset.csv")

dataset = pd.read_csv(SAMPLE_DATA_PATH,error_bad_lines=False, sep=';')

fulltext = " ".join(str(text) for text in dataset['cleanedtext'])

split_it = fulltext.split() 
Counter = Counter(split_it) 
most_occur = Counter.most_common(100) 
print(most_occur) 


