import os
import subprocess
import socket
import json
import time

from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivymd.uix.card import MDCard
from kivymd.uix.list import OneLineIconListItem, IconLeftWidget
from kivymd.app import MDApp
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.textfield import MDTextField
from ping3 import ping, verbose_ping

from kivy.config import Config
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

subprocess.Popen(["python", "create_server.py"], creationflags=subprocess.CREATE_NEW_CONSOLE)
# Set window size
Window.size = (1920 / 2, 1080 / 2)

# Constants
SERVER_IP = "10.0.0.212"
SERVER_PORT = 1000
SERVERS_FILE = 'server_ips.json'


class MainApp(MDApp):
    last_refresh_time = 0
    server_created = False
    servers = []

    def build(self):
        # Create the main layout
        main_layout = BoxLayout(orientation='vertical')

        # Setup Theme
        self.theme_cls.theme_style = "Dark"  # "Light" or "Dark"
        self.theme_cls.primary_palette = "Orange"  # choose a color that fits your design

        # Define a layout for the input and buttons
        action_layout = BoxLayout(orientation='horizontal', size_hint=(1, None), height='80dp')

        # Add widgets to the action layout
        server_name_input = MDTextField(hint_text='Server Name')
        action_layout.add_widget(server_name_input)

        refresh_button = MDRectangleFlatButton(text='Refresh Server List')
        refresh_button.bind(on_release=self.update_server_list)
        action_layout.add_widget(refresh_button)

        create_button = MDRectangleFlatButton(text='Create New Server')
        create_button.bind(on_release=lambda x: create_server(server_name_input.text))
        action_layout.add_widget(create_button)

        # Add the filter dropdown
        self.filter_dropdown = DropDown()
        for option in ['Low to High Ping', 'High to Low Ping']:
            btn = Button(text=option, size_hint_y=None, height='40dp')
            btn.bind(on_release=lambda btn: self.filter_dropdown.select(btn.text))
            self.filter_dropdown.add_widget(btn)

        filter_button = MDRectangleFlatButton(text='•••••')
        filter_button.bind(on_release=self.filter_dropdown.open)
        action_layout.add_widget(filter_button)

        self.filter_dropdown.bind(on_select=lambda instance, x: setattr(filter_button, 'text', x))
        self.filter_dropdown.bind(on_select=self.filter_server_list)

        # Add the action layout to the main layout
        main_layout.add_widget(action_layout)

        # Create a card for the server list
        self.scroll_layout = BoxLayout(orientation='vertical', size_hint_y=None)
        self.scroll_layout.bind(minimum_height=self.scroll_layout.setter('height'))

        scroll_view = ScrollView(size_hint=(1, None), size=("280dp", "180dp"), pos_hint={"center_x": .2})
        scroll_view.add_widget(self.scroll_layout)

        server_list_card = MDCard(orientation="vertical", padding="180dp")
        server_list_card.add_widget(scroll_view)

        # Add the server list card to the main layout
        main_layout.add_widget(server_list_card)

        # Update the server list
        self.update_server_list(None)

        return main_layout

    def update_server_list(self, instance):
        current_time = time.time()
        # Only refresh the server list if 3 seconds have passed since last refresh
        if current_time - self.last_refresh_time >= 3:
            get_servers_from_server()

            servers = get_servers_from_file()

            self.servers = []
            self.scroll_layout.clear_widgets()

            for server in servers:
                if server['port'] != 1000 and is_server_online(server['ip'], server['port']):
                    # Calculate ping
                    ping_time = ping(server['ip'])
                    # Decide color based on ping value
                    if ping_time < 50:  # adjust these values as per requirement
                        color = 'green'
                    elif ping_time < 100:
                        color = 'yellow'
                    else:
                        color = 'red'
                    server_info = {'server': server, 'ping_time': ping_time, 'color': color}
                    self.servers.append(server_info)

            self.last_refresh_time = current_time
            self.filter_server_list(None, 'Low to High Ping')
        else:
            print("You can only refresh every 3 seconds.")

    @staticmethod
    def create_server_item(server_info):
        server = server_info['server']
        server_name = server.get('name', 'Unnamed server')
        icon = IconLeftWidget(icon="server", theme_text_color="Custom", text_color=server_info['color'])
        ping_info = f'{server_name} - Ping: {round(server_info["ping_time"])}ms'
        item = OneLineIconListItem(text=ping_info)
        item.add_widget(icon)
        item.bind(on_release=lambda x: Join_Server(server, server['port']))
        return item

    def filter_server_list(self, instance, filter):
        self.scroll_layout.clear_widgets()
        if filter == 'Low to High Ping':
            sorted_servers = sorted(self.servers, key=lambda x: x['ping_time'])
        elif filter == 'High to Low Ping':
            sorted_servers = sorted(self.servers, key=lambda x: x['ping_time'], reverse=True)
        else:
            return
        for server_info in sorted_servers:
            item = self.create_server_item(server_info)
            self.scroll_layout.add_widget(item)


def create_server(server_name):
    app = MDApp.get_running_app()
    if app.server_created:
        print("You can only create one server.")
        return

    server_socket = setup_socket(SERVER_IP, SERVER_PORT)

    if not server_name:
        servers = get_servers_from_file()
        server_name = f"server{len([server for server in servers if server.get('name', '').startswith('server')]) + 1}"

    server_socket.send(json.dumps({"type": "CREATE_SERVER", "ip": SERVER_IP, "port": SERVER_PORT, "name": server_name}).encode())
    server_socket.close()

    app.server_created = True


def get_servers_from_server():
    server_socket = setup_socket(SERVER_IP, SERVER_PORT)
    server_socket.send(json.dumps({"type": "GET_SERVERS"}).encode())

    try:
        received_data = server_socket.recv(1024).decode()
        servers = json.loads(received_data)
        server_socket.close()

        with open(SERVERS_FILE, 'w') as f:
            json.dump(servers, f)
    except json.JSONDecodeError as e:
        print("JSON decoding error:", e)
        print("Received data:", received_data)
    except Exception as e:
        print("An error occurred:", e)
        print("Received data:", received_data)

    server_socket.close()


def is_server_online(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.01)
    result = sock.connect_ex((ip, port))
    print(result)
    sock.close()

    return result == 0


def Join_Server(server, port):
    subprocess.Popen(["python", "chat.py", server['ip'], str(port)])
    MDApp.get_running_app().stop()


def get_servers_from_file():
    try:
        with open(SERVERS_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def setup_socket(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))

    return sock


if __name__ == "__main__":
    MainApp().run()
