import os
import prepare_sample
from  mail_manager import mail

#CLEANED_MAILS_FOLDER = os.path.join(os.getcwd() , "tmpcleanedup")

if not os.path.isdir( prepare_sample.SAMPLE_DATA_PATH):
    prepare_sample.create_mails_sample_dataset(1)


""" if os.path.exists(CLEANED_MAILS_FOLDER):
        shutil.rmtree(CLEANED_MAILS_FOLDER)

os.makedirs(CLEANED_MAILS_FOLDER) """

#todo : re factorize
def get_sample_mails():
    for path, _, files in os.walk(prepare_sample.SAMPLE_DATA_PATH):
        for filename in  files :
            yield os.path.join(path, filename)

header = False
with open("sample_dataset.csv", "w") as file_out:
    for file in get_sample_mails():
        with open(file, "r", encoding="utf-8") as file_in:
            m = mail(os.path.basename(file), file_in.read())
            if not header:
                file_out.write(m.to_csv_header() + '\n')
                header = True

            print(m.to_csv_line())
            file_out.write(m.to_csv_line() + '\n')

            


