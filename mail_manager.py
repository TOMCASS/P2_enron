import email
import re
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk import word_tokenize 
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem import wordnet
from nltk import pos_tag
import csv

import string

class mail():
    def is_not_enron_domain(self, email):
        domain = re.findall('(?<=@)([\w.-]+)',email)
        return False if len(domain) == 0 else not 'enron' in str(domain[0]) 

    def get_wordnet_pos(self, tagged_word):
        """
        Categorizing and tagging words
        """
        if tagged_word.startswith('N'):
            return wn.NOUN
        elif tagged_word.startswith('J'):
            return wn.ADJ
        elif tagged_word.startswith('R'):
            return wn.ADV
        elif tagged_word.startswith('V'):
            return wn.VERB
        else:
            return wn.NOUN

    def standardize_text(self, text):

        text = text.lower()
        #remove punctuation
        result = re.compile('[%s]' % re.escape(string.punctuation))
        text = result.sub('', text)

        #simplify lexical content
        tokenized_words = word_tokenize(text)
        tagged_pos = pos_tag(tokenized_words)
        wordnet_pos = [self.get_wordnet_pos(word[1]) for word in tagged_pos]
        lem = WordNetLemmatizer()
        text = " ".join([lem.lemmatize(pair[0], pair[1]) for pair in zip(tokenized_words, wordnet_pos)])

        #remove stop words
        en_stopwords = stopwords.words('english')
        newStopWords = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", "need", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't", "subject","pm","say","please","cc","would", "make", "next", "friday", "dont", "email","new","send","get","forward","may","2001","message","thanks","go","also","u","one","use","week","change","want","could","like","look","question","2000","well","error","2","back","09","file","regard","good","list","today","first","two","date""a", "about", "above", "after", "again", "against", "ain", "all", "am", "an", "and", "any", "are", "aren", "aren't", "as", "at", "be", "because", "been", "before", "being", "below", "between", "both", "but", "by", "can", "couldn", "couldn't", "d", "did", "didn", "didn't", "do", "does", "doesn", "doesn't", "doing", "don", "don't", "down", "during", "each", "few", "for", "from", "further", "had", "hadn", "hadn't", "has", "hasn", "hasn't", "have", "haven", "haven't", "having", "he", "her", "here", "hers", "herself", "him", "himself", "his", "how", "i", "if", "in", "into", "is", "isn", "isn't", "it", "it's", "its", "itself", "just", "ll", "m", "ma", "me", "mightn", "mightn't", "more", "most", "mustn", "mustn't", "my", "myself", "needn", "needn't", "no", "nor", "not", "now", "o", "of", "off", "on", "once", "only", "or", "other", "our", "ours", "ourselves", "out", "over", "own", "re", "s", "same", "shan", "shan't", "she", "she's", "should", "should've", "shouldn", "shouldn't", "so", "some", "such", "t", "than", "that", "that'll", "the", "their", "theirs", "them", "themselves", "then", "there", "these", "they", "this", "those", "through", "to", "too", "under", "until", "up", "ve", "very", "was", "wasn", "wasn't", "we", "were", "weren", "weren't", "what", "when", "where", "which", "while", "who", "whom", "why", "will", "with", "won", "won't", "wouldn", "wouldn't", "y", "you", "you'd", "you'll", "you're", "you've", "your", "yours", "yourself", "yourselves", "could", "he'd", "he'll", "he's", "here's", "how's", "i'd", "i'll", "i'm", "i've", "let's", "ought", "she'd", "she'll", "that's", "there's", "they'd", "they'll", "they're", "they've", "we'd", "we'll", "we're", "we've", "what's", "when's", "where's", "who's", "why's", "would", "year", "see", "day", "last"]       
        en_stopwords.extend(newStopWords)

        tokenized_words = word_tokenize(text)
        text = " ".join([word for word in tokenized_words if word not in en_stopwords])

        return text

    def __init__(self, name, archive):
        text = email.message_from_string(archive)
        self.headers = []
        self.attributes = []

        self.headers.append('id')
        self.attributes.append(name)

        #set from sender in dataset
        self.headers.append('from')
        self.attributes.append(str(text['from']))

        #set to senders in dataset
        self.headers.append('to')        
        self.attributes.append(str(text['to']).replace('\n', '').replace('\t', ''))

        #set mail location in dataset
        self.headers.append('mail_folder')        
        try:
            self.mail_folder = str(text['X-Folder']).split('\\')[3]
        except:
            self.mail_folder = str(None)
        self.attributes.append(self.mail_folder)
        
        #clean up text (punctuation, stopwords, lemmatization)
        self.text = self.standardize_text(text._payload)
        
        #set true/false if incriminating words exists in the body of the email in the dataset
        with open("incriminating_words.csv", "r", encoding="utf-8") as incriminating_word:
            for word in incriminating_word:
                exists = False
                if re.sub('\n','',word) in self.text:
                    exists = True

                self.headers.append(word.rstrip('\n'))
                self.attributes.append(str(exists))

        self.headers.append('cleanedtext')
        self.attributes.append(self.text)

        #set true/false if the mail concerns external consultant
        self.headers.append('is_extern')
        is_extern = False
        is_extern |= self.is_not_enron_domain(str(text['from']))

        for mail in str(text['to']).split(','):
            is_extern |= self.is_not_enron_domain(mail)

        self.attributes.append(str(is_extern))

        #set true/false if the mail location is in incriminating folder
        with open("incriminating_folders.csv", "r", encoding="utf-8") as f:
            incriminating_folders = f.readlines()
        incriminating_folders = [x.strip() for x in incriminating_folders] 
        self.headers.append('is_incriminating_folder')
        self.attributes.append(str(self.mail_folder in incriminating_folders))

    def to_csv_line(self):
        return ';'.join(self.attributes)
        

    def to_csv_header(self):
        return ';'.join(self.headers)

    def to_csv_body(self):
        return self.text

    