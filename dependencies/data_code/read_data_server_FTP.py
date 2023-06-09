import os
from dotenv import load_dotenv
from ftplib import FTP

load_dotenv()

server = os.getenv('SERVER')
username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')
file_path = os.getenv('FILE_PATH')

# Anslut till servern
ftp = FTP(server)
ftp.login(username, password)

# Läs in filen
with open(file_path, 'wb') as file:
    ftp.retrbinary('RETR ' + file_path, file.write)

# Stäng anslutningen
ftp.quit()