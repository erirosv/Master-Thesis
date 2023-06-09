import paramiko
import os
from dotenv import load_dotenv

load_dotenv()

server = os.getenv('SERVER')
username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')
file_path = os.getenv('FILE_PATH')
port = os.getenv('PORT')

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(server, port=port, username=username, password=password)

# Öppna en SFTP-session
sftp = client.open_sftp()

# Läs in filen
sftp.get(remote_filepath, local_filepath)

# Stäng SFTP-sessionen och SSH-anslutningen
sftp.close()
client.close()