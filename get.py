import paramiko
import os

hostname = '154.205.159.234'
port = 22
username = 'root'
password = 'SemarangHebat2022!'

files = ['exe.go']  # List of files to upload
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
    sftp.put(local_file, remote_file)

# Run the build command on the remote server
print("Running build command on remote server...")
stdin, stdout, stderr = ssh.exec_command(f"cd {remote_path} && source /etc/profile && /usr/local/go/bin/go build {files[0]}")

# Print command output
print(stdout.read().decode())
print(stderr.read().decode())

# Retrieve the built file
built_file = os.path.join(remote_path, 'exe')  # Assuming 'exe' is the output binary
local_built_file = os.path.join(local_path, 'exe')
go_local_built_file = os.path.join(local_path, 'exe.go')
go_remote_built_file = os.path.join(remote_path, 'exe.go')


print(f"Downloading {built_file} to {local_built_file}...")
sftp.get(built_file, local_built_file)
# sftp.get(go_remote_built_file, go_local_built_file)

# Close the SFTP session and SSH connection
sftp.close()