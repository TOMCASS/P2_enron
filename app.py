import os
import re
import email

MAILDIR_PATH = os.getcwd() + os.sep + "maildir"

with open("blablabla.csv", "w") as file_out:
    for mail in mails:
        with open(mail, "r", encoding="utf-8") as file_in:
            print(mail)
            v= file_in.read()
            b = email.message_from_string(v)
            bbb = b['from']
            ccc = b['to']
            ddd = b['X-Folder'].split('\\')[3]
            eee = b._payload

            file_out.write(bbb)
            
