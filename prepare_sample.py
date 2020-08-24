import os
import random
import shutil

MAILDIR_PATH = os.path.join(os.getcwd() , "maildir")
SAMPLE_DATA_PATH = os.path.join(os.getcwd() , "sample")

#todo : re factorize
def get_mails():
    for path, _, files in os.walk(MAILDIR_PATH):
        for filename in  files :
            yield os.path.join(path, filename)

def create_mails_sample_dataset (sample_data_percent) :
    """isolate number of mails to test data

    Args:
        sample_data_percent (int): % of mails to isolate for the test
    """
    print ("Create sample dataset with %s percents of elements" % (sample_data_percent))

    # get global informations
    mails_count = sum(len(files) for _, _, files in os.walk(MAILDIR_PATH)) 
    print("%s mails found in folder : %s" % (mails_count, MAILDIR_PATH))
    nb_sample = int( mails_count * sample_data_percent / 100)
    print("%s mails will be extracted to be used as training dataset" % (nb_sample))

    # Clean up sample folder
    if os.path.exists(SAMPLE_DATA_PATH):
        shutil.rmtree(SAMPLE_DATA_PATH)

    os.makedirs(SAMPLE_DATA_PATH)

    sample_dataset = random.sample(set(get_mails()), nb_sample)
    
    i=1
    for mail in sample_dataset:
        print("(%s) %s" % (i, mail))
        shutil.copy(mail, SAMPLE_DATA_PATH)
        i = i+1

