import pandas as pd
import os
import numpy as np
from collections import Counter
import re
import matplotlib.pyplot as plt

def get_mail_domain(email):
    domain = re.findall('(?<=@)([\w.-]+)',email)
    return '' if len(domain) == 0 else str(domain[0])

SAMPLE_DATA_PATH = os.path.join(os.getcwd() , "sample_dataset.csv")

dataset = pd.read_csv(SAMPLE_DATA_PATH,error_bad_lines=False, sep=';')

fulltext = " ".join(str(text) for text in dataset['cleanedtext'])

split_it = fulltext.split() 
Counter = Counter(split_it) 
most_occur = Counter.most_common(50) 

print('most used words')
print(most_occur) 

word = []
occurrence = []
for i in range(len(most_occur)):
  word.append(most_occur[i][0])
  occurrence.append(most_occur[i][1])
indices = np.arange(len(most_occur))
plt.bar(indices, occurrence, color='r')
plt.xticks(indices, word, rotation='vertical')
plt.tight_layout()
plt.show()
plt.close()

collusion  = {}
for _, data_mail in dataset.iterrows():
    for to_mail in data_mail['to'].split('-'):
        fromto = data_mail['from'] + "-" + to_mail
        tofrom = to_mail + "-" + data_mail['from']

        if not fromto in collusion and not tofrom in collusion:
            collusion[fromto] = 1
        else:
            try:
                collusion[fromto] += 1
            except:
                collusion[tofrom] += 1

collusion = dict(sorted(collusion.items(), key=lambda x: x[1], reverse=True)[:20])

print("top collaborators' mails exchanges")
print(collusion.keys())
plt.bar(range(len(collusion)), list(collusion.values()), align='center')
plt.xticks(range(len(collusion)), list(collusion.keys()), rotation='vertical')
plt.show()
plt.close()


dataset = pd.read_csv(SAMPLE_DATA_PATH,error_bad_lines=False, sep=';')
list_emails = []
for email in dataset['from'].unique():
    list_emails.append(get_mail_domain(email))
for emails in dataset['to']:
    for email in emails.split(','):
        list_emails.append(get_mail_domain(email))

list_emails = pd.unique(list_emails)
#fromdomains= dataset['from'].map(lambda element: get_mails_domain(element)).unique()
#todomains = dataset['to'].str.split(",",expand = True).map(lambda element: get_mail_domain(element))

print('list of mails domains')
print(list_emails)


print('list of mail folders')
print(dataset['mail_folder'].unique())

dataset["is_shifty"] = None
for index, row in dataset.iterrows():
    is_shifty = 0
    for col in dataset.columns: 
        if isinstance(row[col], bool):
            if bool(row[col]):
                is_shifty += 1
    dataset.loc[index, 'is_shifty'] =str(1 if is_shifty > 5 else 0)

print(dataset)

