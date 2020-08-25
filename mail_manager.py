import email
import re
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
from nltk.corpus import stopwords
from nltk import word_tokenize 
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem import wordnet
from nltk import pos_tag

import string

class mail():
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
        newStopWords = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]
        en_stopwords.extend(newStopWords)

        tokenized_words = word_tokenize(text)
        text = " ".join([word for word in tokenized_words if word not in en_stopwords])

        return text

    def __init__(self, archive):
        text = email.message_from_string(archive)
        self.headers = []
        self.attributes = []

        self.headers.append('from')
        self.attributes.append(str(text['from']))
        self.headers.append('to')        
        self.attributes.append(str(text['to']).replace('\n', '').replace('\t', ''))


        self.headers.append('X-Folder')        
        try:
            self.attributes.append(str(text['X-Folder']).split('\\')[3])
        except:
            self.attributes.append(str(None))
        
        self.text = self.standardize_text(text._payload)
        
        with open("incriminating_words.csv", "r", encoding="utf-8") as incriminating_word:
            for word in incriminating_word:
                exists = False
                if re.sub('\n','',word) in self.text:
                    exists = True

                self.headers.append(word.rstrip('\n'))
                self.attributes.append(str(exists))

        self.headers.append('cleanedtext')
        self.attributes.append(self.text)


    def to_csv_line(self):
        return ';'.join(self.attributes)
        

    def to_csv_header(self):
        return ';'.join(self.headers)

    def to_csv_body(self):
        return self.text

    