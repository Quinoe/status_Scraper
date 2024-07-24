import paramiko
import os 

hostname = '154.90.49.143'
port = 22
username = 'root'
password = 'SemarangHebat2022!'

files = ['exe']  # List of files to upload
remote_path = '/tmp/exe/'  # Remote directory path
local_path = ''  # Local directory path (set to current directory)

# Create an SSH client
ssh = paramiko.SSHClient()
# Automatically add the server's host key (not recommended for production)
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# Connect to the server
print(f"Connecting to {hostname}:{port} as {username}...")
ssh.connect(hostname, port=port, username=username, password=password)

# Create an SFTP session
sftp = ssh.open_sftp()

# Upload files
for file in files:
    local_file = os.path.join(local_path, file)
    remote_file = os.path.join(remote_path, file)

    print(f"Uploading {local_file} to {remote_file}...")
    sftp.get(remote_file, local_file)
    # sftp.put(local_file, remote_file)

# Close the SFTP session and SSH connection
sftp.close()
ssh.close()