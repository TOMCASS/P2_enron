import pandas as pd
import os
import numpy
from collections import Counter
import re

def get_mail_domain(email):
    domain = re.findall('(?<=@)([\w.-]+)',email)
    return '' if len(domain) == 0 else str(domain[0])

SAMPLE_DATA_PATH = os.path.join(os.getcwd() , "sample_dataset.csv")

dataset = pd.read_csv(SAMPLE_DATA_PATH,error_bad_lines=False, sep=';')

fulltext = " ".join(str(text) for text in dataset['cleanedtext'])

split_it = fulltext.split() 
Counter = Counter(split_it) 
most_occur = Counter.most_common(100) 

print('most used words')
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

print("top collaborators' mails exchanges")
print(d.keys())


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

