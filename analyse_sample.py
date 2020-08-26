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

d  = {}
for _, data_mail in dataset.iterrows():
    for to_mail in data_mail['to'].split('-'):
        fromto = data_mail['from'] + "-" + to_mail
        tofrom = to_mail + "-" + data_mail['from']

        if not fromto in d and not tofrom in d:
            d[fromto] = 1
        else:
            try:
                d[fromto] = d[fromto] + 1
            except:
                d[tofrom] = d[tofrom] + 1

d = dict(sorted(d.items(), key=lambda x: x[1], reverse=True)[:20])

print(d.keys)
