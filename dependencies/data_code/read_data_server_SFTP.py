import paramiko
import os
from dotenv import load_dotenv

load_dotenv()

server = os.getenv('SERVER')
username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')
file_path = os.getenv('FILE_PATH_2')
port = os.getenv('PORT')

local_filepath = '/home/rusty/fun/Master-Thesis/dependencies/data_code/data'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(server, port=port, username=username, password=password)

# Öppna en SFTP-session
sftp = client.open_sftp()

# Läs in filen
sftp.get(file_path, local_filepath)

# Stäng SFTP-sessionen och SSH-anslutningen
sftp.close()
client.close()