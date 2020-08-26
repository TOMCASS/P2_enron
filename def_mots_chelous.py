import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 

data = pd.read_csv('C:/Users/utilisateur/Documents/3.PROJETS/P2/projet2_git/enron/sample_dataset.csv', sep = ";")

print(data)

def louche(mots_louches):
    chelou = data[mots_louches].value_counts()                        # Trouve le nombre de mail contenants le terme "trade"
    print(chelou)
    return chelou                                                    # Print le résultat

def graph(mots_louches):
    chelou_graph = data[mots_louches].value_counts().plot.bar()       # Créée le graph lié a nombre de mail contenants le terme "trade"
    plt.show(chelou_graph)                                            # Affiche le graph dans une nouvelle fenetre

def louche_graph(mots_louches):
    chelou = data[mots_louches].value_counts()                        
    print(chelou)
    chelou_graph = data[mots_louches].value_counts().plot.bar()       
    plt.show(chelou_graph)          

a = louche
                               