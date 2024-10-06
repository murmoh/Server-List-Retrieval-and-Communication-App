import socket
import threading
import tkinter as tk
import sys
from tkinter import simpledialog
from blur import *

if len(sys.argv) < 3:
    print("Please provide server IP and port as command-line arguments.")
    sys.exit(1)

server_ip = sys.argv[1]
server_port = int(sys.argv[2])

root = tk.Tk()
root.withdraw()
username = replace_bad_words(simpledialog.askstring("Username", "Please enter your username"))
root.destroy()

my_gui = None


class ChatClient:
    def __init__(self, root, server_ip, server_port):
        self.root = root
        root.title("Chat Application")

        self.main_frame = tk.Frame(root)
        self.main_frame.pack(fill="both", expand=True)

        self.chat_frame = tk.Frame(self.main_frame, width=200, height=400)
        self.chat_frame.pack(fill="both", expand=True, side="left")

        self.text_history = tk.Text(self.chat_frame)
        self.text_history.pack()

        self.message_entry = tk.Entry(self.chat_frame)
        self.message_entry.bind("<Return>", self.send_message)
        self.message_entry.pack()

        self.send_button = tk.Button(self.chat_frame, text="Send", command=self.send_message)
        self.send_button.pack()

        self.online_frame = tk.Frame(self.main_frame, width=200, height=400)
        self.online_frame.pack(fill="both", expand=False, side="right")

        self.online_label = tk.Label(self.online_frame, text="Online Users")
        self.online_label.pack()

        self.online_list = tk.Listbox(self.online_frame)
        self.online_list.pack(fill="both", expand=True)

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(("0.0.0.0", server_port))  # IP HERE

        self.username = username
        self.client.send(self.username.encode('utf-8'))

        threading.Thread(target=self.receive_messages_thread, daemon=True).start()

        self.root.protocol("WM_DELETE_WINDOW", self.close_connection)

    def send_message(self, event=None):
        message = self.message_entry.get()
        if message != "":
            self.text_history.insert(tk.END, "You: " + message + "\n")
            self.text_history.see(tk.END)
            self.message_entry.delete(0, tk.END)
            self.client.send(message.encode('utf-8'))

    def receive_messages_thread(self):
        while True:
            try:
                message = self.client.recv(1024).decode('utf-8')

                if message.startswith("ONLINE_PLAYERS:"):
                    users = message[len("ONLINE_PLAYERS:"):].split(",")
                    self.online_list.delete(0, tk.END)
                    for user in users:
                        self.online_list.insert(tk.END, user)
                else:
                    self.text_history.insert(tk.END, message + "\n")
                    self.text_history.see(tk.END)
            except OSError:
                break

    def close_connection(self):
        self.client.send("DISCONNECTING".encode('utf-8'))
        self.client.close()
        self.root.destroy()


def Join_Server():
    global my_gui
    root = tk.Tk()
    my_gui = ChatClient(root, "10.0.0.212", server_port)
    root.mainloop()
    root.destroy()


Join_Server()
