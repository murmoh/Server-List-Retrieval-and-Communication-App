import random
import sys
import threading
from blur import *
import socket
import json

clients = {}
stop_server = False


def stop_server_after_delay():
    global stop_server
    if not clients:
        stop_server = True


def broadcast(message, username, conn=None, notify_online=False):
    broken_clients = []
    for client_conn, client_username in list(clients.items()):  # Create a copy of dictionary items
        if client_conn != conn:
            try:
                if client_username == username:
                    client_conn.sendall(f"You: {message}".encode('utf-8'))
                else:
                    client_conn.sendall(f"{username}: {message}".encode('utf-8'))
            except (ConnectionResetError, ConnectionAbortedError):  # Catching ConnectionAbortedError too
                broken_clients.append(client_conn)

    for client_conn in broken_clients:
        del clients[client_conn]

    if notify_online:
        online_players = get_online_players()
        online_message = f"ONLINE_PLAYERS:{','.join(online_players)}"
        for client_conn in clients.keys():
            try:
                client_conn.sendall(online_message.encode('utf-8'))
            except (ConnectionResetError, ConnectionAbortedError):  # Catching ConnectionAbortedError too
                pass
        # Update the server list's online players
        update_online_players(online_players)


def update_online_players(online_players):
    # Save the online players to a file
    with open("online_players.txt", "w") as f:
        f.write("\n".join(online_players))


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    username = conn.recv(1024).decode('utf-8')
    print(f"Username: {username}")
    clients[conn] = username

    broadcast(f"{username} has joined the chat.", username, conn, notify_online=True)

    while True:
        try:
            message = conn.recv(1024)
            if not message or message.decode('utf-8') == "DISCONNECTING":
                break
            text = replace_bad_words(message.decode('utf-8'))
            print(f"[{username}] {text}")
            broadcast(text, username, conn)
        except:
            break

    print(f"[DISCONNECTED] {username} disconnected.")
    if conn in clients:  # Check if the connection exists before deleting
        del clients[conn]
    broadcast(f"{username} has left the chat.", "Server", conn, notify_online=True)
    conn.close()


def get_online_players():
    return list(clients.values())


def write_server_info_to_file(ip, port, name):

    server_info = {"ip": ip, "port": port, "name": name}
    servers = get_servers_from_file()

    # Check if server with same IP and port already exists
    if any(server["ip"] == ip and server["port"] == port for server in servers):
        return

    # Add the new server info
    servers.append(server_info)

    with open("server_ips.json", "w") as f:
        json.dump(servers, f)

def get_servers_from_file():
    try:
        with open("server_ips.json", "r") as f:
            servers = json.load(f)
            return servers
    except FileNotFoundError:
        print("No server list file found")
        return []


def start(server_ip, server_port, server_name):
    global stop_server
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 0)  # Allow reusing address
    server.bind((server_ip, server_port))
    server.listen()
    print("Server is listening...")
    ip, _ = server.getsockname()

    servers = get_servers_from_file()

    # Check if server with same IP and port already exists
    if not any(s["ip"] == ip and s["port"] == server_port for s in servers):
        write_server_info_to_file('Public IP HERE', server_port, server_name)
    else:
        print("Server already exists, not updated in file")

    # Handle incoming connections
    while True:
        try:
            client_socket, client_address = server.accept()
            print(f"New connection from {client_address}")
            # Here you should handle the client_socket connection
            # For example, you could create a new thread to handle each client

        except KeyboardInterrupt:
            print("Stopping server.")
            break

    server.close()


if __name__ == "__main__":
    server_ip = socket.gethostbyname(socket.gethostname())
    server_port = random.randint(1001, 1100)
    print(server_port)
    servers = get_servers_from_file()

    # Assuming you want to use the first server in the list
    if len(servers) > 0:
        server = servers[0]
        server_name = server["name"]
        start(server_ip, server_port, server_name)
    else:
        print("No servers found in the file")
