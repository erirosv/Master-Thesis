import os
from dotenv import load_dotenv
from ftplib import FTP

load_dotenv()

# Anslut till servern
ftp = FTP('SERVER')
ftp.login('USERNAME', 'PASSWORD')

# Läs in filen
with open('FILE_PATH', 'wb') as file:
    ftp.retrbinary('RETR ' + 'FILE_PATH', file.write)

# Stäng anslutningen
ftp.quit()