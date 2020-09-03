import os
import sys
import email.message
import re
import csv
import pandas 
#
rootdir ='C:/Users/utilisateur/projet_IA/maildir/allen-p/_sent_mail'
def extract(path):

#
    data = []
  
    index = 0
    dirs = os.listdir(path)
    for fi in dirs:
        with open(path+"/" + fi , 'r')as file:
            mail = email.message_from_string(file.read())
            data.append({'index':index, 'date':mail.get('date'),'From':mail.get('From'), 'To':mail.get('To'), 'content': mail.get_payload()})
            index += 1
            
            
    return(data)
#
data_list = extract(rootdir)
value_liste = []

for dic in data_list:
        key = dic.keys()
        value = dic.values()
        for val in value:
            regex = re.compile(r'[\n\r\t]')
            val = regex.sub("",str(val))
            value_liste.append(val)

    
#print(value_liste)
   
#création d'un fichier csv

with open ('data_set.csv.', 'w', newline= '') as file:

    writer = csv.writer(file)
    #writer.writerow(key)
    writer.writerow(value_liste)
#
#création d'un fichier dataframe
#
# with open("data_set.csv", "r")as filein:
#     data_set_frame = pandas.read_csv(filein)
#     print(data_set_frame)
