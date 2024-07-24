import paramiko
import argparse

parser = argparse.ArgumentParser(description='Process IP address.')
    
# Add the --ip argument
parser.add_argument('--ip', required=True, help='IP address to process')
    
 # Parse the arguments
args = parser.parse_args()
    
def ssh_connect_and_run_command(hostname, port, username, password, command):
    try:
        # Create an SSH client
        ssh = paramiko.SSHClient()
        # Automatically add the server's host key (not recommended for production)
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        # Connect to the server
        print(f"Connecting to {hostname}:{port} as {username}...")
        ssh.connect(hostname, port=port, username=username, password=password)

        # Create an SFTP session
        sftp = ssh.open_sftp()
        
        # Local bash file
        local_temp_file_path = 'exe'
        remote_temp_file_path = '/tmp/temp4'  # Path on the remote server

        # Upload the file via SFTP
        print(f"Uploading {local_temp_file_path} to {remote_temp_file_path}...")
        sftp.put(local_temp_file_path, remote_temp_file_path)

        # Write the commands to execute
        commands = [
            f'chmod +x {remote_temp_file_path}',
            f'{remote_temp_file_path} -address="{args.ip}" -user="deddy.handoko" -pass="Nofraud24!" -cmd="show interfaces description"',
            f'rm {remote_temp_file_path}',
        ]

        # Execute the commands
        for cmd in commands:
            stdin, stdout, stderr = ssh.exec_command(cmd)
            print(f"Command: {cmd}")
            print("Output:")
            print(stdout.read().decode())
            print("Errors:")
            print(stderr.read().decode())
            
        sftp.get("status.log", f"status-{args.ip}.log")
        
        commands = [
            f'rm status.log',
        ]

        # Execute the commands
        for cmd in commands:
            stdin, stdout, stderr = ssh.exec_command(cmd)
            print(f"Command: {cmd}")
            print("Output:")
            print(stdout.read().decode())
            print("Errors:")
            print(stderr.read().decode())

        # Close the SFTP session
        sftp.close()
        
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the SSH connection
        ssh.close()

# Usage example
if __name__ == "__main__":
    hostname = "10.14.4.5"  # Replace with your server's hostname or IP address
    port = 21112            # SSH port (default is 22)
    username = "rangga.yudistira"  # Replace with your username
    password = "Sipsip@1986"       # Replace with your password
    command = ""                  # Replace with the command you want to run

    ssh_connect_and_run_command(hostname, port, username, password, command)
