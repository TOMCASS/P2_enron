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
        #remove punctuation
        result = re.compile('[%s]' % re.escape(string.punctuation))
        text = result.sub('', text)

        #remove stop words
        en_stopwords = set(stopwords.words('english'))
        tokenized_words = word_tokenize(text)
        text = " ".join([word for word in tokenized_words if word not in en_stopwords])

        #simplify lexical content
        tokenized_words = word_tokenize(text)
        tagged_pos = pos_tag(tokenized_words)
        wordnet_pos = [self.get_wordnet_pos(word[1]) for word in tagged_pos]
        lem = WordNetLemmatizer()
        return " ".join([lem.lemmatize(pair[0], pair[1]) for pair in zip(tokenized_words, wordnet_pos)])

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
                if word in text:
                    exists = True

                self.headers.append(word.rstrip('\n'))
                self.attributes.append(str(exists))


    def to_csv_line(self):
        return ';'.join(self.attributes)
        

    def to_csv_header(self):
        return ';'.join(self.headers)

    def to_csv_body(self):
        return self.text

    