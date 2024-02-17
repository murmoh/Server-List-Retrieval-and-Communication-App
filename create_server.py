import socket
import subprocess
import json

server_ip = "Public IP Here"
server_port = 1000

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((server_ip, server_port))
server_socket.listen(1)

print(f"Create Server is running at {server_ip}:{server_port}")


def load_server_data():
    try:
        with open('server_ips.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def save_server_data(servers):
    with open('server_ips.json', 'w') as f:
        json.dump(servers, f)


while True:
    client_socket, client_address = server_socket.accept()
    print(f"[NEW CONNECTION] {client_address} connected.")

    data = client_socket.recv(1024)
    if not data:
        print(f"No data received from {client_address}")
        continue

    try:
        request = json.loads(data.decode())
    except json.JSONDecodeError:
        print(f"Failed to decode JSON from {client_address}")
        continue

    if request.get("type") == "CREATE_SERVER":
        try:
            subprocess.Popen(["python", "server.py"], creationflags=subprocess.CREATE_NEW_CONSOLE)
            print(f"New server process has been started")
            servers = load_server_data()
            new_server = {"ip": request.get("ip"), "port": request.get("port"), "name": request.get("name")}
            if not any(s['ip'] == new_server['ip'] and s['port'] == new_server['port'] for s in servers):
                servers.append(new_server)
                save_server_data(servers)
                print("Server details written to file")
            else:
                print("Server already exists, not written to file")

        except Exception as e:
            print(f"Failed to start new server or write to file: {e}")


    client_socket.close()
